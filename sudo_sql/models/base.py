from abc import ABC, abstractmethod

class BaseModelProvider(ABC):
    """
    Abstract base class for all model providers.
    It ensures that any new model integration will follow a consistent interface.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        The core generation method that takes a formatted prompt and returns the model's output.

        Args:
            prompt: The complete prompt to be sent to the model.

        Returns:
            The generated text as a string.
        """
        pass

    def generate_sql(self, question: str, schema: str) -> str:
        """
        Generates an SQL query by creating a specific prompt and calling the generate method.

        Args:
            question: The natural language question from the user.
            schema: The database schema description (e.g., from D-Schema).

        Returns:
            The generated SQL query as a string.
        """
        prompt = f"""Given the following database schema:
{schema}

Please generate the SQL query for the following question:
\"{question}\"
"""
        return self.generate(prompt)
