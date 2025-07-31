import os
from openai import OpenAI
from sudo_sql.models.base import BaseModelProvider
from dotenv import load_dotenv

load_dotenv()

class OpenAIProvider(BaseModelProvider):
    """
    A provider for OpenAI and compatible models.
    """
    def __init__(self, model: str = "gpt-4", api_key: str = None, base_url: str = None):
        """
        Initializes the OpenAI provider.

        Args:
            model: The name of the OpenAI model to use.
            api_key: The OpenAI API key. Can be None for local models.
            base_url: The base URL for the API endpoint.
        """
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        # If no api_key is found, set it to a dummy value for local models, as the client requires it.
        if not self.api_key:
            self.api_key = "no-key"

        self.client = OpenAI(api_key=self.api_key, base_url=base_url)

    def generate(self, prompt: str) -> str:
        """
        Generates text using the specified OpenAI model.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates SQL queries."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()
