import os
from openai import OpenAI
from sudo_sql.models.base import BaseModelProvider

class OpenAIProvider(BaseModelProvider):
    """
    A provider for OpenAI models like GPT-4 and GPT-3.5.
    """
    def __init__(self, model: str = "gpt-4", api_key: str = None):
        """
        Initializes the OpenAI provider.

        Args:
            model: The name of the OpenAI model to use.
            api_key: The OpenAI API key. If not provided, it will be
                     sourced from the OPENAI_API_KEY environment variable.
        """
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Please set the OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)

    def generate_sql(self, question: str, schema: str) -> str:
        """
        Generates SQL using the specified OpenAI model.
        """
        prompt = f"""Given the following database schema:
{schema}

Please generate the SQL query for the following question:
\"{question}\"
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates SQL queries."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()
