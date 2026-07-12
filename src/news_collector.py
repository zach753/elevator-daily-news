 """
 新闻采集模块

 负责从多个来源采集电梯行业新闻：
 - 英文源: elevatorworld.com (RSS + HTML 抓取)
 - 中文源: 百度新闻搜索、行业网站等
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
     """一篇文章的数据模型"""
     title: str
     url: str
     summary: str = ""
     source: str = ""
     published: Optional[str] = None
     language: str = "en"  # "en" or "zh"


 # =============================================================
 # 通用工具
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
     """安全地获取页面内容"""
     try:
         resp = _session.get(url, timeout=_TIMEOUT)
         resp.raise_for_status()
         return resp.text
     except Exception as e:
         logger.warning("Failed to fetch %s: %s", url, e)
         return None


 def _clean_summary(text: str, max_len: int = 300) -> str:
     """清理 HTML 标签并截取摘要"""
     text = re.sub(r"<[^>]+>", "", text)
     text = re.sub(r"\s+", " ", text).strip()
     if len(text) > max_len:
         text = text[:max_len].rsplit(" ", 1)[0] + "..."
     return text


 # =============================================================
 # 英文源采集器
 # =============================================================

 def collect_elevatorworld_rss(rss_urls: list[str]) -> list[Article]:
     """通过 RSS 从 elevatorworld.com 采集新闻"""
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
                 break  # 取到 RSS 就不再尝试下一个
         except Exception as e:
             logger.warning("RSS parse failed for %s: %s", rss_url, e)

     return articles


 def collect_elevatorworld_scrape(news_url: str) -> list[Article]:
     """通过 HTML 抓取 elevatorworld.com 新闻（RSS 备份方案）"""
     html = _fetch_page(news_url)
     if not html:
         return []

     articles = []
     soup = BeautifulSoup(html, "lxml")

     # 尝试多种文章选择器（WordPress 主题各异）
     selectors = [
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

         # 摘要
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
     """采集所有英文源新闻"""
     articles = []

     # 1. elevatorworld RSS
     articles.extend(collect_elevatorworld_rss(config.ELEVATOR_WORLD_RSS))

     # 2. 如果 RSS 没取到，尝试 HTML 抓取
     if len(articles) < 3:
         articles.extend(collect_elevatorworld_scrape(config.ELEVATOR_WORLD_NEWS_URL))

     if len(articles) < 3:
         articles.extend(collect_elevatorworld_scrape(config.ELEVATOR_WORLD_INDUSTRY_URL))

     # 3. 去重 & 截断
     seen = set()
     unique = []
     for a in articles:
         if a.url not in seen:
             seen.add(a.url)
             unique.append(a)

     return unique[:config.MAX_ARTICLES_ENGLISH]


 # =============================================================
 # 中文源采集器
 # =============================================================

 def collect_baidu_news(keywords: list[str], max_per_keyword: int = 3) -> list[Article]:
     """从百度新闻搜索电梯相关新闻"""
     articles = []
     seen_urls = set()

     for keyword in keywords[:3]:  # 只取前3个关键词避免重复
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

             # 找摘要
             summary_tag = div.find(["p", ".c-summary", ".summary", ".abstract"])
             summary = _clean_summary(
                 summary_tag.get_text() if summary_tag else "",
                 max_len=200,
             )

             articles.append(Article(
                 title=title,
                 url=href,
                 summary=summary,
                 source=f"百度新闻 - {keyword}",
                 language="zh",
             ))
             count += 1

         logger.info("Got %d baidu news for keyword '%s'", count, keyword)

     return articles


 def collect_industry_news(keywords: list[str]) -> list[Article]:
     """从行业网站采集中文电梯新闻（扩展用）"""
     articles = []

     # 36氪搜索
     for keyword in keywords[:2]:
         encoded = quote_plus(f"{keyword} 电梯")
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
                 source="36氪",
                 language="zh",
             ))
             count += 1
         logger.info("Got %d articles from 36kr for '%s'", count, keyword)

     return articles


 def collect_chinese_news(config) -> list[Article]:
     """采集所有中文源新闻"""
     articles = []

     articles.extend(collect_baidu_news(config.BAIDU_NEWS_KEYWORDS))

     if len(articles) < 3:
         articles.extend(collect_industry_news(["电梯"]))

     # 去重
     seen = set()
     unique = []
     for a in articles:
         norm_url = a.url.rstrip("/")
         if norm_url not in seen:
             seen.add(norm_url)
             unique.append(a)

     return unique[:config.MAX_ARTICLES_CHINESE]


 # =============================================================
 # 统一入口
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
