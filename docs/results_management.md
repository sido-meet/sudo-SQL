# Results Management Strategy

This document outlines the strategy for managing inference results in the `sudo-SQL` project.

## Philosophy

Logging is used for diagnostics and monitoring the *process*, not for storing the *output*. A dedicated results management strategy is essential for evaluation, analysis, and sharing.

## Core Components

### Output Directory

- A new top-level directory, `results/`, is created at the project root.
- This directory is added to `.gitignore` as it contains generated artifacts.

### File Format: JSON Lines (`.jsonl`)

- Each inference result (one per question) is saved as a single JSON object on its own line in the output file.
- This format is ideal for append-style writing, is highly structured, and is easily parsed by other tools.

**Example of a single line in the `.jsonl` file:**
```json
{"db_id": "concert_singer", "question": "How many singers are there?", "generated_sql": "SELECT count(*) FROM singer", "ground_truth_sql": "SELECT count(*) FROM singer"}
```

### File Naming Convention

- To ensure traceability and support for resuming jobs, filenames are generated based on the `save_mode`.
- **`overwrite` or `append` mode**: `{dataset_name}_{split}_{model_name}_{timestamp}.jsonl`
    - **Example**: `spider_dev_Qwen2.5-3B-Instruct_20250731-153000.jsonl`
- **`resume` mode**: `{dataset_name}_{split}_{model_name}.jsonl` (deterministic)
    - **Example**: `spider_dev_Qwen2.5-3B-Instruct.jsonl`

## Configuration

A new `output` section is added to the `inference` configuration in `configs/infer.yaml`.

**Example `configs/infer.yaml`:**
```yaml
mode: infer
# ... model config ...
inference:
  # ... dataset config ...
  output:
    save_path: "results/"
    save_mode: "resume" # Options: "overwrite", "append", "resume"
```

- **`save_path`**: The directory where the results file will be saved.
- **`save_mode`**:
    - `overwrite` (Default): Creates a new timestamped file for each run. If a file with the exact same name were to exist, it would be overwritten.
    - `append`: Creates a new timestamped file and appends to it if it exists.
    - `resume`: Uses a deterministic filename. If the file exists, it reads the contents to skip already processed questions and resumes where it left off.