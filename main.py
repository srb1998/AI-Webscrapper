import asyncio
import argparse
import json
from typing import List, Dict
from crawler import EcommerceCrawler
from classifier import URLClassifier

async def main(domains: List[str], patterns: List[str], output_file: str):
    crawler = EcommerceCrawler(depth=3)
    classifier = URLClassifier()

    results: Dict[str, List[str]] = {}

    for domain in domains:
        print(f"Crawling domain: {domain}")
        product_urls = await crawler.crawl_domain(domain, patterns, classifier)
        results[domain] = list(product_urls)

    # Write results to a JSON file
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Crawling completed. Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="E-commerce Product URL Crawler")
    parser.add_argument("--domains", nargs='+', required=True, help="List of e-commerce domains to crawl")
    parser.add_argument("--output", required=True, help="Output file to save the results")
    
    args = parser.parse_args()

    # Patterns for product URLs
    PRODUCT_PATTERNS = [
        r"/product/", r"/item/", r"/p/", r"/products/", r"/shop/"
    ]

    asyncio.run(main(args.domains, PRODUCT_PATTERNS, args.output))
