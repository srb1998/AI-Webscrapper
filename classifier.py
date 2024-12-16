# --- classifier.py ---
from transformers import pipeline
from bs4 import BeautifulSoup
import httpx

class URLClassifier:
    def __init__(self):
        self.classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

    async def fetch_page_content(self, url: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10, follow_redirects=True)
            response.raise_for_status()
            return response.text

    def extract_text(self, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.stripped_strings
        return ' '.join(texts)

    async def is_product_url(self, url: str) -> bool:
        try:
            html_content = await self.fetch_page_content(url)
            text_content = self.extract_text(html_content)
            prediction = self.classifier(text_content)
            return prediction[0]['label'] == 'POSITIVE'
        except Exception as e:
            print(f"Error classifying {url}: {e}")
            return False