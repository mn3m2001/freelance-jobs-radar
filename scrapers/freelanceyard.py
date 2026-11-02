"""
FreelanceYard Platform Scraper
"""

import re
from scrapers.base_scraper import BaseScraper
from config import PLATFORMS


class FreelanceYardScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            platform_key="freelanceyard",
            platform_name=PLATFORMS["freelanceyard"]["name"],
            base_url=PLATFORMS["freelanceyard"]["url"]
        )

    def scrape(self) -> list:
        soup = self.fetch_soup(self.base_url)
        if not soup:
            return []

        jobs = []
        seen_urls = set()

        links = soup.select("a[href*='/jobs/']")
        for link in links:
            url = link.get("href", "").strip()
            if not url or url in ["/jobs", "/ar/jobs"] or url in seen_urls:
                continue

            seen_urls.add(url)
            slug = url.strip("/").split("/")[-1]
            job_id = f"freelanceyard_{slug}"

            if not url.startswith("http"):
                url = "https://freelanceyard.com" + url

            title = link.get_text(strip=True)
            if not title or len(title) < 3:
                continue

            card = link.find_parent("div", class_=re.compile(r"job|card|item", re.I)) or link.parent
            card_text = card.get_text(" ", strip=True) if card else ""

            # Check for date or metadata
            date_match = re.search(r"\d{2}-\d{2}-\d{4}", card_text)
            time_posted = date_match.group(0) if date_match else "حديثاً"

            jobs.append({
                "id": job_id,
                "platform": "freelanceyard",
                "platform_name": self.platform_name,
                "title": title,
                "url": url,
                "description": card_text.replace(title, "").strip()[:200],
                "budget": "حسب العرض",
                "time_posted": time_posted,
                "tags": []
            })

        return jobs
