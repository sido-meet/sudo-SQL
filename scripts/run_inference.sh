#!/bin/bash

# This script runs the inference pipeline.

set -e

# --- Configuration ---
INFER_CONFIG="configs/infer.yaml"

# --- Main Logic ---
echo "--- Running Inference ---"
uv run main.py infer --config "$INFER_CONFIG"
echo "--- Inference finished successfully ---"
