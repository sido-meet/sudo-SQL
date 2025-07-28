from abc import ABC, abstractmethod

class BaseModelProvider(ABC):
    """
    Abstract base class for all model providers.
    It ensures that any new model integration will follow a consistent interface.
    """

    @abstractmethod
    def generate_sql(self, question: str, schema: str) -> str:
        """
        Generates an SQL query based on a natural language question and a database schema.

        Args:
            question: The natural language question from the user.
            schema: The database schema description (e.g., from D-Schema).

        Returns:
            The generated SQL query as a string.
        """
        pass
