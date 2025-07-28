# sudo-SQL: Your Extensible Text-to-SQL Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced, modular, and extensible framework designed to bridge the gap between natural language and SQL databases. `sudo-SQL` focuses on leveraging Large Language Models (LLMs) for high-accuracy Text-to-SQL generation, training, and deployment.

This project is the second stage of a larger vision, building upon the schema generation capabilities of its sibling project, [D-Schema](https://github.com/sido-meet/D-Schema).

## Core Features

-   **Multi-Model Support**: Pluggable architecture to easily integrate with various LLMs. Configure models centrally in `configs/models.yaml`.
-   **Advanced Inference Strategies**:
    -   **Multi-model Voting**: Enhance accuracy by polling multiple LLMs and choosing the most common response.
    -   **Critic Agent**: A secondary agent that reviews, validates, and corrects generated SQL for higher precision.
-   **Flexible Training Pipelines**:
    -   **Supervised Fine-Tuning (SFT)**: Adapt models to specific database schemas or question styles using Hugging Face `trl` and `peft` for LoRA.
    -   **Reinforcement Learning (RL) with `verl`**: Further refine models based on direct feedback from a live database environment.
-   **Efficient Training Techniques**: Full support for parameter-efficient fine-tuning (PEFT) via LoRA to reduce computational costs.

## Getting Started

### 1. Installation

First, clone the repository and install the required dependencies using `uv`.

```bash
git clone https://github.com/sido-meet/sudo-SQL.git
cd sudo-SQL
uv pip install -r requirements.txt
```
*(Note: A `requirements.txt` can be generated from `pyproject.toml` if not present.)*

### 2. Configuration

Model configurations are managed in `configs/models.yaml`. You can define multiple providers here.

```yaml
# configs/models.yaml

openai_gpt4:
  type: "openai"
  args:
    model: "gpt-4"
    # For OpenAI, set your API key as an environment variable:
    # export OPENAI_API_KEY="your_key_here"

huggingface_t5:
  type: "huggingface"
  args:
    model_name: "t5-small"
```

## Usage

`sudo-SQL` provides a powerful command-line interface (`main.py`) for inference and training scripts in the `sudo_sql/training/` directory.

### Inference

The primary tool for Text-to-SQL generation is `main.py`.

**Basic Generation:**

Use one or more `--provider` flags to select the models defined in your config file.

```bash
# Create a dummy schema file
echo "CREATE TABLE users (id INT, name TEXT)" > schema.sql

# Run inference with a single provider
python main.py "Show me all user names" schema.sql --provider openai_gpt4
```

**Advanced Modes:**

-   **Critic Mode**: The first provider generates the SQL, and a critic (using the same provider) reviews it.
    ```bash
    python main.py "List all users" schema.sql --provider openai_gpt4 --use-critic
    ```

-   **Voting Mode**: Multiple providers generate SQL, and the most common result is chosen.
    ```bash
    python main.py "Count the users" schema.sql --provider openai_gpt4 --provider huggingface_t5 --voting
    ```

### Training

The framework includes scripts for both Supervised Fine-Tuning (SFT) and Reinforcement Learning (RL).

**1. Supervised Fine-Tuning (SFT) with LoRA:**

The `train.py` script in `sudo_sql/training/sft/` handles SFT. It downloads a dataset from Hugging Face, formats it, and uses `SFTTrainer` and LoRA to fine-tune a model.

```bash
python sudo_sql/training/sft/train.py \
    --model_name "codellama/CodeLlama-7b-hf" \
    --dataset_name "b-mc2/sql-create-context" \
    --output_dir "./sft-output" \
    --num_train_epochs 1
```

**2. Reinforcement Learning (RL) with `verl`:**

The `train_with_verl.py` script in `sudo_sql/training/rl/` uses PPO to fine-tune a model based on feedback from a live database.

```bash
# You need a database file for the environment
sqlite3 my_database.db "CREATE TABLE users (id INT, name TEXT);"

python sudo_sql/training/rl/train_with_verl.py \
    --model_name "codellama/CodeLlama-7b-hf" \
    --db_path "my_database.db" \
    --schema "CREATE TABLE users (id INT, name TEXT)" \
    --question "List the names of all users"
```

## Project Roadmap

-   [x] **Phase 1: Core Framework & Inference Engine**
-   [x] **Phase 2: Supervised Fine-Tuning (SFT) with LoRA**
-   [x] **Phase 3: Advanced Agents & Multi-Model Strategies**
-   [x] **Phase 4: Reinforcement Learning with `verl`**

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.
