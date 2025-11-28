import os
from openai import OpenAI
import time

class Summarizer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            print("Warning: No OpenAI API key found. Summarization will be mocked.")

    def summarize(self, text):
        """Summarizes the given text using OpenAI API."""
        if not self.client:
            return self.mock_summarize(text)

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes news articles. Keep it concise (2-3 sentences)."},
                    {"role": "user", "content": f"Summarize this text:\n\n{text[:4000]}"} # Truncate to avoid token limits
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error during summarization: {e}")
            return self.mock_summarize(text)

    def mock_summarize(self, text):
        """Mock summarization for when API is unavailable."""
        sentences = text.split('.')
        return ". ".join(sentences[:3]) + "."
