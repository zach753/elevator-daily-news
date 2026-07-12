\"\"\"Elevator Daily News - Configuration

All verified elevator industry sources (domestic + international).
\"\"\"

import os
# ============================================================
# Email Settings
# ============================================================
QQ_EMAIL = os.environ.get("QQ_EMAIL", "noah30@qq.com")
QQ_EMAIL_AUTH_CODE = os.environ.get("QQ_EMAIL_AUTH_CODE", "")
NEWS_RECEIVER = os.environ.get("NEWS_RECEIVER", QQ_EMAIL)
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465

# ============================================================
# Category 1: Chinese Official & Industry Sources
# ============================================================
CHINA_OFFICIAL = {
    "name": "涓浗鐢垫鍗忎細 - policy/standards/export",
    "url": "http://www.elevator.org.cn",
    "rss_urls": [],
}
CHINA_ELEVATOR_MAGAZINE = {
    "name": "涓浗鐢垫鏉傚織 - market/price/supply chain",
    "url": "http://www.chinaelevator.org",
    "rss_urls": [],
}
CHINA_BICM = {
    "name": "鐢垫淇℃伅娓?BICM - industry info",
    "url": "https://www.bicm.com.cn",
    "rss_urls": [],
}
CHINA_SAMR = {
    "name": "鍥藉甯傜洃鎬诲眬鐗圭璁惧灞€ - safety regulations",
    "url": "https://www.samr.gov.cn/tzsbj",
    "rss_urls": [],
}
CHINA_ELEVATOR_EXPO = {
    "name": "涓浗鍥介檯鐢垫灞?(biennial exhibition)",
    "url": "http://association.elevator-expo.com",
    "rss_urls": [],
}
CHINA_SOURCES = [CHINA_OFFICIAL, CHINA_ELEVATOR_MAGAZINE, CHINA_BICM, CHINA_SAMR, CHINA_ELEVATOR_EXPO]

# ============================================================
# Category 2: International Industry Associations
# ============================================================
ELA = {
    "name": "European Lift Association (EN81 standards)",
    "url": "https://www.ela-aisbl.eu",
    "rss_urls": ["https://www.ela-aisbl.eu/feed/", "https://www.ela-aisbl.eu/rss/"],
}
IRAM = {
    "name": "IRAM Argentina (elevator standards IRAM 3681)",
    "url": "https://www.iram.org.ar",
    "rss_urls": [],
}
NAEC = {
    "name": "NAEC USA (ASME A17.1 code)",
    "url": "https://www.naec.org",
    "rss_urls": ["https://www.naec.org/feed/", "https://www.naec.org/rss/"],
}
ABNT = {
    "name": "ABNT Brazil (Brazil elevator standards)",
    "url": "https://www.abnt.org.br",
    "rss_urls": [],
}
INTL_ASSOCIATIONS = [ELA, IRAM, NAEC, ABNT]

# ============================================================
# Category 3: Global Elevator Media
# ============================================================
ELEVATOR_WORLD = {
    "name": "Elevator World (global #1 elevator magazine)",
    "url": "https://www.elevatorworld.com",
    "news_url": "https://www.elevatorworld.com/category/news/",
    "industry_url": "https://www.elevatorworld.com/category/industry-news/",
    "rss_urls": [
        "https://www.elevatorworld.com/feed/",
        "https://www.elevatorworld.com/rss/",
        "https://www.elevatorworld.com/rss2/",
        "https://elevatorworld.com/feed/",
        "https://www.elevatorworld.com/feed/rss/",
        "https://www.elevatorworld.com/?feed=rss2",
    ],
}
GLOBAL_MEDIA = [ELEVATOR_WORLD]

# ============================================================
# Category 4: International Elevator Exhibitions
# ============================================================
INTERLIFT = {
    "name": "Interlift Germany (world's largest elevator expo)",
    "url": "https://www.interlift.de/en",
    "rss_urls": ["https://www.interlift.de/en/feed/"],
}
NAEC_CONFERENCE = {
    "name": "NAEC Annual Conference (North America market)",
    "url": "https://www.naec.org/conference/",
    "rss_urls": [],
}
EXHIBITIONS = [INTERLIFT, NAEC_CONFERENCE]

# ============================================================
# Category 5: Customs / Trade Data Platforms
# ============================================================
VOLZA = {
    "name": "Volza (global bill of lading data, HS 842810)",
    "url": "https://www.volza.com",
}
TENDATA = {
    "name": "Tendata (Chinese customs data platform)",
    "url": "https://www.tendata.cn",
}
TRADE_DATA = [VOLZA, TENDATA]

# ============================================================
# Category 6: EU Standards Official
# ============================================================
CEN = {
    "name": "CEN European Committee for Standardization (EN81)",
    "url": "https://www.cen.eu",
    "rss_urls": [],
}
EU_STANDARDS = [CEN]

# ============================================================
# Search keywords (Bing News / Google News)
# ============================================================
SEARCH_KEYWORDS = [
    # Chinese keywords
    "鐢垫鍑哄彛", "鐢垫琛屼笟", "鐢垫鎷涙爣", "鐢垫澶栬锤",
    "elevator export", "elevator China",
    # Elevator World
    "site:elevatorworld.com elevator",
    # International standards
    "EN81 elevator", "ASME A17.1 elevator",
    # Markets
    "Argentina elevator", "Brazil elevator", "South America elevator",
]

# For site-specific news searches
SITE_SEARCH_QUERIES = [
    "site:ela-aisbl.eu elevator",
    "site:naec.org elevator",
    "site:elevator.org.cn elevator",
    "site:chinaelevator.org elevator",
    "site:iram.org.ar ascensor",
]

# ============================================================
# Push Settings
# ============================================================
MAX_ARTICLES_ENGLISH = 6
MAX_ARTICLES_CHINESE = 6
