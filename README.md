# E-commerce Product URL Crawler

## Overview
This project is an asynchronous web crawler designed to find and classify "product" URLs from various e-commerce websites. The crawler fetches web pages, extracts links, and uses a machine learning model to classify whether a URL points to a product page.

## Features
- **Asynchronous Web Crawling**: Built using `httpx` and `asyncio` for efficient, concurrent crawling.
- **HTML Parsing**: Utilizes `BeautifulSoup` for extracting links from web pages.
- **URL Classification**: Leverages a pre-trained `distilbert-base-uncased-finetuned-sst-2-english` model from the `transformers` library to classify URLs.
- **Respect for Crawling Rules**: Handles `robots.txt` files to ensure compliance with website crawling policies.
- **Automatic Redirect Handling**: Manages HTTP redirects seamlessly during crawling.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ecommerce-crawler.git
   ```
   Replace the above link with the actual repository if required:
   ```bash
   git clone https://github.com/srb1998/AI-Web-Scrapper.git
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Crawler**:
   ```bash
   python main.py --domains example.com anotherexample.com --output results.json
   ```
   Example:
   ```bash
   python main.py --domains gamenation.in myntra.com gameloot.in snitch.co.in --output results.json
   ```

2. **Configuration**:
   - Modify the `main.py` file to specify the starting URLs and crawling depth.

## Project Structure
- **`crawler.py`**: Contains the `EcommerceCrawler` class responsible for fetching pages, parsing HTML, and extracting URLs.
- **`classifier.py`**: Contains the `URLClassifier` class responsible for fetching page content, extracting text, and classifying URLs.
- **`main.py`**: Entry point for running the crawler.
- **`results.json`**: Stores the results of the crawling process.

