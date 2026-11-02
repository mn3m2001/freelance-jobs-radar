"""
Mostaql Platform Scraper
"""

import re
from scrapers.base_scraper import BaseScraper
from config import PLATFORMS


class MostaqlScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            platform_key="mostaql",
            platform_name=PLATFORMS["mostaql"]["name"],
            base_url=PLATFORMS["mostaql"]["url"]
        )

    def scrape(self) -> list:
        soup = self.fetch_soup(self.base_url)
        if not soup:
            return []

        jobs = []
        rows = soup.select("tr.project-row, div.project-row")
        for row in rows:
            link_tag = row.select_one("h2 a, a[href*='/project/']")
            if not link_tag:
                continue

            url = link_tag.get("href", "").strip()
            if not url.startswith("http"):
                url = "https://mostaql.com" + url

            match_id = re.search(r"/project/(\d+)", url)
            job_id = f"mostaql_{match_id.group(1)}" if match_id else f"mostaql_{hash(url)}"

            title = link_tag.get_text(strip=True)

            desc_tag = row.select_one("p.project__brief, p")
            desc = desc_tag.get_text(" ", strip=True) if desc_tag else ""

            time_tag = row.select_one("time")
            time_posted = time_tag.get_text(strip=True) if time_tag else "غير محدد"

            # Check for budget or proposals if present
            meta_items = row.select("ul.project__meta li, div.project__meta span")
            meta_texts = [m.get_text(strip=True) for m in meta_items if m.get_text(strip=True)]
            budget = meta_texts[0] if meta_texts else "حسب العرض"

            jobs.append({
                "id": job_id,
                "platform": "mostaql",
                "platform_name": self.platform_name,
                "title": title,
                "url": url,
                "description": desc,
                "budget": budget,
                "time_posted": time_posted,
                "tags": []
            })

        return jobs
