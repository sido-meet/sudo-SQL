import yaml
from collections import Counter
from sudo_sql.models.base import BaseModelProvider
from sudo_sql.models.openai import OpenAIProvider
from sudo_sql.models.huggingface import HuggingFaceProvider
from sudo_sql.agents.critic import CriticAgent

class InferenceEngine:
    """
    The core inference engine that orchestrates the Text-to-SQL process.
    """
    def __init__(self, providers: list[BaseModelProvider], critic: CriticAgent = None):
        """
        Initializes the inference engine.

        Args:
            providers: A list of model providers for SQL generation. The first is the primary.
            critic: An optional CriticAgent for reviewing the generated SQL.
        """
        if not providers:
            raise ValueError("At least one model provider is required.")
        self.providers = providers
        self.critic = critic

    def run(self, question: str, schema: str) -> str:
        """
        Runs the basic inference process using the primary model provider.

        Args:
            question: The natural language question.
            schema: The database schema.

        Returns:
            The generated SQL query.
        """
        primary_provider = self.providers[0]
        return primary_provider.generate_sql(question, schema)

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

        initial_sql = self.run(question, schema)
        corrected_sql = self.critic.review_and_correct(question, schema, initial_sql)
        return corrected_sql

    def run_with_voting(self, question: str, schema: str) -> str:
        """
        Runs inference with multiple providers and returns the most common SQL query.

        Args:
            question: The natural language question.
            schema: The database schema.

        Returns:
            The SQL query that received the most votes.
        """
        if len(self.providers) < 2:
            print("Warning: Voting requires at least 2 providers. Running with a single provider.")
            return self.run(question, schema)

        all_sql_queries = [p.generate_sql(question, schema) for p in self.providers]
        
        # Find the most common query
        vote_counts = Counter(all_sql_queries)
        most_common_sql = vote_counts.most_common(1)[0][0]
        
        return most_common_sql

def get_engine(provider_names: list[str], config_path: str = "configs/models.yaml", with_critic: bool = False) -> InferenceEngine:
    """
    Factory function to get an inference engine.

    Args:
        provider_names: A list of provider names to use (e.g., ['openai', 'huggingface']).
        config_path: Path to the YAML configuration file.
        with_critic: Whether to initialize the engine with a CriticAgent.

    Returns:
        An instance of the InferenceEngine.
    """
    with open(config_path, 'r') as f:
        configs = yaml.safe_load(f)

    providers = []
    for name in provider_names:
        provider_config = configs.get(name)
        if not provider_config:
            raise ValueError(f"Configuration for provider '{name}' not found in {config_path}")
        
        provider_type = provider_config.get("type")
        provider_args = provider_config.get("args", {})

        if provider_type == "openai":
            providers.append(OpenAIProvider(**provider_args))
        elif provider_type == "huggingface":
            providers.append(HuggingFaceProvider(**provider_args))
        else:
            raise ValueError(f"Unknown provider type '{provider_type}' for provider '{name}'")

    critic = None
    if with_critic:
        # The critic uses the primary (first) provider
        critic = CriticAgent(providers[0])
    
    return InferenceEngine(providers, critic=critic)
