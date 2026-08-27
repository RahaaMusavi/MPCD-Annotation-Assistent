import os
import pandas as pd
from tqdm.notebook import tqdm
from conllu import parse
from conllu.parser import DEFAULT_FIELD_PARSERS
from collections.abc import Mapping


class Token:
    def __init__(self, token_data):
        try:
            original_id = token_data.get('id')
            self.id = int(float(original_id)) if original_id is not None else None
        except (ValueError, TypeError):
            self.id = token_data.get('id')

        self.form = token_data.get('form')
        self.lemma = token_data.get('lemma')
        self.upos = token_data.get('upos')
        self.xpos = token_data.get('xpos')
        self.feats = token_data.get('feats')

        try:
            original_head = token_data.get('head')
            self.head = int(float(original_head)) if original_head is not None else None
        except (ValueError, TypeError):
            self.head = token_data.get('head')

        self.deprel = token_data.get('deprel')
        self.deps = token_data.get('deps')
        self.misc = token_data.get('misc')

        self.misc_dict = self.misc if isinstance(self.misc, dict) else {}
        self.sense = self.misc_dict.get('sense', "_")
        self.transliteration = self.misc_dict.get('transliteration', '_')

    def __repr__(self):
        return f"Token({self.id}: {self.form})"


STRUCTURAL_KEYS = {"chapter", "section", "subsection", "unit", "part"}

# any of these header keys mark the start of a NEW sentence, independent
# of whether chapter/section metadata changed (fixes sentences silently
# merging together when several consecutive sentences share the same
# chapter/section)
SENTENCE_ID_KEYS = {"sentence id", "sent_id", "sentence_id", "sentenceid"}

class Sentence:
    def __init__(self, sentence_token_list, source_filename):
        self.metadata = sentence_token_list.metadata
        self.sentence_id = self.metadata.get('sent_id')
        self.text = self.metadata.get('text')
        self.file_name = source_filename
        self._tokens = [Token(t) for t in sentence_token_list]

        # structural hierarchy fields written by _write_conllu_block
        for key in STRUCTURAL_KEYS:
            setattr(self, key, self.metadata.get(key))

    def get_tokens(self):
        return self._tokens

    def get_translations(self):
        return [v for k, v in self.metadata.items() if k.startswith('translation')]

    def __repr__(self):
        return f"Sentence(id={self.sentence_id}, tokens={len(self._tokens)})"


def _sanitize_field(text):
    if text is None or str(text).strip() in ["", "nan", "None"]:
        return "_"
    return str(text).replace('\t', ' ').replace('\n', ' ').strip()


def _sanitize_misc_value(text):
    """
    Same as _sanitize_field, but additionally escapes '|', since '|' is
    the separator between different MISC fields once they are joined
    together. Without this, a cell value that itself contains '|' (e.g.
    a newpart column holding 'chapter:X|section:Y' as one string) would
    split apart into a malformed, key-less fragment when written out.
    """
    val = _sanitize_field(text)
    if val == "_":
        return val
    return val.replace("|", ";")


def _sanitize_head(val):
    if val is None or str(val).strip() in ["", "_", "nan", "None"]:
        return "_"
    val_str = str(val).strip()
    if "|" in val_str:
        val_str = val_str.split("|")[0]
    try:
        return str(int(float(val_str)))
    except (ValueError, TypeError):
        return "_"


def _detect_misc_fields(df):
    core_fields = {'id', 'transcription', 'lemma', 'postag', 'postfeatures', 'head', 'deprel', 'deps'}
    return [col for col in df.columns if col.lower() not in core_fields]


def _parse_structural_pairs(raw_value):
    """
    Parse chapter/section/etc. markers out of a per-token structural
    column, e.g. a newpart cell holding 'chapter:AŌD 1|section:AŌD 1.1'.

    Only keys listed in STRUCTURAL_KEYS are kept; anything else in the
    cell is ignored. Returns an empty dict if nothing recognisable is
    found (e.g. the cell is empty, or holds unrelated annotation).
    """
    pairs = {}
    if raw_value is None:
        return pairs

    raw_value = str(raw_value).strip()
    if raw_value in ("", "_", "nan", "None"):
        return pairs

    for part in raw_value.split("|"):
        part = part.strip()
        if ":" not in part:
            continue
        key, val = part.split(":", 1)
        key = key.strip().lower()
        val = val.strip()
        if key in STRUCTURAL_KEYS:
            pairs[key] = val

    return pairs


def _write_conllu_block(f, sent_idx, tokens, translations, comment, structural_meta=None):
    f.write(f"# sent_id = {sent_idx}\n")
    f.write(f"# text = {' '.join(t[1] for t in tokens)}\n")

    if not translations:
        f.write("# translation = _\n")
    else:
        for i, trans in enumerate(translations):
            key = "translation" if len(translations) == 1 else f"translation_{i+1}"
            f.write(f"# {key} = {trans}\n")

    if structural_meta:
        for k, v in structural_meta.items():
            f.write(f"# {k} = {v}\n")

    if comment:
        f.write(f"# comment = {comment}\n")

    for t in tokens:
        f.write("\t".join(t) + "\n")

    f.write("\n")


def _convert_csv_to_conllu(csv_file_path, output_dir):
    try:
        ext = os.path.splitext(csv_file_path)[1].lower()
        if ext in ['.xlsx', '.xls']:
            df = pd.read_excel(csv_file_path, dtype=str, keep_default_na=False, engine='openpyxl')
        else:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                sample = f.read(4096)
                sep = '\t' if sample.count('\t') >= sample.count(',') else ','
            df = pd.read_csv(csv_file_path, sep=sep, dtype=str, keep_default_na=False,
                             encoding='utf-8', engine='python', on_bad_lines='skip')

        id_col = next((c for c in df.columns if c.lower() == 'id'), 'id')
        base_name = os.path.splitext(os.path.basename(csv_file_path))[0]
        output_file_path = os.path.join(output_dir, f"{base_name}.conllu")
        misc_fields = _detect_misc_fields(df)

        # column holding per-token structural markers (chapter/section/etc.),
        # if the source file records them this way instead of via '#' rows
        structural_col = next((c for c in df.columns if c.lower() == 'newpart'), None)

        with open(output_file_path, 'w', encoding='utf-8') as f:
            current_tokens = []
            current_translations = []
            current_comment = None

            # hierarchical context (chapter/section/subsection/etc.)
            current_meta = {}

            # tracks the current explicit sentence marker (e.g. "#sentence_id = 32")
            # and the last token id seen, so a sentence boundary is detected even
            # when chapter/section metadata stays the same across sentences
            current_sentence_marker = None
            last_token_id = None

            sent_counter = 1

            for _, row in df.iterrows():
                raw_id = str(row.get(id_col, '')).strip()

                # =========================
                # 1. METADATA HANDLING
                # =========================
                if raw_id.startswith('#'):
                    # robust, format-agnostic check: ANY row that mentions a
                    # sentence-id marker starts a new sentence, regardless of
                    # exact spacing/casing/separator around it (does not rely
                    # on the header parsing cleanly into key/val below)
                    upper_raw = raw_id.upper()
                    if ("SENTENCE ID" in upper_raw or "SENT_ID" in upper_raw
                            or "SENT ID" in upper_raw or "SENTENCE_ID" in upper_raw):
                        if current_tokens:
                            _write_conllu_block(
                                f,
                                sent_counter,
                                current_tokens,
                                current_translations,
                                current_comment,
                                structural_meta=dict(current_meta),
                            )
                            current_tokens, current_translations, current_comment = [], [], None
                            sent_counter += 1
                        current_sentence_marker = raw_id
                        continue

                    header = raw_id[1:].strip()

                    # support both ":" and "=" formats
                    if ":" in header:
                        key, val = header.split(":", 1)
                    elif "=" in header:
                        key, val = header.split("=", 1)
                    else:
                        continue

                    key = key.strip().lower()
                    val = val.strip()

                    # any structural hierarchy key triggers a boundary on change
                    if key in STRUCTURAL_KEYS:
                        if current_meta.get(key) != val and current_tokens:
                            _write_conllu_block(
                                f,
                                sent_counter,
                                current_tokens,
                                current_translations,
                                current_comment,
                                structural_meta=dict(current_meta),
                            )
                            current_tokens, current_translations, current_comment = [], [], None
                            sent_counter += 1

                        current_meta[key] = val
                        continue

                    # an explicit sentence-id marker always starts a new sentence
                    # on change, even if chapter/section metadata is unchanged
                    if key in SENTENCE_ID_KEYS:
                        if (current_sentence_marker is not None
                                and val != current_sentence_marker
                                and current_tokens):
                            _write_conllu_block(
                                f,
                                sent_counter,
                                current_tokens,
                                current_translations,
                                current_comment,
                                structural_meta=dict(current_meta),
                            )
                            current_tokens, current_translations, current_comment = [], [], None
                            sent_counter += 1

                        current_sentence_marker = val
                        continue

                    # non-structural metadata
                    if key.startswith("translation"):
                        current_translations.append(val)
                    elif key == "comment":
                        current_comment = val

                    continue

                # =========================
                # 2. NORMAL TOKEN ROW
                # =========================
                try:
                    norm_id = str(int(float(raw_id)))
                except:
                    norm_id = raw_id

                if norm_id in ["", "_", "nan"]:
                    continue

                # backstop: if the token id resets (e.g. back down to 1) while
                # tokens are already accumulating, a new sentence has begun --
                # catches this even if no explicit sentence-id marker is present
                try:
                    norm_id_int = int(norm_id)
                except (ValueError, TypeError):
                    norm_id_int = None

                if (norm_id_int is not None and last_token_id is not None
                        and norm_id_int <= last_token_id and current_tokens):
                    _write_conllu_block(
                        f,
                        sent_counter,
                        current_tokens,
                        current_translations,
                        current_comment,
                        structural_meta=dict(current_meta),
                    )
                    current_tokens, current_translations, current_comment = [], [], None
                    sent_counter += 1
                    current_sentence_marker = None

                if norm_id_int is not None:
                    last_token_id = norm_id_int

                # some source files carry chapter/section markers on every
                # token row (e.g. a 'newpart' column) instead of dedicated
                # '#' rows; treat a change here the same way as above
                if structural_col:
                    token_structural = _parse_structural_pairs(row.get(structural_col))
                    changed = {k: v for k, v in token_structural.items() if current_meta.get(k) != v}

                    if changed and current_tokens:
                        _write_conllu_block(
                            f,
                            sent_counter,
                            current_tokens,
                            current_translations,
                            current_comment,
                            structural_meta=dict(current_meta),
                        )
                        current_tokens, current_translations, current_comment = [], [], None
                        sent_counter += 1

                    current_meta.update(token_structural)

                token_line = [
                    norm_id,
                    _sanitize_field(row.get('transcription')),
                    _sanitize_field(row.get('lemma')),
                    _sanitize_field(row.get('postag')),
                    "_",
                    _sanitize_field(row.get('postfeatures')),
                    _sanitize_head(row.get('head')),
                    _sanitize_field(row.get('deprel')),
                    _sanitize_field(row.get('deps')),
                    "_"
                ]

                misc_parts = []
                for field in misc_fields:
                    val = _sanitize_misc_value(row.get(field))
                    if val != "_":
                        misc_parts.append(f"{field}={val}")

                token_line[9] = "|".join(misc_parts) if misc_parts else "_"

                current_tokens.append(token_line)

            # =========================
            # FINAL FLUSH
            # =========================
            if current_tokens:
                _write_conllu_block(
                    f,
                    sent_counter,
                    current_tokens,
                    current_translations,
                    current_comment,
                    structural_meta=dict(current_meta),
                )

    except Exception as e:
        print(f"Error processing {csv_file_path}: {e}")


def parse_corpus(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(('.csv', '.tsv', '.xlsx'))
        and "outdated" not in f.lower()
    ]

    if not files:
        print(f"Warning: No valid files found in {input_folder}")
    else:
        for f in tqdm(files, desc="Converting files"):
            _convert_csv_to_conllu(os.path.join(input_folder, f), output_folder)

    custom_field_parsers = DEFAULT_FIELD_PARSERS.copy()
    custom_field_parsers['id'] = lambda line, i: line[i]
    custom_field_parsers['head'] = lambda line, i: line[i]

    all_sentences = []
    conllu_files = [f for f in os.listdir(output_folder) if f.lower().endswith('.conllu')]

    for cf in tqdm(conllu_files, desc="Loading CoNLL-U"):
        file_path = os.path.join(output_folder, cf)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                continue

            parsed_data = parse(content, field_parsers=custom_field_parsers)
            for s in parsed_data:
                all_sentences.append(Sentence(s, cf))

    print(f"\n--- Pipeline Complete: Loaded {len(all_sentences)} sentences ---")
    return all_sentences
