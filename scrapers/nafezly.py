"""
Nafezly Platform Scraper
"""

import re
from scrapers.base_scraper import BaseScraper
from config import PLATFORMS


class NafezlyScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            platform_key="nafezly",
            platform_name=PLATFORMS["nafezly"]["name"],
            base_url=PLATFORMS["nafezly"]["url"]
        )

    def scrape(self) -> list:
        soup = self.fetch_soup(self.base_url)
        if not soup:
            return []

        jobs = []
        seen_urls = set()

        # Find project links on Nafezly
        links = soup.select("a[href*='/project/']")
        for link in links:
            url = link.get("href", "").strip()
            if not url or url in seen_urls:
                continue

            match_id = re.search(r"/project/(\d+)", url)
            if not match_id:
                continue

            seen_urls.add(url)
            job_id = f"nafezly_{match_id.group(1)}"

            if not url.startswith("http"):
                url = "https://nafezly.com" + url

            title = link.get_text(strip=True)
            if not title:
                continue

            # Card container
            card = link.find_parent("div", class_=re.compile(r"project|box|card", re.I)) or link.parent
            card_text = card.get_text(" ", strip=True) if card else ""

            # Extract tags (e.g. badges / skill pills)
            tag_elements = card.select("span.badge, a.badge, span.tag, a.tag") if card else []
            tags = [t.get_text(strip=True) for t in tag_elements if t.get_text(strip=True)]

            # Extract price or budget
            budget_match = re.search(r"(\$\s*\d+[\s\-\$\d]*|\d+\s*(?:دولار|ريال|جنيه))", card_text)
            budget = budget_match.group(0) if budget_match else "مفتوح"

            # Time posted
            time_match = re.search(r"منذ\s+[\w\s]+", card_text)
            time_posted = time_match.group(0) if time_match else "جديد"

            desc = card_text.replace(title, "").strip()[:200]

            jobs.append({
                "id": job_id,
                "platform": "nafezly",
                "platform_name": self.platform_name,
                "title": title,
                "url": url,
                "description": desc,
                "budget": budget,
                "time_posted": time_posted,
                "tags": tags
            })

        return jobs
