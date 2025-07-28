import yaml
from sudo_sql.models.base import BaseModelProvider
from sudo_sql.models.openai import OpenAIProvider
from sudo_sql.models.huggingface import HuggingFaceProvider

class InferenceEngine:
    """
    The core inference engine that orchestrates the Text-to-SQL process.
    """
    def __init__(self, provider: BaseModelProvider):
        """
        Initializes the inference engine with a specific model provider.

        Args:
            provider: An instance of a class that inherits from BaseModelProvider.
        """
        self.provider = provider

    def run(self, question: str, schema: str) -> str:
        """
        Runs the inference process.

        Args:
            question: The natural language question.
            schema: The database schema.

        Returns:
            The generated SQL query.
        """
        return self.provider.generate_sql(question, schema)

def get_engine(provider_name: str = "openai", config_path: str = "configs/models.yaml") -> InferenceEngine:
    """
    Factory function to get an inference engine with a specific provider,
    loading configuration from a YAML file.

    Args:
        provider_name: The name of the provider to use ('openai' or 'huggingface').
        config_path: Path to the YAML configuration file.

    Returns:
        An instance of the InferenceEngine.
    """
    with open(config_path, 'r') as f:
        configs = yaml.safe_load(f)

    provider_config = configs.get(provider_name, {})

    if provider_name == "openai":
        provider = OpenAIProvider(**provider_config)
    elif provider_name == "huggingface":
        provider = HuggingFaceProvider(**provider_config)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
    
    return InferenceEngine(provider)
