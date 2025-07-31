# sudo-SQL: A Unified Text-to-SQL Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**`sudo-SQL`** is an end-to-end, `verl`-native framework for building and training state-of-the-art Text-to-SQL models. Inspired by the flexibility and power of [verl](https://github.com/volcengine/verl), this project provides a single, unified pipeline for Supervised Fine-Tuning (SFT), Reinforcement Learning (RL), and high-performance Inference.

This project is the second stage of a larger vision, building upon the schema generation capabilities of its sibling project, [D-Schema](https://github.com/sido-meet/D-Schema).

## Core Philosophy: A Unified Pipeline

The `sudo-SQL` framework is designed around a central principle: **unification**. By leveraging `verl` for all core operations, we eliminate the need for separate scripts and workflows for training and inference. This results in a more robust, maintainable, and powerful codebase.

## Key Features

-   **`verl`-Native**: Built from the ground up to leverage the full power of the `verl` library.
-   **Unified Pipeline**: A single, configurable pipeline for SFT, RL, and Inference.
-   **Flexible RL Environments**:
    -   `SFTEnvironment`: A specialized `verl` environment for Supervised Fine-Tuning, which rewards the model for generating correct SQL queries from a dataset.
    -   `SQLExecutionEnvironment`: A `verl` environment for Reinforcement Learning, which provides feedback by executing generated SQL against a live database.
-   **Dynamic Model Support**: Easily integrate and switch between different language models (e.g., OpenAI, Hugging Face).
-   **Clear & Modular Structure**: A redesigned file structure that reflects the unified `verl` architecture.

## New File Structure

The project will be reorganized to reflect the new, unified `verl`-based approach:

```
/home/sido/projects/sudo-SQL/
├───.gitignore
├───main.py                 # Main CLI entry point for all operations
├───pyproject.toml
├───README.md               # This file
├───configs/
│   ├───models.yaml         # Model provider configurations
│   ├───sft.yaml            # Example config for an SFT run
│   └───rl.yaml             # Example config for an RL run
├───data/                   # Training and evaluation data
├───schemas/                # Generated database schemas
└───sudo_sql/
    ├───__init__.py
    ├───pipeline.py           # The core unified `verl` pipeline
    ├───environments/
    │   ├───__init__.py
    │   ├───base.py             # Base environment class
    │   ├───sft.py              # SFTEnvironment
    │   └───sql_execution.py    # SQLExecutionEnvironment
    └───models/
        ├───__init__.py
        ├───base.py
        ├───huggingface.py
        └───openai.py
```

## Execution Plan

The refactoring will be executed in the following phases:

1.  **Phase 1: Project Restructuring**: Create the new directory structure, move existing files, and remove obsolete ones.
2.  **Phase 2: Environment Implementation**:
    -   Create a `BaseEnvironment` class.
    -   Implement `SFTEnvironment` for Supervised Fine-Tuning.
    -   Refactor the existing `SQLExecutionEnvironment` to fit the new structure.
3.  **Phase 3: Unified Pipeline Implementation**:
    -   Create `sudo_sql/pipeline.py`, which will contain the core logic for running SFT, RL, and Inference using the `verl` framework based on a configuration file.
4.  **Phase 4: CLI Entry Point**:
    -   Refactor `main.py` to be a clean command-line interface that parses a configuration and calls the unified pipeline.
5.  **Phase 5: Documentation & Testing**:
    -   Update all documentation and add comprehensive tests for the new pipeline.

## Usage (Post-Refactoring)

Once the refactoring is complete, all operations will be run through `main.py` with a configuration file.

**Supervised Fine-Tuning (SFT):**
```bash
python main.py train --config configs/sft.yaml
```

**Reinforcement Learning (RL):**
```bash
python main.py train --config configs/rl.yaml
```

**Inference:**
```bash
python main.py infer --model "openai_gpt4" --question "How many users are there?" --schema "CREATE TABLE users (id INT, name TEXT);"
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.
