"""
 鏂伴椈閲囬泦妯″潡

 璐熻矗浠庡涓潵婧愰噰闆嗙數姊涓氭柊闂伙細
 - 鑻辨枃婧? elevatorworld.com (RSS + HTML 鎶撳彇)
 - 涓枃婧? 鐧惧害鏂伴椈鎼滅储銆佽涓氱綉绔欑瓑
 """

 import logging
 import re
 from dataclasses import dataclass, field
 from datetime import datetime, timezone
 from typing import Optional
 from urllib.parse import quote_plus

 import feedparser
 import requests
 from bs4 import BeautifulSoup

 logger = logging.getLogger(__name__)


 @dataclass
 class Article:
     """涓€绡囨枃绔犵殑鏁版嵁妯″瀷"""
     title: str
     url: str
     summary: str = ""
     source: str = ""
     published: Optional[str] = None
     language: str = "en"  # "en" or "zh"


 # =============================================================
 # 閫氱敤宸ュ叿
 # =============================================================

 _session = requests.Session()
 _session.headers.update({
     "User-Agent": (
         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
         "AppleWebKit/537.36 (KHTML, like Gecko) "
         "Chrome/125.0.0.0 Safari/537.36"
     ),
     "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
 })

 _TIMEOUT = 20  # seconds


 def _fetch_page(url: str) -> Optional[str]:
     """瀹夊叏鍦拌幏鍙栭〉闈㈠唴瀹?""
     try:
         resp = _session.get(url, timeout=_TIMEOUT)
         resp.raise_for_status()
         return resp.text
     except Exception as e:
         logger.warning("Failed to fetch %s: %s", url, e)
         return None


 def _clean_summary(text: str, max_len: int = 300) -> str:
     """娓呯悊 HTML 鏍囩骞舵埅鍙栨憳瑕?""
     text = re.sub(r"<[^>]+>", "", text)
     text = re.sub(r"\s+", " ", text).strip()
     if len(text) > max_len:
         text = text[:max_len].rsplit(" ", 1)[0] + "..."
     return text


 # =============================================================
 # 鑻辨枃婧愰噰闆嗗櫒
 # =============================================================

 def collect_elevatorworld_rss(rss_urls: list[str]) -> list[Article]:
     """閫氳繃 RSS 浠?elevatorworld.com 閲囬泦鏂伴椈"""
     articles = []
     seen_urls = set()

     for rss_url in rss_urls:
         try:
             feed = feedparser.parse(rss_url)
             if not feed.entries:
                 continue
             for entry in feed.entries:
                 url = entry.get("link", "")
                 if not url or url in seen_urls:
                     continue
                 seen_urls.add(url)
                 title = entry.get("title", "").strip()
                 summary = _clean_summary(
                     entry.get("summary", entry.get("description", "")),
                     max_len=250,
                 )
                 published = entry.get("published")
                 articles.append(Article(
                     title=title,
                     url=url,
                     summary=summary,
                     source="elevatorworld.com (RSS)",
                     published=published,
                     language="en",
                 ))
             if articles:
                 logger.info("Got %d articles from RSS: %s", len(articles), rss_url)
                 break  # 鍙栧埌 RSS 灏变笉鍐嶅皾璇曚笅涓€涓?         except Exception as e:
             logger.warning("RSS parse failed for %s: %s", rss_url, e)

     return articles


 def collect_elevatorworld_scrape(news_url: str) -> list[Article]:
     """閫氳繃 HTML 鎶撳彇 elevatorworld.com 鏂伴椈锛圧SS 澶囦唤鏂规锛?""
     html = _fetch_page(news_url)
     if not html:
         return []

     articles = []
     soup = BeautifulSoup(html, "lxml")

     # 灏濊瘯澶氱鏂囩珷閫夋嫨鍣紙WordPress 涓婚鍚勫紓锛?     selectors = [
         "article", "div.post", "div.entry", ".post-content",
         ".entry-content", "div[class*='post']",
     ]
     for selector in selectors:
         items = soup.select(selector)
         if len(items) >= 3:
             break
     else:
         items = soup.find_all("article") or []

     for item in items[:15]:
         title_tag = item.find(["h1", "h2", "h3", "h4"])
         if not title_tag:
             continue
         link_tag = title_tag.find("a") if title_tag else None
         if link_tag:
             url = link_tag.get("href", "")
             title = link_tag.get_text(strip=True)
         else:
             url = item.find("a")
             url = url.get("href", "") if url else ""
             title = title_tag.get_text(strip=True)

         if not title or not url:
             continue

         # 鎽樿
         excerpt = item.find(["p", "div.excerpt", ".entry-summary"])
         summary = _clean_summary(
             excerpt.get_text() if excerpt else "",
             max_len=250,
         )

         articles.append(Article(
             title=title,
             url=url,
             summary=summary,
             source="elevatorworld.com",
             language="en",
         ))

     logger.info("Scraped %d articles from %s", len(articles), news_url)
     return articles


 def collect_english_news(config) -> list[Article]:
     """閲囬泦鎵€鏈夎嫳鏂囨簮鏂伴椈"""
     articles = []

     # 1. elevatorworld RSS
     articles.extend(collect_elevatorworld_rss(config.ELEVATOR_WORLD_RSS))

     # 2. 濡傛灉 RSS 娌″彇鍒帮紝灏濊瘯 HTML 鎶撳彇
     if len(articles) < 3:
         articles.extend(collect_elevatorworld_scrape(config.ELEVATOR_WORLD_NEWS_URL))

     if len(articles) < 3:
         articles.extend(collect_elevatorworld_scrape(config.ELEVATOR_WORLD_INDUSTRY_URL))

     # 3. 鍘婚噸 & 鎴柇
     seen = set()
     unique = []
     for a in articles:
         if a.url not in seen:
             seen.add(a.url)
             unique.append(a)

     return unique[:config.MAX_ARTICLES_ENGLISH]


 # =============================================================
 # 涓枃婧愰噰闆嗗櫒
 # =============================================================

 def collect_baidu_news(keywords: list[str], max_per_keyword: int = 3) -> list[Article]:
     """浠庣櫨搴︽柊闂绘悳绱㈢數姊浉鍏虫柊闂?""
     articles = []
     seen_urls = set()

     for keyword in keywords[:3]:  # 鍙彇鍓?涓叧閿瘝閬垮厤閲嶅
         encoded = quote_plus(keyword)
         url = (
             f"https://news.baidu.com/ns?word={encoded}"
             f"&pn=0&rn=10&cl=2&ct=1&tn=newstitle&ie=utf-8"
         )
         html = _fetch_page(url)
         if not html:
             continue

         soup = BeautifulSoup(html, "lxml")
         result_divs = soup.select(".result, .result-item, li")

         count = 0
         for div in result_divs:
             if count >= max_per_keyword:
                 break

             link = div.find("a")
             if not link:
                 continue

             href = link.get("href", "")
             title = link.get_text(strip=True)
             if not title or not href or href in seen_urls:
                 continue

             seen_urls.add(href)

             # 鎵炬憳瑕?             summary_tag = div.find(["p", ".c-summary", ".summary", ".abstract"])
             summary = _clean_summary(
                 summary_tag.get_text() if summary_tag else "",
                 max_len=200,
             )

             articles.append(Article(
                 title=title,
                 url=href,
                 summary=summary,
                 source=f"鐧惧害鏂伴椈 - {keyword}",
                 language="zh",
             ))
             count += 1

         logger.info("Got %d baidu news for keyword '%s'", count, keyword)

     return articles


 def collect_industry_news(keywords: list[str]) -> list[Article]:
     """浠庤涓氱綉绔欓噰闆嗕腑鏂囩數姊柊闂伙紙鎵╁睍鐢級"""
     articles = []

     # 36姘悳绱?     for keyword in keywords[:2]:
         encoded = quote_plus(f"{keyword} 鐢垫")
         url = f"https://36kr.com/search/articles/{encoded}"
         html = _fetch_page(url)
         if not html:
             continue

         soup = BeautifulSoup(html, "lxml")
         items = soup.select("a[class*='title'], .article-item-title, h3 a, .kr-search-result-item a")
         count = 0
         for item in items[:5]:
             title = item.get_text(strip=True)
             href = item.get("href", "")
             if not title or not href:
                 continue
             if href.startswith("/"):
                 href = "https://36kr.com" + href
             articles.append(Article(
                 title=title,
                 url=href,
                 source="36姘?,
                 language="zh",
             ))
             count += 1
         logger.info("Got %d articles from 36kr for '%s'", count, keyword)

     return articles


 def collect_chinese_news(config) -> list[Article]:
     """閲囬泦鎵€鏈変腑鏂囨簮鏂伴椈"""
     articles = []

     articles.extend(collect_baidu_news(config.BAIDU_NEWS_KEYWORDS))

     if len(articles) < 3:
         articles.extend(collect_industry_news(["鐢垫"]))

     # 鍘婚噸
     seen = set()
     unique = []
     for a in articles:
         norm_url = a.url.rstrip("/")
         if norm_url not in seen:
             seen.add(norm_url)
             unique.append(a)

     return unique[:config.MAX_ARTICLES_CHINESE]


 # =============================================================
 # 缁熶竴鍏ュ彛
 # =============================================================

 def collect_all_news(config) -> tuple[list[Article], list[Article]]:
     """
     Collect news from all sources.
     Returns (english_articles, chinese_articles)
     """
     logger.info("=== Starting English news collection ===")
     en_articles = collect_english_news(config)
     logger.info("English articles collected: %d", len(en_articles))

     logger.info("=== Starting Chinese news collection ===")
     zh_articles = collect_chinese_news(config)
     logger.info("Chinese articles collected: %d", len(zh_articles))

     return en_articles, zh_articles
