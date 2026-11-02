"""
Local Reporter - Console Output & Markdown/JSON Report Generator
"""

import json
from datetime import datetime
from tabulate import tabulate
from colorama import Fore, Style, init
from config import LATEST_MATCHES_MD, LATEST_MATCHES_JSON

# Initialize colorama
init(autoreset=True)


class LocalReporter:
    @staticmethod
    def print_console_summary(all_scraped_count: int, matched_jobs: list, is_all_mode: bool = False):
        print("\n" + "=" * 70)
        print(f"{Fore.CYAN}{Style.BRIGHT}  Freelance Jobs Radar - Execution Summary")
        print("=" * 70)
        print(f"Total jobs scraped: {Fore.YELLOW}{all_scraped_count}")
        print(f"Matching opportunities found: {Fore.GREEN}{Style.BRIGHT}{len(matched_jobs)}")
        if is_all_mode:
            print(f"Mode: {Fore.MAGENTA}Displaying ALL matches (history check bypassed)")
        else:
            print(f"Mode: {Fore.MAGENTA}New matches only (deduplicated against history)")
        print("-" * 70)

        if not matched_jobs:
            print(f"{Fore.YELLOW}No new matching opportunities found in this run.")
            print("=" * 70 + "\n")
            return

        table_data = []
        for i, j in enumerate(matched_jobs, 1):
            categories_str = ", ".join(j.get("categories", []))
            table_data.append([
                i,
                j.get("platform_name", j.get("platform")),
                j.get("title")[:40] + ("..." if len(j.get("title")) > 40 else ""),
                categories_str,
                j.get("budget", "N/A"),
                f"Score: {j.get('score', 0)}"
            ])

        headers = ["#", "Platform", "Title", "Matched Niches", "Budget", "Relevance"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print("=" * 70)
        print(f"{Fore.GREEN}Detailed links and report saved to: {LATEST_MATCHES_MD}")
        print("=" * 70 + "\n")

    @staticmethod
    def save_markdown_report(matched_jobs: list):
        """Save latest matches to an attractive Markdown digest."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"# Freelance Jobs Radar - Latest Matches Report",
            f"\n> **Generated At**: `{now_str}`",
            f"> **Total Opportunities**: `{len(matched_jobs)}`\n",
            "---",
            "\n## Quick Opportunities Overview\n"
        ]

        if not matched_jobs:
            lines.append("No matching jobs found in this run.\n")
        else:
            table_rows = []
            table_rows.append("| # | Platform | Title | Categories | Budget | Link |")
            table_rows.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

            for i, j in enumerate(matched_jobs, 1):
                cat_str = ", ".join(j.get("categories", []))
                safe_title = j.get("title", "").replace("|", "-")
                table_rows.append(
                    f"| {i} | {j.get('platform_name')} | {safe_title} | `{cat_str}` | {j.get('budget')} | [Apply Now]({j.get('url')}) |"
                )

            lines.extend(table_rows)
            lines.append("\n---\n")
            lines.append("## Detailed Breakdown\n")

            for i, j in enumerate(matched_jobs, 1):
                lines.append(f"### {i}. [{j.get('title')}]({j.get('url')})")
                lines.append(f"- **Platform**: `{j.get('platform_name')}`")
                lines.append(f"- **Categories**: {', '.join(j.get('category_labels', []))}")
                lines.append(f"- **Matched Keywords**: `{', '.join(j.get('matched_keywords', []))}`")
                lines.append(f"- **Budget / Price**: `{j.get('budget')}`")
                lines.append(f"- **Posted**: `{j.get('time_posted')}`")
                if j.get("description"):
                    lines.append(f"- **Description Snippet**: {j.get('description')}")
                lines.append(f"- **Direct Link**: [{j.get('url')}]({j.get('url')})\n")

        with open(LATEST_MATCHES_MD, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    @staticmethod
    def save_json_report(matched_jobs: list):
        """Save raw JSON data for downstream pipelines."""
        payload = {
            "timestamp": datetime.now().isoformat(),
            "count": len(matched_jobs),
            "jobs": matched_jobs
        }
        with open(LATEST_MATCHES_JSON, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
