import asyncio
import httpx
from bs4 import BeautifulSoup
import re
from typing import List, Set
from classifier import URLClassifier

class EcommerceCrawler:
    def __init__(self, depth: int = 2):
        self.depth = depth
        self.visited = set()

    async def fetch_page(self, client: httpx.AsyncClient, url: str) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        try:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            print(f"Error fetching {url}: {e.response.status_code} {e.response.reason_phrase}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return ""

    async def crawl_domain(self, domain: str, patterns: List[str], classifier: URLClassifier) -> Set[str]:
        product_urls = set()
        queue = [f"https://{domain}"]

        async with httpx.AsyncClient(follow_redirects=True) as client:
            for _ in range(self.depth):
                tasks = [self.fetch_page(client, url) for url in queue if url not in self.visited]
                self.visited.update(queue)
                queue = []

                responses = await asyncio.gather(*tasks)

                for html in responses:
                    if not html:
                        continue
                    soup = BeautifulSoup(html, "html.parser")

                    for a_tag in soup.find_all("a", href=True):
                        href = a_tag["href"]
                        absolute_url = href if href.startswith("http") else f"https://{domain.rstrip('/')}/{href.lstrip('/')}"

                        if any(re.search(pattern, absolute_url) for pattern in patterns) or classifier.is_product_url(absolute_url):
                            product_urls.add(absolute_url)
                        elif domain in absolute_url and absolute_url not in self.visited:
                            queue.append(absolute_url)
        return product_urls