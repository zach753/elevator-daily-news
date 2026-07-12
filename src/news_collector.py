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

_session = requests.Session()
_session.headers.update({"User-Agent": "Mozilla/5.0 Chrome/125", "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"})
_TIMEOUT = 20

def _fetch_page(url):
    try:
        resp = _session.get(url, timeout=_TIMEOUT)
        resp.raise_for_status(); return resp.text
    except Exception as e:
        logger.warning("Failed %s: %s", url, e); return None

def _clean_summary(text, max_len=300):
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len].rsplit(" ", 1)[0] + "..." if len(text) > max_len else text

def collect_elevatorworld_rss(rss_urls):
    articles = []; seen = set()
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            if not feed.entries: continue
            for e in feed.entries:
                link = e.get("link","")
                if not link or link in seen: continue
                seen.add(link)
                articles.append(Article(title=e.get("title","").strip(), url=link,
                    summary=_clean_summary(e.get("summary",e.get("description","")),250),
                    source="elevatorworld.com (RSS)", published=e.get("published"), language="en"))
            if articles: break
        except Exception as e: logger.warning("RSS fail %s: %s", url, e)
    return articles

def collect_english_news(config):
    arts = collect_elevatorworld_rss(config.ELEVATOR_WORLD_RSS)
    if len(arts) < 3:
        for u in [config.ELEVATOR_WORLD_NEWS_URL, config.ELEVATOR_WORLD_INDUSTRY_URL]:
            if len(arts) >= 3: break
            html = _fetch_page(u)
            if not html: continue
            soup = BeautifulSoup(html, "lxml")
            items = soup.select("article") or []
            for item in items[:10]:
                t = item.find(["h1","h2","h3"])
                if not t: continue
                a = t.find("a") if t else item.find("a")
                if not a: continue
                url = a.get("href",""); title = a.get_text(strip=True)
                if not title or not url: continue
                p = item.find("p")
                arts.append(Article(title=title, url=url, summary=_clean_summary(p.get_text() if p else "",250), source="elevatorworld.com", language="en"))
    seen = set(); uniq = []
    for a in arts:
        if a.url not in seen: seen.add(a.url); uniq.append(a)
    return uniq[:config.MAX_ARTICLES_ENGLISH]

def collect_chinese_news(config):
    arts = []
    for kw in config.BAIDU_NEWS_KEYWORDS[:3]:
        html = _fetch_page(f"https://news.baidu.com/ns?word={quote_plus(kw)}&pn=0&rn=10&cl=2&ct=1&tn=newstitle&ie=utf-8")
        if not html: continue
        soup = BeautifulSoup(html, "lxml")
        for div in soup.select(".result, .result-item, li")[:3]:
            a = div.find("a")
            if not a: continue
            h = a.get("href",""); t = a.get_text(strip=True)
            if not t or not h: continue
            arts.append(Article(title=t, url=h, source=f"Baidu-{kw}", language="zh"))
    seen = set(); uniq = []
    for a in arts:
        n = a.url.rstrip("/")
        if n not in seen: seen.add(n); uniq.append(a)
    return uniq[:config.MAX_ARTICLES_CHINESE]

def collect_all_news(config):
    logger.info("=== English ===")
    en = collect_english_news(config)
    logger.info("Got %d EN", len(en))
    logger.info("=== Chinese ===")
    zh = collect_chinese_news(config)
    logger.info("Got %d ZH", len(zh))
    return en, zh
