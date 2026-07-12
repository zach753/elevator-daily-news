"""Multi-source elevator news collector using cloudscraper."""
import logging, re, sys
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote_plus, urlparse
import feedparser, cloudscraper
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class Article:
    title: str = ""
    url: str = ""
    summary: str = ""
    source: str = ""
    language: str = "en"


_scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "desktop": True}
)


def _fetch(url, timeout=25):
    try:
        r = _scraper.get(url, timeout=timeout)
        logger.info("GET %s -> %d (%d b)", url, r.status_code, len(r.text))
        return r.text if r.status_code == 200 else None
    except Exception as e:
        logger.warning("FAIL %s: %s", url, e)
        return None


def _clean(text, max_len=300):
    if not text: return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\\s+", " ", text).strip()
    return (text[:max_len].rsplit(" ", 1)[0] + "...") if len(text) > max_len else text


# ================================================================
# RSS helpers
# ================================================================
def _try_rss(urls, source_name, lang="en", max_items=10):
    arts, seen = [], set()
    for url in urls:
        try:
            raw = _fetch(url)
            if not raw: continue
            feed = feedparser.parse(raw)
            entries = getattr(feed, "entries", [])
            if not entries: continue
            logger.info("RSS OK %s: %d entries", url, len(entries))
            for e in entries[:max_items]:
                link = e.get("link", "")
                if not link or link in seen: continue
                seen.add(link)
                arts.append(Article(title=e.get("title","").strip(), url=link,
                    summary=_clean(e.get("summary",e.get("description","")),250),
                    source=source_name, language=lang))
            if arts: break
        except Exception as ex:
            logger.warning("RSS err %s: %s", url, ex)
    return arts


def _scrape_links(url, source_name, min_title=15, lang="en", link_filter=None):
    html = _fetch(url)
    if not html: return []
    soup = BeautifulSoup(html, "lxml")
    arts, seen = [], set()
    for a in soup.find_all("a", href=True):
        t = a.get_text(strip=True)
        h = a["href"]
        if not t or not h or len(t) < min_title: continue
        if h.startswith("/"):
            pr = urlparse(url)
            h = f"{pr.scheme}://{pr.netloc}{h}"
        if h in seen: continue
        seen.add(h)
        arts.append(Article(title=t, url=h, source=source_name, language=lang))
    logger.info("Scraped %d links from %s", len(arts), url)
    return arts


# ================================================================
# 1. Elevator World
# ================================================================
def collect_elevatorworld(config):
    ew = config.ELEVATOR_WORLD
    arts = _try_rss(ew.get("rss_urls",[]), "Elevator World (RSS)")
    if len(arts) < 3:
        arts += _scrape_links(ew["news_url"], "Elevator World", min_title=20)
    if len(arts) < 3:
        arts += _scrape_links(ew["url"], "Elevator World", min_title=20)
    return arts


# ================================================================
# 2. International Associations
# ================================================================
def collect_associations(config):
    arts = []
    for assoc in config.INTL_ASSOCIATIONS:
        name = assoc.get("name","").split("(")[0].strip()
        urls = assoc.get("rss_urls",[])
        if urls:
            arts += _try_rss(urls, name)
        if len(arts) < 12:
            arts += _scrape_links(assoc["url"], name, min_title=20)
    return arts


# ================================================================
# 3. Chinese official sources (try RSS + scrape)
# ================================================================
def collect_china_sources(config):
    arts = []
    for src in config.CHINA_SOURCES:
        name = src["name"].split("-")[0].strip()
        urls = src.get("rss_urls",[])
        if urls:
            arts += _try_rss(urls, name, lang="zh")
        arts += _scrape_links(src["url"], name, min_title=10, lang="zh")
    # Dedup
    seen = set()
    uniq = []
    for a in arts:
        if a.url not in seen:
            seen.add(a.url); uniq.append(a)
    return uniq


# ================================================================
# 4. Bing News search
# ================================================================
def search_bing_news(keywords, label):
    arts, seen = [], set()
    q = " ".join(kw for kw in keywords if not kw.startswith("site:"))[:3]
    if not q: return arts
    html = _fetch(f"https://www.bing.com/news/search?q={quote_plus(q)}&FORM=HDRSC7")
    if not html: return arts
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all("a", href=True):
        t = a.get_text(strip=True); h = a["href"]
        if not t or not h or len(t) < 10 or h in seen: continue
        seen.add(h)
        lang = "zh" if max(ord(c) for c in t) > 0x2e80 else "en"
        arts.append(Article(title=t, url=h, source=label, language=lang))
    return arts


def collect_search_news(config):
    kws = config.SEARCH_KEYWORDS
    ch_kws = [k for k in kws if not k.startswith("site:") and max(ord(c) for c in k) > 0x2e80]
    en_kws = [k for k in kws if not k.startswith("site:") and "\\u4e00" not in repr(k)]
    en = search_bing_news(en_kws, "Bing News EN")
    zh = search_bing_news(ch_kws, "Bing News ZH")
    return en, zh


# ================================================================
# Main entry
# ================================================================
def collect_all_news(config):
    en_arts, zh_arts = [], []

    logger.info("=== Elevator World ===")
    en_arts += collect_elevatorworld(config)

    logger.info("=== Associations ===")
    en_arts += collect_associations(config)

    logger.info("=== China Sources ===")
    zh_arts += collect_china_sources(config)

    logger.info("=== Bing Search ===")
    en_s, zh_s = collect_search_news(config)
    en_arts += en_s; zh_arts += zh_s

    # Dedup
    seen_en, seen_zh = set(), set()
    en = []
    for a in en_arts:
        if a.url not in seen_en:
            seen_en.add(a.url); en.append(a)
    zh = []
    for a in zh_arts:
        if a.url not in seen_zh:
            seen_zh.add(a.url); zh.append(a)

    logger.info("FINAL: EN=%d ZH=%d", len(en), len(zh))
    return en[:config.MAX_ARTICLES_ENGLISH], zh[:config.MAX_ARTICLES_CHINESE]

