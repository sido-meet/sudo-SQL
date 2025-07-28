import yaml
from sudo_sql.models.base import BaseModelProvider
from sudo_sql.models.openai import OpenAIProvider
from sudo_sql.models.huggingface import HuggingFaceProvider
from sudo_sql.agents.critic import CriticAgent

class InferenceEngine:
    """
    The core inference engine that orchestrates the Text-to-SQL process.
    """
    def __init__(self, provider: BaseModelProvider, critic: CriticAgent = None):
        """
        Initializes the inference engine.

        Args:
            provider: The primary model provider for initial SQL generation.
            critic: An optional CriticAgent for reviewing the generated SQL.
        """
        self.provider = provider
        self.critic = critic

    def run(self, question: str, schema: str) -> str:
        """
        Runs the basic inference process.

        Args:
            question: The natural language question.
            schema: The database schema.

        Returns:
            The generated SQL query.
        """
        return self.provider.generate_sql(question, schema)

    def run_with_critic(self, question: str, schema: str) -> str:
        """
        Runs the inference process with a critic to review and correct the SQL.

        Args:
            question: The natural language question.
            schema: The database schema.

        Returns:
            The reviewed and potentially corrected SQL query.
        """
        if not self.critic:
            raise ValueError("CriticAgent is not configured for this engine.")

        # 1. Generate initial SQL
        initial_sql = self.run(question, schema)

        # 2. Let the critic review and correct it
        corrected_sql = self.critic.review_and_correct(question, schema, initial_sql)

        return corrected_sql

def get_engine(provider_name: str = "openai", config_path: str = "configs/models.yaml", with_critic: bool = False) -> InferenceEngine:
    """
    Factory function to get an inference engine.

    Args:
        provider_name: The name of the provider to use ('openai' or 'huggingface').
        config_path: Path to the YAML configuration file.
        with_critic: Whether to initialize the engine with a CriticAgent.

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

    critic = None
    if with_critic:
        # For simplicity, the critic uses the same provider. This could be configured separately.
        critic = CriticAgent(provider)
    
    return InferenceEngine(provider, critic=critic)
