"""
Filter Engine - Matches and Scores Jobs against Target Niches
"""

import re
from config import KEYWORDS, CATEGORY_LABELS


class FilterEngine:
    def __init__(self, keywords_dict=None):
        self.keywords_dict = keywords_dict or KEYWORDS

    def evaluate_job(self, job: dict) -> dict:
        """
        Evaluate a single job dict.
        Returns a dict with match details, or None if no match.
        """
        title = (job.get("title") or "").lower()
        desc = (job.get("description") or "").lower()
        tags = " ".join(job.get("tags") or []).lower()
        full_text = f"{title} {desc} {tags}"

        matched_categories = []
        matched_keywords = []
        total_score = 0

        for cat_key, kw_list in self.keywords_dict.items():
            cat_matched = False
            for kw in kw_list:
                kw_lower = kw.lower()
                # Check title match (double weight)
                if kw_lower in title:
                    total_score += 3
                    cat_matched = True
                    matched_keywords.append(kw)
                elif kw_lower in full_text:
                    total_score += 1
                    cat_matched = True
                    matched_keywords.append(kw)

            if cat_matched:
                matched_categories.append(cat_key)

        if not matched_categories:
            return None

        # Format matched categories with human labels
        category_names = [CATEGORY_LABELS.get(c, c) for c in matched_categories]

        enriched_job = dict(job)
        enriched_job["categories"] = matched_categories
        enriched_job["category_labels"] = category_names
        enriched_job["matched_keywords"] = list(set(matched_keywords))
        enriched_job["score"] = total_score

        return enriched_job

    def filter_jobs(self, jobs: list, min_score: int = 1) -> list:
        """Filter a list of jobs, sorting by relevance score descending."""
        matched = []
        for j in jobs:
            evaluated = self.evaluate_job(j)
            if evaluated and evaluated["score"] >= min_score:
                matched.append(evaluated)

        # Sort by score descending
        matched.sort(key=lambda x: x["score"], reverse=True)
        return matched
