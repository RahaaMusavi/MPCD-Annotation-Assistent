import os
import re
import time
import gradio as gr
from openai import OpenAI
import pickle
from pathlib import Path

client = OpenAI()


# ============================================================
# SOURCE FILES
# ============================================================


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SYNTAX_BOOK = BASE_DIR / "data" / "syntax-handbook.md"

MORPHOLOGY_BOOK = BASE_DIR / "data" / "morphology-handbook.md"

UD_PRINCIPLES = BASE_DIR / "data" / "ud-principles.txt"

RAG_CORPUS_FILE = BASE_DIR / "data" / "corpus_for_rag.txt"

CORPUS_FILE = RAG_CORPUS_FILE

ANNOTATED_CORPUS_PICKLE = BASE_DIR / "data" / "annotated_corpus.pkl"

VECTOR_STORE_CACHE = BASE_DIR / "vector_store_cache.pkl"

SOURCE_FILES = [SYNTAX_BOOK, MORPHOLOGY_BOOK, CORPUS_FILE, UD_PRINCIPLES]

MAX_SEARCH_RESULTS = 25



# ============================================================
# CHECK FOR MISSING FILES
# ============================================================


def check_required_files():
    required_files = [
        SYNTAX_BOOK,
        MORPHOLOGY_BOOK,
        UD_PRINCIPLES,
        ANNOTATED_CORPUS_PICKLE,
    ]

    missing = [str(path) for path in required_files if not path.exists()]

    if missing:
        raise FileNotFoundError(
            "Required data files are missing:\n"
            + "\n".join(missing)
            + "\n\nSee data/README.md for information about the required data."
        )



# ============================================================
# CORPUS EXPORT
# ============================================================

def load_annotated_corpus():
    with open(ANNOTATED_CORPUS_PICKLE, "rb") as f:
        return pickle.load(f)


def pick_english_translation(translations):
    """Return the [eng]-tagged translation if present, else the first
    translation available, else None."""
    for t in translations:
        if t.strip().lower().startswith("[eng]"):
            return t
    return translations[0] if translations else None


def export_for_rag(annotated_corpus, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for sent in annotated_corpus:

            f.write(f"SENTENCE_ID: {sent.file_name} | sent_id={sent.sentence_id}\n")

            for key in ("chapter", "section", "subsection", "unit", "part"):
                val = getattr(sent, key, None)
                if val:
                    f.write(f"{key.upper()}: {val}\n")

            if sent.text:
                f.write(f"SURFACE_TEXT: {sent.text}\n")

            translations = sent.get_translations()
            english = pick_english_translation(translations)
            f.write(f"TRANSLATION_ENGLISH: {english or '(none available)'}\n")

            other_translations = [t for t in translations if t != english]
            for t in other_translations:
                f.write(f"OTHER_TRANSLATION: {t}\n")

            f.write("TOKENS (ID | FORM | LEMMA | UPOS | HEAD | DEPREL | DEPS | SENSE | NEWPART | FILE):\n")

            word_tokens = [t for t in sent.get_tokens() if isinstance(t.id, int)]
            word_tokens.sort(key=lambda t: t.id)

            for t in word_tokens:
                newpart = t.misc_dict.get("newpart", "_")
                f.write(
                    f"  {t.id} | {t.form} | {t.lemma} | {t.upos} | "
                    f"{t.head} | {t.deprel} | {t.deps or '_'} | {t.sense} | "
                    f"{newpart} | {sent.file_name}\n"
                )

            f.write("=== END SENTENCE ===\n\n")

    print(f"Exported {len(annotated_corpus)} sentences to {output_path}")


def ensure_rag_corpus_exists():
    if os.path.exists(RAG_CORPUS_FILE):
        return
    print("Loading annotated corpus and exporting for RAG...")
    annotated_corpus = load_annotated_corpus()
    export_for_rag(annotated_corpus, RAG_CORPUS_FILE)

check_required_files()
ensure_rag_corpus_exists()
ensure_rag_corpus_exists()


# ============================================================
# CORPUS LOOKUP
# ============================================================

CORPUS_FOR_LOOKUP = load_annotated_corpus()

FORM_TO_TOKENS = {}
for sent in CORPUS_FOR_LOOKUP:
    for t in sent.get_tokens():
        if isinstance(t.id, int) and t.form:
            FORM_TO_TOKENS.setdefault(t.form, []).append((sent, t))


def find_real_token(form, deprel_claimed):
    """Look for a real token with this exact FORM and DEPREL among the
    actual annotated corpus. Returns (sentence, token) or None."""
    for sent, tok in FORM_TO_TOKENS.get(form, []):
        if tok.deprel == deprel_claimed:
            return sent, tok
    return None


# ============================================================
# VECTOR STORE
# ============================================================

def build_or_load_vector_store():
    """Create the vector store once and reuse it on later runs, re-uploading
    only if a source file has changed since the store was built."""

    sources_signature = {path: os.path.getmtime(path) for path in SOURCE_FILES}

    if os.path.exists(VECTOR_STORE_CACHE):
        with open(VECTOR_STORE_CACHE, "rb") as f:
            cached = pickle.load(f)
        if cached.get("signature") == sources_signature:
            return cached["vector_store_id"]

    print("Building vector store (source files changed or first run)...")

    vector_store = client.vector_stores.create(name="MPCD Corpus and Handbooks")

    for path in SOURCE_FILES:
        with open(path, "rb") as f:
            client.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store.id,
                file=f,
                chunking_strategy={
                    "type": "static",
                    "static": {
                        "max_chunk_size_tokens": 1600,
                        "chunk_overlap_tokens": 800
                    }
                }
            )

    with open(VECTOR_STORE_CACHE, "wb") as f:
        pickle.dump(
            {"signature": sources_signature, "vector_store_id": vector_store.id},
            f
        )

    return vector_store.id


VECTOR_STORE_ID = build_or_load_vector_store()


# ============================================================
# CITATION CLEANUP
# ============================================================

def strip_citation_markers(text):
    """Remove OpenAI's raw file_search reference markers like 【2:syntax-handbook.md】."""
    return re.sub(r"【[^】]*】", "", text)


# ============================================================
# EXAMPLE CHECKS
# ============================================================

def load_raw_source_text():
    """Concatenate the handbooks and corpus export into one searchable
    blob, used to verify that any Middle Persian example sentence the
    model displays actually exists verbatim in a real source file."""
    parts = []
    for path in (SYNTAX_BOOK, MORPHOLOGY_BOOK, RAG_CORPUS_FILE, UD_PRINCIPLES):
        with open(path, "r", encoding="utf-8") as f:
            parts.append(f.read())
    return "\n".join(parts)


RAW_SOURCE_TEXT = load_raw_source_text()


def normalize_for_match(s):
    """Strip hyphens (compound spelling variants like 'ganāg-mēnōy' vs
    'ganāgmēnōy') and markdown emphasis markers (**bold**, *italic*),
    which are formatting artifacts in the source, not content
    differences. '=' is left untouched — it's meaningful clitic
    notation present verbatim in both the handbook and the corpus."""
    s = s.replace("-", "")
    s = s.replace("**", "")
    s = s.replace("*", "")
    return s


NORMALIZED_SOURCE_TEXT = normalize_for_match(RAW_SOURCE_TEXT)


def join_table_words(words):
    """Join a table's FORM values into a phrase, closing the gap before
    any clitic (a token whose FORM starts with '=') so it matches the
    corpus's own no-space clitic-attachment convention, e.g. 'pad' +
    '=iš' -> 'pad=iš', not 'pad =iš'."""
    phrase = ""
    for w in words:
        if not phrase:
            phrase = w
        elif w.startswith("="):
            phrase += w
        else:
            phrase += " " + w
    return phrase


def extract_markdown_tables_raw(answer_text):
    """Split the answer into table blocks using the markdown separator
    row (|---|---|...) as the structural marker for 'previous line was
    a header' — robust regardless of what column names the model uses.
    Returns a list of {'header': [...], 'rows': [(raw_line, cells), ...]}."""
    lines = answer_text.splitlines()
    tables = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and line.count("|") >= 3:
            header_cells = [c.strip().strip("*") for c in line.strip("|").split("|")]
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            next_cells = [c.strip() for c in next_line.strip("|").split("|")] if next_line.startswith("|") else []
            is_separator = bool(next_cells) and all(set(c) <= set("-: ") and c for c in next_cells)

            if is_separator:
                rows = []
                j = i + 2
                while j < len(lines) and lines[j].strip().startswith("|") and lines[j].strip().count("|") >= 3:
                    raw = lines[j]
                    cells = [c.strip().strip("*") for c in raw.strip().strip("|").split("|")]
                    rows.append((raw, cells))
                    j += 1
                tables.append({"header": header_cells, "rows": rows})
                i = j
                continue
        i += 1
    return tables


def is_token_evidence_table(header):
    """Only genuine per-token annotation tables (with a FORM/WORD column
    and a DEPREL column) count as checkable evidence. Recap/summary
    tables that abbreviate examples without real token data are
    excluded, since they aren't citations — they're restatements."""
    header_lower = [h.lower() for h in header]
    has_form = "form" in header_lower or "word" in header_lower
    has_deprel = "deprel" in header_lower
    return has_form and has_deprel


def verify_example_tables(answer_text):
    """For each genuine token-evidence table, split it into contiguous
    runs of real (non-placeholder) words at any '...' boundary, join
    each run with clitic-aware spacing, normalize formatting
    differences, and check for verbatim presence in the source files."""
    suspect = []
    for table in extract_markdown_tables_raw(answer_text):
        if not is_token_evidence_table(table["header"]):
            continue
        header_lower = [h.lower() for h in table["header"]]
        form_idx = header_lower.index("form") if "form" in header_lower else header_lower.index("word")

        words = [
            cells[form_idx]
            for _, cells in table["rows"]
            if form_idx < len(cells) and cells[form_idx].strip()
        ]

        runs = []
        current_run = []
        for w in words:
            if w.strip() in ("...", "…"):
                if current_run:
                    runs.append(current_run)
                    current_run = []
            else:
                current_run.append(w)
        if current_run:
            runs.append(current_run)

        for run in runs:
            if len(run) < 2:
                continue
            phrase = join_table_words(run)
            normalized_phrase = normalize_for_match(phrase)
            if normalized_phrase not in NORMALIZED_SOURCE_TEXT:
                suspect.append(phrase)
    return suspect


def verify_feature_claims(answer_text):
    """Find any 'Feature=Value' style tokens the answer asserts and
    check whether that exact string appears in the real source text."""
    claimed = set(re.findall(r"\b[A-Z][a-zA-Z]+=[A-Za-z]+\b", answer_text))
    return [f for f in claimed if f not in RAW_SOURCE_TEXT]


# ============================================================
# CORPUS CITATIONS
# ============================================================

def reconcile_corpus_citations(answer_text):
    """For every genuine token-evidence table with a NEWPART or FILE
    column, look up each cited FORM+DEPREL pair against the real
    annotated_corpus in memory. If a real matching token exists,
    correct the NEWPART/FILE cells in place to the real values. If no
    matching token exists for that FORM+DEPREL combination, record it
    as unverifiable so it can be flagged rather than trusted."""
    corrected = answer_text
    unverifiable = []

    for table in extract_markdown_tables_raw(answer_text):
        if not is_token_evidence_table(table["header"]):
            continue
        header_lower = [h.lower() for h in table["header"]]
        if "newpart" not in header_lower and "file" not in header_lower:
            continue

        form_idx = header_lower.index("form") if "form" in header_lower else header_lower.index("word")
        deprel_idx = header_lower.index("deprel")
        newpart_idx = header_lower.index("newpart") if "newpart" in header_lower else None
        file_idx = header_lower.index("file") if "file" in header_lower else None

        for raw_line, cells in table["rows"]:
            if form_idx >= len(cells):
                continue
            form = cells[form_idx].strip()
            deprel_claimed = cells[deprel_idx].strip() if deprel_idx < len(cells) else None

            match = find_real_token(form, deprel_claimed) if deprel_claimed else None

            if match is None:
                unverifiable.append(f"{form} (claimed DEPREL: {deprel_claimed})")
                continue

            sent, tok = match
            new_cells = list(cells)
            if newpart_idx is not None and newpart_idx < len(new_cells):
                new_cells[newpart_idx] = tok.misc_dict.get("newpart", "_")
            if file_idx is not None and file_idx < len(new_cells):
                new_cells[file_idx] = sent.file_name

            new_line = "|" + "|".join(new_cells) + "|"
            corrected = corrected.replace(raw_line, new_line, 1)

    return corrected, unverifiable


def expand_corpus_examples(answer_text):
    """For every corpus token citation successfully matched to a real
    token, append the full sentence context (surface text, English
    translation, and complete token table) after the answer — pulled
    directly from annotated_corpus, not from the model's output. This
    guarantees full, correct sentence context regardless of what the
    model chose to display."""
    seen_sentences = {}

    for table in extract_markdown_tables_raw(answer_text):
        if not is_token_evidence_table(table["header"]):
            continue
        header_lower = [h.lower() for h in table["header"]]
        form_idx = header_lower.index("form") if "form" in header_lower else header_lower.index("word")
        deprel_idx = header_lower.index("deprel")

        for _, cells in table["rows"]:
            if form_idx >= len(cells) or deprel_idx >= len(cells):
                continue
            form = cells[form_idx].strip()
            deprel_claimed = cells[deprel_idx].strip()

            match = find_real_token(form, deprel_claimed)
            if match is None:
                continue

            sent, _ = match
            key = (sent.file_name, sent.sentence_id)
            if key not in seen_sentences:
                seen_sentences[key] = sent

    if not seen_sentences:
        return answer_text

    blocks = ["\n\n---\n### Full sentence context (from corpus)\n"]
    for (file_name, sent_id), sent in seen_sentences.items():
        english = pick_english_translation(sent.get_translations())
        blocks.append(f"\n**{file_name} {sent_id}**")
        if sent.text:
            blocks.append(f"\nSurface text: *{sent.text}*")
        blocks.append(f"\nTranslation: {english or '(none available)'}")

        word_tokens = sorted(
            [t for t in sent.get_tokens() if isinstance(t.id, int)],
            key=lambda t: t.id
        )
        blocks.append("\n\n| ID | FORM | LEMMA | UPOS | HEAD | DEPREL | DEPS | SENSE |")
        blocks.append("|---|---|---|---|---|---|---|---|")
        for t in word_tokens:
            blocks.append(
                f"| {t.id} | {t.form} | {t.lemma} | {t.upos} | "
                f"{t.head} | {t.deprel} | {t.deps or '_'} | {t.sense} |"
            )
        blocks.append("")

    return answer_text + "\n".join(blocks)


# ============================================================
# GPT FUNCTION
# ============================================================

def build_prompt(message):
    """Return the instructions for the annotation assistant."""
    return f"""
You are an expert linguistics assistant helping an annotator.

REFERENCE MATERIAL
You have access to the syntax handbook, morphology handbook, annotated
CoNLL-U corpus, and UD principles document through file search.

GROUNDING
- Run file search before every question.
- Search broadly: the requested term, related vocabulary, and relevant
  construction types/sections. For "what is X?" questions, check more than
  one section when appropriate.
- Use the two handbooks first. If they do not answer the question, check the
  corpus. Use UD principles only if the handbooks and corpus are insufficient,
  and say that the generic UD material is being used.
- Do not add facts, rules, examples, translations, or feature values that are
  not supported by the retrieved material.
- If the search finds nothing relevant, answer exactly:
  "I cannot find information regarding [TERM]."
- For factual claims based on retrieved source text, include a short,
  verbatim supporting quotation (under 15 words) followed by the filename.
- Do not turn an unsupported paraphrase into a quotation.
- Keep negative conclusions limited to the search results. Say
  "I found no supporting passage for X" rather than making an absolute claim.

EXAMPLES
- If Middle Persian examples occur in the syntax handbook, morphology
  handbook, or corpus, include at least two distinct examples when available.
- If only one genuinely distinct example exists, use that one and say so;
  never duplicate an example just to reach two.
- Never invent examples.
- Do not reuse an example for a different construction simply because it looks
  similar.
- Search other xcomp sections when needed; MX 2.103 is a valid modal-verb
  xcomp example, while necessitative active/passive examples are not xcomp
  examples.

CORPUS EVIDENCE
- DEPREL and DEPS are separate fields. When assigning a relation to a token,
  use the exact value attached to that token in the retrieved data.
- Never infer a relation from translation, meaning, POS, or a similar token.
  This applies to every relation mentioned, not just the requested one.
- Every corpus-sourced claim must be shown in a full token table with:
  ID, FORM, LEMMA, UPOS, HEAD, DEPREL, NEWPART, FILE, and SENSE.
- Every displayed value must be real. Do not invent placeholders.
- HEAD is meaningful only in sentence context, so do not show it for an
  isolated token.
- Use the token's actual NEWPART and FILE values for corpus citations.
  Never cite the uploaded filename. If NEWPART is "_", state that no
  newpart is recorded.
- Use the authoritative sentence TRANSLATION field only. Never construct a
  translation from individual token forms or lemmas.
- Do not create abbreviated recap tables.
- Token SENSE is a word-level gloss; TRANSLATION is reserved for the full
  sentence translation.
- Before using an example, verify that its text occurs in the retrieved
  source. Before using a corpus token, verify its exact row. Do not cite the
  same sentence twice.
- If a corpus relation cannot be verified directly from DEPREL/DEPS, do not
  claim that the example illustrates that relation.

FEATURES AND CONSTRUCTIONS
- Morphological feature values are exact labels. State X=Y only when that
  exact string occurs in the retrieved material.
- Match examples to the construction actually discussed in their source.
- The handbook's necessitative active/passive examples must not be presented
  as xcomp examples.
- If two source passages repeat the same explanation, state it once; retain
  distinct details.

ANSWER STYLE
- Begin with a short Markdown heading naming the requested term(s).
- Explain the material in your own concise words rather than copying large
  passages.
- State separate facts in plain sentences.
- Avoid repetitive transitions and filler.
- Include all materially different points supported by the relevant sources.
- If a summary is included, make it a plain list of the main characteristics;
  do not repeat examples in the summary.
- Do not write "according to the handbooks" as filler.

CURRENT USER QUESTION
{message}
"""


def message_gpt(message):
    if not message or not message.strip():
        yield "*Please ask your question.*", ""
        return

    prompt = build_prompt(message)

    max_retries = 3
    stream = None
    for attempt in range(max_retries):
        try:
            stream = client.responses.create(
                model="gpt-4.1",
                input=prompt,
                tools=[{
                    "type": "file_search",
                    "vector_store_ids": [VECTOR_STORE_ID],
                    "max_num_results": MAX_SEARCH_RESULTS
                }],
                tool_choice="required",
                temperature=0,
                stream=True
            )
            break
        except Exception as e:
            if attempt == max_retries - 1:
                yield f"**⚠ Rate limit or error, please try again shortly.**\n\n{e}", ""
                return
            time.sleep(16)

    partial_answer = ""
    for event in stream:
        if event.type == "response.output_text.delta":
            partial_answer += event.delta
            yield partial_answer, ""

    cleaned_answer = strip_citation_markers(partial_answer)
    cleaned_answer, unverifiable_corpus = reconcile_corpus_citations(cleaned_answer)
    suspect_phrases = verify_example_tables(cleaned_answer)
    suspect_features = verify_feature_claims(cleaned_answer)
    cleaned_answer = expand_corpus_examples(cleaned_answer)


    if suspect_phrases or suspect_features or unverifiable_corpus:
        warning = "\n\n---\n**⚠ Verification warning:** the following could not be confirmed and may be inaccurate:\n"
        for phrase in suspect_phrases:
            warning += f"- example: \"{phrase}\"\n"
        for feature in suspect_features:
            warning += f"- feature value: \"{feature}\"\n"
        for item in unverifiable_corpus:
            warning += f"- corpus citation could not be verified: {item}\n"
        cleaned_answer += warning

    yield cleaned_answer, ""


# ============================================================
# UI HELPERS
# ============================================================

def clear_conversation():
    return "*No messages yet.*"


# ============================================================
# UI
# ============================================================

with gr.Blocks(title="MPCD Annotation Assistant") as view:

    gr.Markdown(
        """
        # MPCD Annotation Assistant
        """
    )

    conversation_display = gr.Markdown(
        value="*No messages yet.*",
        label="Answer"
    )

    message_input = gr.Textbox(
        label="Your message:",
        placeholder="Ask a question about syntax or morphology...",
        lines=5
    )

    with gr.Row():
        send_button = gr.Button("Send", variant="primary")
        clear_button = gr.Button("Clear")
        logout_button = gr.Button("Logout")

    send_button.click(
        fn=message_gpt,
        inputs=[message_input],
        outputs=[conversation_display, message_input]
    )

    message_input.submit(
        fn=message_gpt,
        inputs=[message_input],
        outputs=[conversation_display, message_input]
    )

    clear_button.click(
        fn=clear_conversation,
        inputs=None,
        outputs=[conversation_display]
    )

    logout_button.click(
        fn=None,
        inputs=None,
        outputs=None,
        js="() => { window.location.href = '/logout'; }"
    )


# ============================================================
# SERVER
# ============================================================

view.launch(
)
