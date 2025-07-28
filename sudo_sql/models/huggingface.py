from transformers import pipeline
from sudo_sql.models.base import BaseModelProvider

class HuggingFaceProvider(BaseModelProvider):
    """
    A provider for local Hugging Face models.
    """
    def __init__(self, model_name: str = "t5-small"):
        """
        Initializes the Hugging Face provider.

        Args:
            model_name: The name of the Hugging Face model to use.
        """
        self.model_name = model_name
        self.pipeline = pipeline("text2text-generation", model=self.model_name)

    def generate_sql(self, question: str, schema: str) -> str:
        """
        Generates SQL using the specified Hugging Face model.
        """
        # T5 models expect a prefix for the task, "translate English to SQL: " is a common one.
        input_text = f"translate English to SQL: {question} schema: {schema}"
        
        result = self.pipeline(input_text)
        
        return result[0]['generated_text'].strip()
