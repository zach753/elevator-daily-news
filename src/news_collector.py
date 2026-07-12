"""News collection module - uses cloudscraper to bypass Cloudflare."""
import logging, re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote_plus
import feedparser
import cloudscraper
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

@dataclass
class Article:
    title: str = ""
    url: str = ""
    summary: str = ""
    source: str = ""
    language: str = "en"

# cloudscraper mimics a real browser to bypass Cloudflare
_scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "desktop": True}
)

def _fetch(url):
    try:
        r = _scraper.get(url, timeout=30)
        logger.info("Fetch %s -> %d (%d bytes)", url, r.status_code, len(r.text))
        if r.status_code == 200:
            return r.text
        logger.warning("Status %d for %s", r.status_code, url)
        return None
    except Exception as e:
        logger.warning("Fetch FAILED %s: %s", url, e)
        return None

def _clean(text, max_len=300):
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\\s+", " ", text).strip()
    return text[:max_len].rsplit(" ", 1)[0] + "..." if len(text) > max_len else text

# ================================================================
# English: elevatorworld.com
# ================================================================

def collect_elevatorworld():
    """Use cloudscraper to get elevatorworld.com content."""
    articles = []
    seen = set()

    # Try RSS feeds first
    rss_urls = [
        "https://www.elevatorworld.com/feed/",
        "https://www.elevatorworld.com/rss/",
        "https://www.elevatorworld.com/rss2/",
        "https://elevatorworld.com/feed/",
        "https://www.elevatorworld.com/feed/rss/",
        "https://www.elevatorworld.com/?feed=rss2",
    ]

    for rss_url in rss_urls:
        try:
            raw = _fetch(rss_url)
            if not raw:
                continue
            feed = feedparser.parse(raw)
            entries = getattr(feed, "entries", [])
            logger.info("RSS %s: %d entries", rss_url, len(entries))
            if not entries:
                # Might be HTML (Cloudflare passed but not RSS)
                if "<rss" not in raw and "<feed" not in raw:
                    logger.info("Not RSS, trying next feed URL")
                    continue
            for e in entries:
                link = e.get("link", "")
                if not link or link in seen:
                    continue
                seen.add(link)
                articles.append(Article(
                    title=e.get("title", "").strip(), url=link,
                    summary=_clean(e.get("summary", e.get("description", "")), 250),
                    source="elevatorworld.com", language="en"))
            if articles:
                logger.info("Got %d articles from %s", len(articles), rss_url)
                break
        except Exception as ex:
            logger.warning("RSS error %s: %s", rss_url, ex)

    # Fallback: scrape homepage
    if len(articles) < 3:
        html = _fetch("https://www.elevatorworld.com/")
        if html:
            soup = BeautifulSoup(html, "lxml")
            for a_tag in soup.find_all("a", href=True):
                t = a_tag.get_text(strip=True)
                h = a_tag["href"]
                if not t or not h or len(t) < 15:
                    continue
                if "/20" in h or "/article" in h.lower() or "/news" in h.lower():
                    if h.startswith("/"):
                        h = "https://www.elevatorworld.com" + h
                    if h not in seen:
                        seen.add(h)
                        articles.append(Article(title=t, url=h, source="elevatorworld.com", language="en"))
            logger.info("Scraped homepage: %d articles", len(articles))

    return articles

# ================================================================
# Chinese: Bing News + Baidu fallback
# ================================================================

def collect_chinese_news_bing(keywords):
    """Search Bing News for elevator news."""
    articles = []
    seen = set()
    query = " ".join(keywords[:2])
    url = f"https://www.bing.com/news/search?q={quote_plus(query)}&FORM=HDRSC7"
    html = _fetch(url)
    if not html:
        return articles
    soup = BeautifulSoup(html, "lxml")
    for card in soup.select(".news-card, .topic-card, a[href*='https://']"):
        a_tag = card if card.name == "a" else card.find("a")
        if not a_tag:
            continue
        h = a_tag.get("href", "")
        t = a_tag.get_text(strip=True)
        if not t or not h or h in seen:
            continue
        seen.add(h)
        articles.append(Article(title=t, url=h, source="Bing News", language="zh"))
    # Also try regular title links
    for a_tag in soup.find_all("a", href=True):
        t = a_tag.get_text(strip=True)
        h = a_tag["href"]
        if not t or not h or len(t) < 10 or h in seen:
            continue
        if "news" in h.lower() or "bing" in h.lower():
            seen.add(h)
            articles.append(Article(title=t, url=h, source="Bing News", language="zh"))
    logger.info("Bing News: %d articles", len(articles))
    return articles

def collect_chinese_news_baidu(keywords):
    """Baidu News fallback."""
    articles = []
    seen = set()
    for kw in keywords[:1]:
        html = _fetch(f"https://news.baidu.com/ns?word={quote_plus(kw)}&pn=0&rn=10&cl=2&ct=1&tn=newstitle&ie=utf-8")
        if not html:
            continue
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all("a", href=True):
            h = a["href"]
            t = a.get_text(strip=True)
            if not t or not h or h in seen:
                continue
            seen.add(h)
            articles.append(Article(title=t, url=h, source="Baidu News", language="zh"))
    logger.info("Baidu News: %d articles", len(articles))
    return articles

def collect_chinese_news(config):
    arts = collect_chinese_news_bing(config.BAIDU_NEWS_KEYWORDS)
    if len(arts) < 2:
        arts += collect_chinese_news_baidu(config.BAIDU_NEWS_KEYWORDS)
    seen = set()
    uniq = []
    for a in arts:
        n = a.url.rstrip("/")
        if n not in seen:
            seen.add(n); uniq.append(a)
    return uniq[:config.MAX_ARTICLES_CHINESE]

# ================================================================
# Main entry
# ================================================================

def collect_all_news(config):
    logger.info("=== English ===")
    en = collect_elevatorworld()
    logger.info("EN total: %d", len(en))
    logger.info("=== Chinese ===")
    zh = collect_chinese_news(config)
    logger.info("ZH total: %d", len(zh))
    return en, zh
