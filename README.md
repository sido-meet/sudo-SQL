# sudo-SQL: Your Extensible Text-to-SQL Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced, modular, and extensible framework designed to bridge the gap between natural language and SQL databases. `sudo-SQL` focuses on leveraging Large Language Models (LLMs) for high-accuracy Text-to-SQL generation, training, and deployment.

This project is the second stage of a larger vision, building upon the schema generation capabilities of its sibling project, [D-Schema](https://github.com/sido-meet/D-Schema).

## Core Features

-   **Multi-Model Support**: Pluggable architecture to easily integrate with various LLMs, including:
    -   OpenAI (GPT-4, GPT-3.5)
    -   Anthropic (Claude 3)
    -   Local models via Ollama, Hugging Face Transformers.
-   **Advanced Inference Strategies**:
    -   **Multi-model Voting**: Enhance accuracy by polling multiple LLMs.
    -   **Critic Agent**: A secondary agent that reviews, validates, and corrects generated SQL for higher precision.
-   **Flexible Training Pipelines**:
    -   **Supervised Fine-Tuning (SFT)**: Adapt models to specific database schemas or question styles.
    -   **Reinforcement Learning (RL)**: Further refine models based on execution feedback.
-   **Efficient Training Techniques**:
    -   **LoRA / QLoRA**: Full support for parameter-efficient fine-tuning to reduce computational costs.
-   **One-Click Deployment**: Scripts and tools to simplify the deployment of trained models as services.

## Architecture & Design

`sudo-SQL` is designed with modularity at its core. The system is broken down into distinct components that can be developed, tested, and extended independently.

1.  **Schema Input**: The framework ingests database schemas pre-processed by `D-Schema` or a similar tool.
2.  **Model Providers**: A unified interface connects to different LLM APIs or local model servers. Adding a new model is as simple as implementing this interface.
3.  **Inference Engine**: Orchestrates the Text-to-SQL process. It takes a user question and a schema, queries the selected model provider(s), and passes the output to the agentic layer.
4.  **Agentic Layer**: This is where advanced logic resides. The `Critic Agent` and `Voting` mechanisms operate here to refine the final SQL query.
5.  **Training Pipelines**: Self-contained scripts and modules for SFT and RL, leveraging libraries like Hugging Face `transformers`, `peft`, and `trl`.

## Directory Structure

The project follows a structured layout to maintain clarity and scalability.

```
/
├─── .gitignore
├─── pyproject.toml
├─── README.md
├─── uv.lock
│
├─── configs/                  # Configuration files for models, training, etc.
│    └─── models.yaml
│
├─── data/                     # Datasets for training and evaluation
│    ├─── spider/
│    └─── custom_dataset/
│
├─── docs/                     # Detailed documentation
│
├─── scripts/                  # Helper scripts (data processing, deployment)
│    ├─── prepare_dataset.py
│    └─── deploy_fastapi.sh
│
├─── sudo_sql/                 # Main source code
│    ├─── __init__.py
│    │
│    ├─── agents/               # Critic and other agents
│    │    ├─── __init__.py
│    │    └─── critic.py
│    │
│    ├─── models/               # LLM provider integrations
│    │    ├─── __init__.py
│    │    ├─── base.py          # Base model provider interface
│    │    ├─── openai.py
│    │    └─── huggingface.py
│    │
│    ├─── inference/           # Core inference logic
│    │    ├─── __init__.py
│    │    └─── engine.py
│    │
│    ├─── training/            # SFT and RL training pipelines
│    │    ├─── __init__.py
│    │    ├─── sft/
│    │    └─── rl/
│    │
│    └─── evaluation/          # SQL evaluation logic
│         ├─── __init__.py
│         └─── metrics.py
│
└─── tests/                    # Unit and integration tests
     └─── test_inference.py
```

## Project Roadmap

This project will be developed in phases to ensure a stable and feature-rich progression.

### Phase 1: Core Framework & Inference Engine (Current Focus)

-   [x] **Initial Project Setup**: Initialize project with `uv` and define structure.
-   [ ] **Directory Structure Implementation**: Create the folders and initial files outlined above.
-   [ ] **Unified Model Interface**: Design and implement the base `ModelProvider` class in `sudo_sql/models/base.py`.
-   [ ] **Initial Model Integrations**: Implement providers for OpenAI and a local Hugging Face model.
-   [ ] **Core Inference Engine**: Build the main inference pipeline that takes a question and schema, and returns a SQL query.
-   [ ] **Configuration Management**: Set up `configs/models.yaml` to handle API keys and model parameters.
-   [ ] **Basic CLI**: Create a simple command-line interface to test inference.

### Phase 2: Supervised Fine-Tuning (SFT) with LoRA

-   [ ] **Data Handling**: Integrate Hugging Face `datasets` for loading and processing Text-to-SQL datasets.
-   [ ] **SFT Script**: Develop the main fine-tuning script in `sudo_sql/training/sft/`.
-   [ ] **LoRA/PEFT Integration**: Integrate the `peft` library to enable parameter-efficient fine-tuning.
-   [ ] **Evaluation Metrics**: Implement execution accuracy and exact match scoring in `sudo_sql/evaluation/`.

### Phase 3: Advanced Agents & Multi-Model Strategies

-   [ ] **Critic Agent**: Develop the `Critic` agent to review and correct generated SQL. This will likely involve a separate LLM call with a specific prompt template.
-   [ ] **Multi-Model Voting**: Implement a strategy in the inference engine to query multiple models and select the best response.
-   [ ] **Agent Plugin System**: Design a simple plugin architecture to easily add or remove agents like the `Critic`.

### Phase 4: Reinforcement Learning & Deployment

-   [ ] **RL Pipeline**: Research and implement an RL-based fine-tuning pipeline (e.g., using `trl`) to optimize SQL generation from database feedback.
-   [ ] **One-Click Deployment**: Create shell scripts and Dockerfiles to package and deploy the inference engine as a FastAPI service.
-   [ ] **Comprehensive CLI/UI**: Expand the CLI with more features or build a simple Streamlit/Gradio web UI for demos.

## Getting Started

*(This section will be updated once Phase 1 is complete.)*

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.