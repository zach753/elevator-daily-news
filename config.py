"""Elevator Daily News - Configuration

All verified elevator industry sources (domestic + international).
"""
import os

QQ_EMAIL = os.environ.get("QQ_EMAIL", "noah30@qq.com")
QQ_EMAIL_AUTH_CODE = os.environ.get("QQ_EMAIL_AUTH_CODE", "")
NEWS_RECEIVER = os.environ.get("NEWS_RECEIVER", QQ_EMAIL)
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465

CHINA_OFFICIAL = {"name": "China Elevator Assoc", "url": "http://www.elevator.org.cn", "rss_urls": []}
CHINA_ELEVATOR_MAG = {"name": "China Elevator Mag", "url": "http://www.chinaelevator.org", "rss_urls": []}
CHINA_BICM = {"name": "BICM Infoport", "url": "https://www.bicm.com.cn", "rss_urls": []}
CHINA_SAMR = {"name": "SAMR Special Equipment", "url": "https://www.samr.gov.cn/tzsbj", "rss_urls": []}
CHINA_EXPO = {"name": "China Elevator Expo", "url": "http://association.elevator-expo.com", "rss_urls": []}
CHINA_SOURCES = [CHINA_OFFICIAL, CHINA_ELEVATOR_MAG, CHINA_BICM, CHINA_SAMR, CHINA_EXPO]

ELA = {"name": "ELA Europe (EN81)", "url": "https://www.ela-aisbl.eu", "rss_urls": ["https://www.ela-aisbl.eu/feed/"]}
IRAM = {"name": "IRAM Argentina", "url": "https://www.iram.org.ar", "rss_urls": []}
NAEC = {"name": "NAEC USA (ASME A17.1)", "url": "https://www.naec.org", "rss_urls": ["https://www.naec.org/feed/"]}
ABNT = {"name": "ABNT Brazil", "url": "https://www.abnt.org.br", "rss_urls": []}
INTL_ASSOCIATIONS = [ELA, IRAM, NAEC, ABNT]

ELEVATOR_WORLD = {"name": "Elevator World", "url": "https://www.elevatorworld.com", "news_url": "https://www.elevatorworld.com/category/news/", "industry_url": "https://www.elevatorworld.com/category/industry-news/", "rss_urls": ["https://www.elevatorworld.com/feed/", "https://www.elevatorworld.com/rss/", "https://elevatorworld.com/feed/"]}

INTERLIFT = {"name": "Interlift Germany", "url": "https://www.interlift.de/en", "rss_urls": []}
NAEC_CONF = {"name": "NAEC Conference", "url": "https://www.naec.org/conference/", "rss_urls": []}
EXHIBITIONS = [INTERLIFT, NAEC_CONF]

VOLZA = {"name": "Volza B/L data", "url": "https://www.volza.com"}
TENDATA = {"name": "Tendata customs", "url": "https://www.tendata.cn"}
TRADE_DATA = [VOLZA, TENDATA]

CEN = {"name": "CEN (EN81)", "url": "https://www.cen.eu", "rss_urls": []}
EU_STANDARDS = [CEN]

SEARCH_KEYWORDS = ["elevator export","elevator industry","elevator China","EN81 elevator","Argentina elevator","Brazil elevator","电梯出口","电梯行业","电梯招标"]
SITE_SEARCH_QUERIES = ["site:ela-aisbl.eu elevator","site:elevator.org.cn elevator"]

MAX_ARTICLES_ENGLISH = 6
MAX_ARTICLES_CHINESE = 6
