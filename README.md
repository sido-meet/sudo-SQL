# sudo-SQL: A Unified Text-to-SQL Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**`sudo-SQL`** is an end-to-end, modular framework for building, training, and running state-of-the-art Text-to-SQL models. It provides a unified pipeline for Supervised Fine-Tuning (SFT), Reinforcement Learning (RL), and high-performance Inference, with a strong emphasis on robust architecture and developer experience.

This project is the second stage of a larger vision, building upon the schema generation capabilities of its sibling project, [D-Schema](https://github.com/sido-meet/D-Schema).

## Key Features

-   **Modular Pipeline Architecture**: Uses a Strategy Pattern to cleanly separate the logic for different modes of operation (`sft`, `rl`, `infer`), making the system easy to maintain and extend.
-   **Extensible Data Loading**: A dedicated data loader module with a factory pattern supports multiple datasets (e.g., Spider, BIRD) out of the box.
-   **Efficient Schema Caching**: An intelligent, timestamp-based caching system for database schemas drastically speeds up data loading by avoiding redundant generation.
-   **Robust Logging**: A centralized logging system using `Loguru` provides structured, leveled, and persistent logs for both console monitoring and deep debugging.
-   **Resumable Inference**: A fault-tolerant results management system allows inference jobs to be paused and resumed, saving progress and preventing data loss.
-   **Flexible Configuration**: All operations are driven by clear, simple YAML configuration files.

## Getting Started

### Prerequisites

-   Python 3.11+
-   `uv` (for environment and package management)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sido-meet/sudo-SQL.git
    cd sudo-SQL
    ```

2.  **Create the virtual environment:**
    ```bash
    uv venv
    ```

3.  **Activate the environment:**
    ```bash
    source .venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    uv pip install -e .
    ```

## Usage

All operations are run through `main.py` using the `infer` or `train` commands, which are configured via a YAML file.

### Inference

To run inference on a dataset, use the `infer` command with a configuration file.

```bash
uv run main.py infer --config configs/infer.yaml
```

An example `infer.yaml`:
```yaml
mode: infer

model:
  provider: "openai"
  name: "Qwen2.5-3B-Instruct"
  base_url: "http://localhost:8192/v1"

inference:
  dataset_name: "spider"
  data_path: "./data/spider"
  split: "dev"
  schema_type: "ddl-schema"
  use_cache: true

  output:
    save_path: "results/"
    save_mode: "resume" # Options: overwrite, append, resume
```

### Training

To run training (SFT or RL), use the `train` command with the appropriate configuration file.

```bash
# Supervised Fine-Tuning (SFT)
uv run main.py train --config configs/sft.yaml

# Reinforcement Learning (RL)
uv run main.py train --config configs/rl.yaml
```

## Project Structure

The project is organized into a modular and maintainable structure:

```
/sudo-SQL/
├───configs/              # YAML configuration files for different modes.
├───data/                 # Raw data for training and evaluation.
├───docs/                 # Project architecture and strategy documentation.
├───logs/                 # Persistent log files.
├───results/              # Structured inference output files (.jsonl).
├───sudo_sql/
│   ├───data_loaders/     # Modular system for loading different datasets.
│   ├───environments/     # RL environments.
│   ├───models/           # Model provider integrations.
│   ├───pipeline/         # Core pipeline logic (Strategy Pattern).
│   └───logger_config.py  # Centralized Loguru configuration.
├───tests/                # Test suite.
├───main.py               # Main CLI entry point (Typer).
└───README.md             # This file.
```

## Documentation

For more detailed information on the project's architecture and design decisions, please see the documents in the `docs/` directory:

-   `docs/pipeline_architecture.md`
-   `docs/logging_strategy.md`
-   `docs/results_management.md`

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.