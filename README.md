# Cortex

A local-first pipeline that turns messy, hand-typed meeting notes into a structured, searchable knowledgebase — no audio recording, no cloud calls. Built for environments where recording meetings isn't allowed.

## Why

Taking useful notes live is hard, and notes that never get reviewed are worthless. Cortex makes capture nearly frictionless (short fragments during the meeting + a fast unstructured brain-dump right after), then uses a local LLM to turn that into a structured note, and embeds it so you can later ask questions like *"what did we decide about the API latency fix?"*

Everything runs locally. No meeting content ever leaves the machine.

## Architecture

```
Capture (Textual TUI)
   → Structuring (Gemma 4:e2b GGUF via llama-cpp-python, in-process)
   → Embedding (multilingual-e5-small)
   → Storage (LanceDB)
   → Query time: retrieve → rerank (bge-reranker-v2-m3) → answer (Gemma 4:e2b)
```

| Stage | Tool / Model | Purpose |
|---|---|---|
| Capture | [Textual](https://textual.textualize.io/) | Fast fragment logging during meetings + post-meeting brain dump |
| Structuring | Gemma 4:e2b (GGUF, via `llama-cpp-python`) | Turn raw fragments into a structured note (summary, decisions, action items, open questions) |
| Embedding | `intfloat/multilingual-e5-small` | Embed note chunks (EN/DE support) |
| Storage | [LanceDB](https://lancedb.github.io/lancedb/) | Embedded, disk-based vector store |
| Retrieval | LanceDB top-k search | Cheap broad retrieval (k≈15–20) |
| Reranking | `bge-reranker-v2-m3` | Cross-encoder rerank down to top 3–5 chunks |
| Answering | Gemma 4:e2b / E4B (GGUF) | Generate final answer from reranked context |

**No Ollama, no background service.** The LLM runs in-process via `llama-cpp-python`, a plain pip package — no admin rights, no daemon, no unsigned executable.

## Project structure

```
cortex/
├── config/           # config.yaml — all model paths & params, nothing hardcoded in src/
├── model/            # GGUF weights (gitignored) — populate via scripts/download_model.sh
├── data/
│   ├── raw/          # raw captures from the Textual app (gitignored)
│   └── lancedb/      # vector store (gitignored)
├── scripts/          # CLI entry points — run these, don't run src/ modules directly
│   ├── download_model.sh
│   ├── run_capture.py
│   ├── run_ingest.py
│   └── run_query.py
├── src/
│   └── cortex/
│       ├── settings.py     # loads config/config.yaml
│       ├── capture/        # Textual screens
│       ├── pipeline/       # structuring, chunking, embedding
│       ├── storage/        # LanceDB wrapper
│       └── query/          # retrieve, rerank, answer
├── tests/
├── pyproject.toml
└── README.md
```

## Setup

### Prerequisites
- Python 3.11+
- `uv` (recommended) or `pip`/`conda`
- No Ollama, no admin rights needed — the LLM runs via `llama-cpp-python`, a plain pip package

### Install

```bash
git clone https://github.com/<your-username>/cortex.git
cd cortex
uv venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
uv pip install -e ".[dev]"
```

**Work environment (conda-only, no uv):** the dependency spec lives in `pyproject.toml`, which is standard — conda envs can install it via plain `pip`, no uv required.

```bash
conda create -n cortex python=3.11
conda activate cortex
pip install -e ".[dev]"
```

### Download the model

```bash
bash scripts/download_model.sh
```

Downloads the GGUF weights into `model/`. Edit `config/config.yaml` if you want a different quantization or model size (e.g. E4B for better quality at the cost of speed).

### Run

```bash
# Capture screen (during/after meetings)
python scripts/run_capture.py

# Ingest + structure a raw capture into the knowledgebase
python scripts/run_ingest.py --input data/raw/<file>.json

# Query the knowledgebase
python scripts/run_query.py "what did we decide about the API latency fix?"
```

## Project status

Early development. See [Roadmap](#roadmap) below.

## Roadmap

- [ ] v0.1 — Capture TUI: quick-fragment screen + brain-dump screen, saves raw JSON to `data/raw/`
- [ ] v0.2 — Structuring pipeline: raw capture → structured note via local LLM
- [ ] v0.3 — Chunking + embedding + LanceDB ingestion
- [ ] v0.4 — Retrieval + reranking
- [ ] v0.5 — Query/chat script, end-to-end working
- [ ] v0.6 — Polish: error handling, packaging

## A note on data handling

Cortex is built for a workplace where meeting recording isn't permitted. It only ever processes notes you've manually typed — it does not capture audio, screens, or any other meeting content automatically. `data/raw/`, `data/lancedb/`, and `model/` are all gitignored; never commit real meeting notes or weights to this repo. Treat any published version of this repo as containing **code only**, not your actual notes.

## License

MIT — see `LICENSE`.
