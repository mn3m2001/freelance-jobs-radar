# 🚀 Freelance Jobs Radar

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]()
[![Platform](https://img.shields.io/badge/Platforms-Mostaql%20%7C%20Kafiil%20%7C%20Nafezly%20%7C%20Khamsat%20%7C%20FreelanceYard-orange.svg)]()

An automated, intelligent monitoring radar and aggregation engine designed to harvest, filter, and score live freelance opportunities across major Arab & regional freelance platforms in real time.

Built to eliminate manual platform checking, enabling data professionals and freelancers to discover matching opportunities within minutes of posting and submit high-impact proposals before client fatigue sets in.

---

## 🎯 Target Specialization Niches

The engine continuously evaluates job postings across four core technical domains:

1. **Web Scraping & Data Extraction**: Python, BeautifulSoup, Scrapy, Selenium, Async Crawlers.
2. **Data Analysis & Business Intelligence**: Data Cleaning, Pandas, Excel Modeling, Power BI Dashboards, Sales Analytics.
3. **Automation & Scripting**: Workflow Automation, Python Bots, Telegram Integration, n8n, Scheduled Tasks.
4. **E-Commerce Store Setup**: Store Design, Shopify, Salla, Zid, WooCommerce, Product Ingestion.

---

## 🏗 System Architecture

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                Freelance Jobs Radar Pipeline                │
 └──────────────────────────────┬──────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
 ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
 │ Mostaql /    │        │ Kafiil /     │        │ Freelance-   │
 │ Khamsat      │        │ Nafezly      │        │ Yard         │
 └──────┬───────┘        └──────┬───────┘        └──────┬───────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                 ┌─────────────────────────────┐
                 │    BaseScraper Interface    │
                 │   (Session, Retry, UTF-8)   │
                 └──────────────┬──────────────┘
                                ▼
                 ┌─────────────────────────────┐
                 │     Smart Filter Engine     │
                 │  - Multi-Keyword Frequency  │
                 │  - Weighted Title Scoring   │
                 │  - Domain Classification    │
                 └──────────────┬──────────────┘
                                ▼
                 ┌─────────────────────────────┐
                 │     History Deduplication   │
                 │  (Tracks ID Map in JSON)    │
                 └──────────────┬──────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
 ┌──────────────┐                                ┌──────────────┐
 │  Local Out:  │                                │ Telegram Bot │
 │  MD & JSON   │                                │ Instant Push │
 └──────────────┘                                └──────────────┘
```

---

## ✨ Key Features

- **Multi-Platform Regional Coverage**: Scrapes Mostaql, Kafiil, Nafezly, Khamsat (Community Requests), and FreelanceYard with modular, decoupled parsers.
- **Weighted Relevance Scoring**: Assigns higher importance to title keywords vs. body snippets, sorting opportunities by relevance.
- **Stateful Deduplication**: Built-in `history_tracker` records past job identifiers so subsequent executions only notify you about genuine new postings.
- **Dual Output Channels**:
  - **Console Table**: Formatted CLI grid with ANSI color indicators.
  - **Markdown Digest**: Clean, clickable Markdown report (`data/latest_matches.md`).
  - **Structured JSON**: Machine-readable feed (`data/latest_matches.json`) for downstream dashboards.
  - **Telegram Instant Push**: Delivers formatted job alerts directly to your mobile device.
- **Windows Friendly**: Built-in UTF-8 console normalization preventing `UnicodeEncodeError` on legacy Arabic Windows code pages.

---

## 📁 Repository Structure

```text
freelance-jobs-radar/
├── scrapers/
│   ├── base_scraper.py         # Base class with requests session and error handling
│   ├── mostaql.py              # Mostaql projects scraper
│   ├── kafiil.py               # Kafiil projects scraper
│   ├── nafezly.py              # Nafezly projects scraper
│   ├── khamsat.py              # Khamsat community requests scraper
│   └── freelanceyard.py        # FreelanceYard job scraper
├── core/
│   ├── filter_engine.py        # Keyword evaluator & scoring algorithm
│   └── history_tracker.py      # JSON state management for seen job IDs
├── notifiers/
│   ├── local_reporter.py       # Console table & Markdown/JSON generator
│   └── telegram_notifier.py    # Telegram Bot API notification engine
├── data/
│   ├── history.json            # Indexed jobs cache (auto-generated)
│   ├── latest_matches.md       # Clickable Markdown digest
│   └── latest_matches.json     # Raw structured JSON export
├── config.py                   # Central settings, URLs & keyword dictionaries
├── main.py                     # CLI entry point and execution orchestrator
├── run.bat                     # Windows one-click execution script
├── HOW_TO_RUN.md               # Detailed bilingual execution manual
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # Project documentation
```

---

## ⚡ Quickstart

### 1. Installation

```bash
git clone https://github.com/mn3m2001/freelance-jobs-radar.git
cd freelance-jobs-radar
pip install -r requirements.txt
```

### 2. Basic Execution

```bash
# Run radar (notifies on new jobs only)
python main.py

# Or double-click run.bat on Windows
```

### 3. Advanced CLI Options

```bash
# Display all currently matching jobs, bypassing history
python main.py --all

# Scan a single platform
python main.py --platform mostaql

# Filter by custom minimum relevance score
python main.py --min-score 3

# Disable alerts or history updates
python main.py --no-alert --no-save
```

---

## 📱 Telegram Alerts (Optional)

Receive instant mobile notifications whenever a matching job drops:

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy your token.
2. Get your numeric ID with [@userinfobot](https://t.me/userinfobot).
3. Create a `.env` file from `.env.example`:
   ```env
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHI...
   TELEGRAM_CHAT_ID=987654321
   ```
4. Run `python main.py`—new matching leads will trigger instant phone notifications.

---

## ⏰ Automated Scheduling

To automate the radar every 3 hours:
- **Windows**: Use `Task Scheduler` pointing to `python.exe main.py` in the project directory.
- **Linux / macOS**: Add a cron entry:
  ```bash
  0 */3 * * * cd /path/to/freelance-jobs-radar && python3 main.py >> data/cron.log 2>&1
  ```

---

## 👤 Author

**Abdelmonem (`mn3m2001`)**  
*Data Analyst & Aspiring Data Scientist*  
- GitHub: [@mn3m2001](https://github.com/mn3m2001)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
