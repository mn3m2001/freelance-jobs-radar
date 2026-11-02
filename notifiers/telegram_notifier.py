"""
Telegram Alert Notifier
"""

import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ENABLE_TELEGRAM


class TelegramNotifier:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.enabled = ENABLE_TELEGRAM

    def send_job_alert(self, job: dict) -> bool:
        if not self.enabled:
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        categories_text = ", ".join(job.get("categories", []))

        message = (
            f"🎯 <b>فرصة عمل جديدة متطابقة!</b>\n\n"
            f"📌 <b>العنوان:</b> <a href=\"{job.get('url')}\">{job.get('title')}</a>\n"
            f"🏢 <b>المنصة:</b> {job.get('platform_name')}\n"
            f"🏷 <b>التصنيف:</b> {categories_text}\n"
            f"💰 <b>الميزانية:</b> {job.get('budget', 'غير محدد')}\n"
            f"⏰ <b>الوقت:</b> {job.get('time_posted', 'جديد')}\n\n"
            f"🔗 <a href=\"{job.get('url')}\">اضغط هنا لفتح المشروع والتقديم فوراً</a>"
        )

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }

        try:
            res = requests.post(url, json=payload, timeout=10)
            return res.status_code == 200
        except Exception as e:
            print(f"[TelegramNotifier] Error sending alert: {e}")
            return False

    def send_batch_alerts(self, jobs: list) -> int:
        if not self.enabled or not jobs:
            return 0

        sent_count = 0
        for j in jobs:
            if self.send_job_alert(j):
                sent_count += 1
        return sent_count
