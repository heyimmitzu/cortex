"""Entry point: take a raw capture (data/raw/<file>.json), structure it via the local LLM,
chunk + embed it, and write it into LanceDB.

Usage:
    python scripts/run_ingest.py --input data/raw/2026-07-26_standup.json
"""

import argparse

from cortex.pipeline.chunk import chunk_note
from cortex.pipeline.embed import embed_chunks
from cortex.pipeline.structure import structure_capture
from cortex.storage.db import write_chunks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to a raw capture JSON file")
    args = parser.parse_args()

    structured_note = structure_capture(args.input)
    chunks = chunk_note(structured_note)
    embedded = embed_chunks(chunks)
    write_chunks(embedded)


if __name__ == "__main__":
    main()
