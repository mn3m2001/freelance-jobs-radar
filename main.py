"""
Freelance Jobs Radar - Main Orchestrator
Author: Abdelmonem (mn3m2001) - Data Analyst & Aspiring Data Scientist
"""

import sys
import argparse

# Force UTF-8 encoding for Windows standard output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from colorama import Fore, Style, init

from config import PLATFORMS, ENABLE_TELEGRAM
from scrapers import ALL_SCRAPERS
from core.filter_engine import FilterEngine
from core.history_tracker import HistoryTracker
from notifiers.local_reporter import LocalReporter
from notifiers.telegram_notifier import TelegramNotifier

init(autoreset=True)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Freelance Jobs Radar: Monitor Arabic & Regional Freelance Platforms"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Bypass history deduplication and show all current matching jobs"
    )
    parser.add_argument(
        "--platform",
        type=str,
        choices=["mostaql", "kafiil", "nafezly", "khamsat", "freelanceyard"],
        help="Run scraper for a specific platform only"
    )
    parser.add_argument(
        "--no-alert",
        action="store_true",
        help="Disable Telegram alerts even if configured"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save newly seen jobs to history.json"
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=1,
        help="Minimum relevance score threshold (default: 1)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"\n{Fore.CYAN}{Style.BRIGHT}==================================================")
    print(f"{Fore.CYAN}{Style.BRIGHT}  [*] Freelance Jobs Radar (Arabic Platforms Edition)")
    print(f"{Fore.CYAN}{Style.BRIGHT}=================================================={Style.RESET_ALL}")
    print(f"Target Platforms: {', '.join(PLATFORMS.keys())}")
    print(f"Target Domains: Web Scraping, Data Analysis, Automation, E-Commerce Setup\n")

    # 1. Instantiate Scrapers
    scrapers = []
    for ScraperClass in ALL_SCRAPERS:
        scraper_inst = ScraperClass()
        if args.platform and scraper_inst.platform_key != args.platform:
            continue
        scrapers.append(scraper_inst)

    # 2. Scrape platforms
    all_scraped_jobs = []
    for s in scrapers:
        print(f"[*] Scanning {Fore.YELLOW}{s.platform_name}{Style.RESET_ALL}...", end=" ", flush=True)
        try:
            jobs = s.scrape()
            print(f"{Fore.GREEN}Done! ({len(jobs)} projects found)")
            all_scraped_jobs.extend(jobs)
        except Exception as e:
            print(f"{Fore.RED}Failed: {e}")

    # 3. Filter and score jobs
    filter_engine = FilterEngine()
    matched_jobs = filter_engine.filter_jobs(all_scraped_jobs, min_score=args.min_score)

    # 4. History tracking and deduplication
    tracker = HistoryTracker()
    if args.all:
        jobs_to_report = matched_jobs
    else:
        jobs_to_report = tracker.filter_new(matched_jobs)

    # 5. Local Reporting (Console, Markdown, JSON)
    LocalReporter.print_console_summary(
        all_scraped_count=len(all_scraped_jobs),
        matched_jobs=jobs_to_report,
        is_all_mode=args.all
    )
    LocalReporter.save_markdown_report(jobs_to_report)
    LocalReporter.save_json_report(jobs_to_report)

    # 6. Telegram Notifications
    if not args.no_alert and ENABLE_TELEGRAM and jobs_to_report:
        print(f"[*] Dispatching {len(jobs_to_report)} alerts to Telegram...")
        notifier = TelegramNotifier()
        sent = notifier.send_batch_alerts(jobs_to_report)
        print(f"{Fore.GREEN}Successfully sent {sent} alerts to your Telegram chat!\n")
    elif not ENABLE_TELEGRAM:
        print(f"{Fore.BLUE}Tip: Add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env to get live alerts on your phone.{Style.RESET_ALL}\n")

    # 7. Update History
    if not args.no_save and jobs_to_report:
        for j in jobs_to_report:
            tracker.mark_seen(j)
        tracker.commit()
        print(f"[+] History updated. Total indexed jobs: {tracker.count()}\n")


if __name__ == "__main__":
    main()

