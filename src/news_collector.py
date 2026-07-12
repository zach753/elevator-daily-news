"""News collection module."""
import logging, re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote_plus
import feedparser, requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class Article:
    title: str = ""
    url: str = ""
    summary: str = ""
    source: str = ""
    published: Optional[str] = None
    language: str = "en"


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
}
TIMEOUT = 30


def _fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        logger.info("Fetched OK: %s (%d bytes)", url, len(r.text))
        return r.text
    except Exception as e:
        logger.warning("Fetch FAILED: %s - %s", url, e)
        return None


def _clean(text, max_len=300):
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\\s+", " ", text).strip()
    return text[:max_len].rsplit(" ", 1)[0] + "..." if len(text) > max_len else text


def collect_elevatorworld_rss(urls):
    articles = []
    seen = set()
    for url in urls:
        try:
            feed = feedparser.parse(url)
            logger.info("RSS feed %s: %d entries", url, len(feed.entries))
            if not feed.entries:
                continue
            for e in feed.entries:
                link = e.get("link", "")
                if not link or link in seen:
                    continue
                seen.add(link)
                articles.append(Article(
                    title=e.get("title", "").strip(), url=link,
                    summary=_clean(e.get("summary", e.get("description", "")), 250),
                    source="elevatorworld.com (RSS)", published=e.get("published"), language="en"))
            if articles:
                logger.info("Got %d articles from %s", len(articles), url)
                break
        except Exception as e:
            logger.warning("RSS error %s: %s", url, e)
    return articles


def collect_elevatorworld_scrape(url):
    html = _fetch(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "lxml")
    articles = []
    for tag in soup.find_all(["article", "div"], class_=re.compile(r"post|entry|article", re.I)):
        h = tag.find(["h1", "h2", "h3", "h4"])
        if not h:
            continue
        a = h.find("a") if h else tag.find("a")
        if not a:
            continue
        title = a.get_text(strip=True)
        href = a.get("href", "")
        if not title or not href:
            continue
        p = tag.find("p")
        articles.append(Article(title=title, url=href, summary=_clean(p.get_text() if p else "", 250), source="elevatorworld.com", language="en"))
    if not articles:
        for a in soup.find_all("a", href=re.compile(r"elevatorworld")):
            t = a.get_text(strip=True)
            h = a.get("href", "")
            if t and h and len(t) > 10:
                articles.append(Article(title=t, url=h, source="elevatorworld.com", language="en"))
    logger.info("Scraped %d articles from %s", len(articles), url)
    return articles


def collect_english_news(config):
    arts = collect_elevatorworld_rss(config.ELEVATOR_WORLD_RSS)
    if len(arts) < 3:
        arts += collect_elevatorworld_scrape(config.ELEVATOR_WORLD_NEWS_URL)
    if len(arts) < 3:
        arts += collect_elevatorworld_scrape(config.ELEVATOR_WORLD_INDUSTRY_URL)
    seen = set()
    uniq = []
    for a in arts:
        if a.url not in seen:
            seen.add(a.url)
            uniq.append(a)
    return uniq[:config.MAX_ARTICLES_ENGLISH]


def collect_baidu_news(keywords):
    arts = []
    seen = set()
    for kw in keywords[:3]:
        url = f"https://news.baidu.com/ns?word={quote_plus(kw)}&pn=0&rn=10&cl=2&ct=1&tn=newstitle&ie=utf-8"
        html = _fetch(url)
        if not html:
            continue
        soup = BeautifulSoup(html, "lxml")
        for div in soup.select(".result, .result-item, h3"):
            a = div.find("a") if div.name != "a" else div
            if a is None:
                a = div
            if a.name != "a":
                a = a.find("a")
            if not a:
                continue
            href = a.get("href", "")
            title = a.get_text(strip=True)
            if not title or not href or href in seen:
                continue
            seen.add(href)
            arts.append(Article(title=title, url=href, source=f"Baidu-{kw}", language="zh"))
    logger.info("Got %d baidu news articles", len(arts))
    return arts


def collect_chinese_news(config):
    arts = collect_baidu_news(config.BAIDU_NEWS_KEYWORDS)
    seen = set()
    uniq = []
    for a in arts:
        n = a.url.rstrip("/")
        if n not in seen:
            seen.add(n)
            uniq.append(a)
    return uniq[:config.MAX_ARTICLES_CHINESE]


def collect_all_news(config):
    logger.info("=== English ===")
    en = collect_english_news(config)
    logger.info("EN total: %d", len(en))
    logger.info("=== Chinese ===")
    zh = collect_chinese_news(config)
    logger.info("ZH total: %d", len(zh))
    return en, zh
