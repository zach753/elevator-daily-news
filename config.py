"""Elevator Daily News - Configuration

Usage:
  Set env vars via GitHub Secrets:
    QQ_EMAIL, QQ_EMAIL_AUTH_CODE, NEWS_RECEIVER

  To get QQ email auth code:
    1. Login mail.qq.com -> Settings -> Account
    2. Enable POP3/SMTP service
    3. Send SMS to get 16-char auth code
"""

import os


# ============================================================
# Email config (read from env vars / GitHub Secrets)
# ============================================================
QQ_EMAIL = os.environ.get("QQ_EMAIL", "noah30@qq.com")
QQ_EMAIL_AUTH_CODE = os.environ.get("QQ_EMAIL_AUTH_CODE", "")
NEWS_RECEIVER = os.environ.get("NEWS_RECEIVER", QQ_EMAIL)

SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465


# ============================================================
# News Sources
# ============================================================

# English sources
ELEVATOR_WORLD_RSS = [
    "https://www.elevatorworld.com/feed/",
    "https://www.elevatorworld.com/rss/",
    "https://www.elevatorworld.com/rss2/",
]
ELEVATOR_WORLD_NEWS_URL = "https://www.elevatorworld.com/category/news/"
ELEVATOR_WORLD_INDUSTRY_URL = "https://www.elevatorworld.com/category/industry-news/"

OTHER_ENGLISH_RSS = []

# Chinese sources
BAIDU_NEWS_KEYWORDS = [
    "电梯", "电梯行业", "电梯招标", "电梯出口", "电梯外贸", "elevator",
]

ELEVATOR_COMPANY_NEWS = []
BIDDING_URLS = []


# ============================================================
# Push Settings
# ============================================================
MAX_ARTICLES_ENGLISH = 6
MAX_ARTICLES_CHINESE = 6
NEWS_LANGUAGE_MIX = 0.5
