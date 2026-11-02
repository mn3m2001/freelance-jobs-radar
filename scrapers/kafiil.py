"""
Kafiil Platform Scraper
"""

import re
from scrapers.base_scraper import BaseScraper
from config import PLATFORMS


class KafiilScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            platform_key="kafiil",
            platform_name=PLATFORMS["kafiil"]["name"],
            base_url=PLATFORMS["kafiil"]["url"]
        )

    def scrape(self) -> list:
        soup = self.fetch_soup(self.base_url)
        if not soup:
            return []

        jobs = []
        seen_urls = set()

        # Find all project links on Kafiil
        links = soup.select("a[href*='/project/']")
        for link in links:
            url = link.get("href", "").strip()
            if not url or "project/create" in url or url in seen_urls:
                continue

            match_id = re.search(r"/project/(\d+)", url)
            if not match_id:
                continue

            seen_urls.add(url)
            job_id = f"kafiil_{match_id.group(1)}"

            if not url.startswith("http"):
                url = "https://kafiil.com" + url

            title = link.get_text(strip=True)
            if not title:
                continue

            # Traverse to card container to find budget, date, and description
            card = link.find_parent("div", class_=re.compile(r"project|item|card", re.I)) or link.parent
            card_text = card.get_text(" ", strip=True) if card else ""

            # Extract budget like $25 - $50 or similar
            budget_match = re.search(r"\$\s*\d+\s*-\s*\$\s*\d+|\$\s*\d+", card_text)
            budget = budget_match.group(0) if budget_match else "حسب الاتفاق"

            # Extract time if available
            time_match = re.search(r"منذ\s+[\w\s]+", card_text)
            time_posted = time_match.group(0) if time_match else "حديثاً"

            # Clean description snippet from card text
            desc = card_text.replace(title, "").strip()[:200]

            jobs.append({
                "id": job_id,
                "platform": "kafiil",
                "platform_name": self.platform_name,
                "title": title,
                "url": url,
                "description": desc,
                "budget": budget,
                "time_posted": time_posted,
                "tags": []
            })

        return jobs
