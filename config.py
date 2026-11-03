"""
Freelance Jobs Radar - Configuration Module
Author: Abdelmonem (mn3m2001) - Data Analyst & Aspiring Data Scientist
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# Explicitly load .env from project directory
load_dotenv(dotenv_path=ENV_FILE)
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

HISTORY_FILE = DATA_DIR / "history.json"
LATEST_MATCHES_JSON = DATA_DIR / "latest_matches.json"
LATEST_MATCHES_MD = DATA_DIR / "latest_matches.md"

# Target Niche Keywords categorized by domain
KEYWORDS = {
    "web_scraping": [
        "سحب بيانات", "استخراج بيانات", "جمع بيانات", "scraping", "scraper",
        "scrape", "crawler", "crawl", "بايثون", "python", "تفريغ بيانات"
    ],
    "data_analysis": [
        "تحليل بيانات", "محلل بيانات", "data analysis", "data analyst",
        "تنظيف بيانات", "data cleaning", "إكسل", "اكسل", "excel",
        "power bi", "باور بي اي", "باور بي آي", "pandas", "لوحة بيانات",
        "dashboard", "تحليل مبيعات", "احصاء", "إحصاء"
    ],
    "automation": [
        "أتمتة", "اتمتة", "automation", "بوت", "bot", "سكربت", "script",
        "n8n", "selenium", "أتمته", "تلقائي", "مهام تلقائية", "تليجرام بوت"
    ],
    "ecommerce": [
        "متجر", "متاجر", "متجر الكتروني", "متجر إلكتروني", "سلة", "زد",
        "shopify", "شوبيفاي", "woocommerce", "ووكومرس", "إنشاء متجر",
        "تصميم متجر", "تأسيس متجر", "منتجات", "e-commerce"
    ]
}

# Domain display labels (Arabic & English)
CATEGORY_LABELS = {
    "web_scraping": "Web Scraping (سحب البيانات)",
    "data_analysis": "Data Analysis (تحليل البيانات)",
    "automation": "Automation (الأتمتة والسكربتات)",
    "ecommerce": "E-Commerce Setup (تصميم المتاجر الإلكترونية)"
}

# Supported Freelance Platforms
PLATFORMS = {
    "mostaql": {
        "name": "مستقل (Mostaql)",
        "url": "https://mostaql.com/projects",
        "enabled": True
    },
    "kafiil": {
        "name": "كفيل (Kafiil)",
        "url": "https://kafiil.com/projects",
        "enabled": True
    },
    "nafezly": {
        "name": "نفذلي (Nafezly)",
        "url": "https://nafezly.com/projects",
        "enabled": True
    },
    "khamsat": {
        "name": "خمسات (Khamsat)",
        "url": "https://khamsat.com/community/requests",
        "enabled": True
    },
    "freelanceyard": {
        "name": "فريلانس يارد (FreelanceYard)",
        "url": "https://freelanceyard.com/jobs",
        "enabled": True
    }
}

# Request configuration
REQUEST_TIMEOUT = 15
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Telegram Bot Notification (Optional)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
ENABLE_TELEGRAM = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
