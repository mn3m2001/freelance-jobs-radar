"""
Base Scraper Class for Freelance Platforms
"""

import requests
from bs4 import BeautifulSoup
from config import USER_AGENT, REQUEST_TIMEOUT


class BaseScraper:
    def __init__(self, platform_key: str, platform_name: str, base_url: str):
        self.platform_key = platform_key
        self.platform_name = platform_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        })

    def fetch_soup(self, url: str) -> BeautifulSoup:
        """Fetch URL and return BeautifulSoup object with graceful error handling."""
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"[{self.platform_name}] Error fetching {url}: {e}")
            return None

    def scrape(self) -> list:
        """Override this method in subclasses to extract job listings."""
        raise NotImplementedError("Subclasses must implement scrape()")
