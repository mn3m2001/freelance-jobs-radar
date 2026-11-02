"""
Khamsat Community Requests Scraper
"""

import re
from scrapers.base_scraper import BaseScraper
from config import PLATFORMS


class KhamsatScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            platform_key="khamsat",
            platform_name=PLATFORMS["khamsat"]["name"],
            base_url=PLATFORMS["khamsat"]["url"]
        )

    def scrape(self) -> list:
        soup = self.fetch_soup(self.base_url)
        if not soup:
            return []

        jobs = []
        seen_urls = set()

        links = soup.select("a[href*='/community/requests/']")
        for link in links:
            url = link.get("href", "").strip()
            if not url or "requests/new" in url or url in seen_urls:
                continue

            match_id = re.search(r"/community/requests/(\d+)", url)
            if not match_id:
                continue

            seen_urls.add(url)
            job_id = f"khamsat_{match_id.group(1)}"

            if not url.startswith("http"):
                url = "https://khamsat.com" + url

            title = link.get_text(strip=True)
            if not title:
                continue

            tr = link.find_parent("tr")
            time_td = tr.select_one("td:last-child") if tr else None
            time_posted = time_td.get_text(strip=True) if time_td else "طلب جديد"

            jobs.append({
                "id": job_id,
                "platform": "khamsat",
                "platform_name": self.platform_name,
                "title": title,
                "url": url,
                "description": f"طلب خدمة في مجتمع خمسات: {title}",
                "budget": "يبدأ من $5",
                "time_posted": time_posted,
                "tags": []
            })

        return jobs
