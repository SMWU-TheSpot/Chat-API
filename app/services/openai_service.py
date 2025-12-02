from openai import AzureOpenAI
from app.core.config import Config

class OpenAIService:
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            api_key=Config.AZURE_OPENAI_KEY,
            api_version="2024-10-01-preview"
        )

    def ask(self, messages):
        response = self.client.chat.completions.create(
            model=Config.AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            temperature=0.3,
            max_tokens=800
        )
        return response.choices[0].message.content