"""
Interactive / CLI Telegram Setup and Test Utility
"""

import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import requests

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

def test_and_save(bot_token: str, chat_id: str):
    bot_token = bot_token.strip()
    chat_id = chat_id.strip()

    print("[*] Testing connection to Telegram API...")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "🎉 <b>مبروك! تم ربط رادار وظائف الفريلانس بنجاح!</b>\n\nمن الآن ستصلك كل الفرص الجديدة أولاً بأول هنا على موبايلك.",
        "parse_mode": "HTML"
    }

    try:
        res = requests.post(url, json=payload, timeout=10)
        data = res.json()
        if data.get("ok"):
            print("[✓] Success! Test message sent to your Telegram.")
            with open(ENV_FILE, "w", encoding="utf-8") as f:
                f.write(f"TELEGRAM_BOT_TOKEN={bot_token}\n")
                f.write(f"TELEGRAM_CHAT_ID={chat_id}\n")
            print(f"[✓] Saved credentials to {ENV_FILE}")
            return True
        else:
            print(f"[ERROR] Telegram returned error: {data.get('description')}")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to reach Telegram: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) == 3:
        token = sys.argv[1]
        chat = sys.argv[2]
        test_and_save(token, chat)
    else:
        print("Usage: python setup_telegram.py <BOT_TOKEN> <CHAT_ID>")
