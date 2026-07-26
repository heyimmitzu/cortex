#!/usr/bin/env bash
# Downloads the Gemma 3n GGUF weights into model/.
# Adjust REPO/FILENAME to whichever quantization you pick from Hugging Face
# (e.g. unsloth or bartowski's GGUF quant repos).

set -euo pipefail

REPO="unsloth/gemma-3n-E2B-it-GGUF"
FILENAME="gemma-3n-E2B-it-Q4_K_M.gguf"

mkdir -p model
huggingface-cli download "$REPO" "$FILENAME" --local-dir model

echo "Downloaded $FILENAME to model/"
echo "Make sure config/config.yaml -> llm.structuring_model matches this filename."
