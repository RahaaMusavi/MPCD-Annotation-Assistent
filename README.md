# MPCD Annotation Assistant

A AI-assistent research tool to help annotate Middle Persian Corpus according to the Universal Dependencies rules..

The application combines an annotated corpus with syntax and morphology handbooks and allows questions to be answered through retrieval from these materials. 
It uses the OpenAI API and a Gradio interface.

## What it does

* retrieves relevant passages from the reference materials;
* answers questions about syntax and morphology;
* provides corpus examples where available;
* checks generated examples against the source material;
* checks corpus token citations against the annotated corpus;
* retrieves the full sentence context for cited corpus tokens;
* flags examples or feature claims that cannot be verified.

The verification steps are separate from the model output. They are intended to reduce unsupported examples and incorrect corpus references.

## Data

The repository does not contain the research corpus or private source materials.

The application expects the following files:

* syntax handbook
* morphology handbook
* UD principles
* annotated corpus
* corpus export used for retrieval

The paths to these files have to be configured locally.

## Requirements

* Python 3
* OpenAI API access
* `openai`
* `gradio`

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

Set the OpenAI API key as an environment variable before running the application:

```bash
OPENAI_API_KEY=your_api_key
```

## Running

After the source files have been configured:

```bash
python app.py
```

The application starts a Gradio interface.

On the first run, the source files are uploaded to an OpenAI vector store. A local cache is then used so that the vector store does not have to be recreated when the source files have not changed.

## Verification

The application does not rely only on the model's output for corpus evidence.

For corpus examples, it checks whether the relevant forms and relations can be found in the annotated corpus. It also retrieves sentence-level information directly from the corpus, including the surface text, translation, token information, and file name.

Generated examples and morphological feature claims are checked against the available source text. Items that cannot be confirmed are marked with a verification warning.

## Status

This is a research prototype developed for work on Middle Persian syntax and morphology. It is intended primarily as a research and documentation tool rather than as a general-purpose annotation system.
