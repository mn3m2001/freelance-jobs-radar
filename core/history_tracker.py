"""
History Tracker - Deduplication and Seen-Jobs Persistence
"""

import json
from datetime import datetime
from pathlib import Path
from config import HISTORY_FILE


class HistoryTracker:
    def __init__(self, file_path: Path = None):
        self.file_path = file_path or HISTORY_FILE
        self.seen_jobs = {}
        self._load()

    def _load(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.seen_jobs = json.load(f)
            except Exception as e:
                print(f"[HistoryTracker] Warning loading history: {e}")
                self.seen_jobs = {}
        else:
            self.seen_jobs = {}

    def _save(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.seen_jobs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[HistoryTracker] Error saving history: {e}")

    def is_new(self, job_id: str) -> bool:
        return job_id not in self.seen_jobs

    def mark_seen(self, job: dict):
        job_id = job.get("id")
        if not job_id:
            return
        self.seen_jobs[job_id] = {
            "title": job.get("title"),
            "platform": job.get("platform"),
            "url": job.get("url"),
            "first_seen": datetime.now().isoformat()
        }

    def filter_new(self, jobs: list, auto_mark: bool = False) -> list:
        """Return only jobs that have not been seen yet."""
        new_jobs = [j for j in jobs if self.is_new(j.get("id"))]
        if auto_mark:
            for j in new_jobs:
                self.mark_seen(j)
            self._save()
        return new_jobs

    def commit(self):
        """Save state to disk."""
        self._save()

    def count(self) -> int:
        return len(self.seen_jobs)
