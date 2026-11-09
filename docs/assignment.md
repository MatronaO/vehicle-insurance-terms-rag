# Homework Assignment 2

Block 2 case — “RAG on Your Own Data + Evals”

## Goal

Build a complete RAG workflow using your course project’s document corpus: from raw documents to answers with source references. Answer quality must be checked by an automated evaluation pipeline that runs in CI.

```text
documents (PDF / DOCX / HTML) → cleaning → chunks + metadata → vector database (hybrid search + reranking) → model answer with sources → evals in CI
```

This is the second stage of the same course project you worked on in Block 1. The agent in Block 3 will use the corpus from this assignment.

## Steps

Each step builds on the corresponding lesson. Complete them in order: each step uses the results of the previous one.

### Step 1. Corpus and chunking (Lesson 6, approximately 4 hours)

- Collect a corpus for your project: **at least 30 documents in at least 2 formats** (PDF, DOCX, HTML, Markdown). Public documents from your subject area are suitable. No personal data.
- Write an ingestion pipeline that includes:
  - text extraction that preserves structure (headings, lists, tables);
  - cleaning and normalization (headers and footers, line breaks, encoding, HTML boilerplate);
  - deduplication using a content hash; optionally, detection of near-duplicates.
- Choose a chunking strategy and **justify your choice** in the README: explain why the chunk size and splitting method suit your documents. Compare your strategy with fixed-size chunking on at least a few documents.
- Add metadata to every chunk: source, title, section, date or version, and document hash.
- Output: a file containing the chunks, such as `chunks.jsonl`, and a manifest.

Use the Lesson 6 exercise (`lesson-06-data-ingestion`) as a starting point. You can adapt your solution to your own corpus.

### Step 2. Index and hybrid search (Lesson 7, approximately 4 hours)

- Generate embeddings for the chunks using a provider-hosted or local model, and store them in a vector database (Qdrant, Chroma, FAISS, or an equivalent).
- Implement **hybrid search**: lexical search (BM25) + vector search, combining their results.
- Add **reranking and metadata filters**, for example, by date, document type, or access group.
- **Measure retrieval quality:** use 10–15 questions for which you know the correct chunk, and measure recall@k or MRR. Compare at least two configurations: vector search only / hybrid search / hybrid search + reranking.

### Step 3. RAG with sources (Lesson 8, approximately 4 hours)

- The model’s answer must be based only on the retrieved chunks and **cite sources** (document and section) for every claim.
- **Context control:** set a token budget for the context. If there is no relevant information, the system must answer “I don’t know” / “This information is not in the documents” instead of making things up.
- Store prompts in files with versions and a changelog, as in Block 1.

### Step 4. Test set and evals in CI (Lesson 9, approximately 4 hours)

- Create a **test set of at least 20 questions**, with expected answers and sources. You must include questions that have **no answer in the corpus**, as well as trap questions involving similar documents or outdated versions.
- Implement **scoring functions**:
  - deterministic checks wherever possible: the correct source is cited, key facts are present, and “I don’t know” is returned when appropriate;
  - LLM-as-a-judge for the remaining checks, **with calibration**: test the judge on at least 10 answers that you have scored manually, and report how closely its assessments agree with yours;
  - a **faithfulness** check: whether every claim in the answer is supported by the context.
- Run the evals in **CI** (GitHub Actions or an equivalent) on every push or pull request. Set a threshold below which the run fails.
- Write a short report, `REPORT.md`, containing a table of retrieval and answer metrics, an analysis of 3–5 typical errors (what should have happened → what actually happened → why), and what you would improve next.

> **Stretch tasks** (no points; only if you have time left): semantic or parent-child chunking with a comparison; contextual chunk headers; incremental ingestion; embedding caching.

## Dates

| When | What |
| --- | --- |
| After Lesson 8 | Checkpoint: Steps 1–2 in the repository, with a link posted in the cohort chat (no points) |
| Lesson 10 (Q&A) | Feedback on the checkpoint |
| The day after the Q&A, 13 November at 23:59 | Deadline: Steps 1–4 |

## Grading criteria (40 points)

| Step | Item | Points |
| --- | --- | ---: |
| 1. Corpus and chunking | Ingestion of at least 2 formats (PDF / DOCX / HTML) | 3 |
| | Cleaning + deduplication (content hash or embeddings) | 3 |
| | Justified chunking strategy + metadata | 4 |
| 2. Index and search | Embeddings + vector database | 3 |
| | Hybrid search (lexical + vector) | 3 |
| | Reranking and metadata filters | 2 |
| | Retrieval quality measured (recall@k / MRR or an equivalent) | 2 |
| 3. RAG with sources | Answers with source citations | 4 |
| | Context control: token budget, “I don’t know” when there is no data | 4 |
| 4. Evals in CI | Test set of at least 20 questions with expected answers | 3 |
| | Scoring functions: deterministic checks + LLM-as-a-judge with calibration + faithfulness | 4 |
| | Evals run in CI | 3 |
| Repository | README, one-command execution, no keys in the code | 2 |

The most points are awarded for justified chunking, sources, “I don’t know,” and scoring functions, because these are the areas where RAG systems fail most often.

## Common mistakes (points are deducted for these)

- Fixed-length chunking “because that’s what the tutorial used,” without justification or comparison.
- No “I don’t know” response → the model makes things up when the corpus contains no answer.
- LLM-as-a-judge without validation against manual labels: there is no way to know whether the judge is correct.
- A test set generated by AI from the same documents, without anyone checking it.
- Retrieval quality is not measured: “It seems to find things.”

## Not required

UI, deployment, fine-tuning, a large corpus (30–100 documents are enough), or perfect accuracy.

## Technical requirements

- Python 3.10+, with one-command execution (`make run` or `python main.py`).
- Any provider-hosted or local model for answers and embeddings. If a model is paid, state the cost per 1,000 questions.
- Store keys only in `.env`; include only `.env.example` in the repository.
- Submission: one link to a public GitHub repository.

## What must be in the repository

- Code for ingestion, indexing, RAG, and evals.
- `data/`: the corpus, or a script that downloads it if the documents are large or subject to licensing restrictions, plus a manifest.
- `prompts/`: prompts with versions and a changelog.
- `evals/`: the test set, scoring functions, and run results.
- `.github/workflows/` or an equivalent: the workflow that runs the evals.
- `REPORT.md`: metrics, error analysis, and conclusions.
- `README.md`: what the project is, how to run it, and the justification for the chunking strategy.
