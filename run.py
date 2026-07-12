#!/usr/bin/env python3
"""每日电梯新闻推送 - 主入口

此脚本会被 GitHub Actions 每天早上定时执行：
1. 采集英文/中文电梯新闻
2. 组装成简洁的 HTML 邮件
3. 通过 QQ 邮箱 SMTP 发送

本地测试：
  set QQ_EMAIL_AUTH_CODE=your_auth_code
  python run.py
"""

import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from src.news_collector import collect_all_news
from src.newsletter_builder import build_newsletter_html, build_plain_text
from src.email_sender import send_email


def setup_logging():
    """配置日志输出到标准输出（GitHub Actions 可见）"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def main():
    setup_logging()
    logger = logging.getLogger("main")

    logger.info("=" * 50)
    logger.info("  Elevator Daily News - 开始采集")
    logger.info("=" * 50)

    en_articles, zh_articles = collect_all_news(config)

    logger.info("")
    logger.info("采集结果:")
    logger.info("  - 英文新闻: %d 篇", len(en_articles))
    logger.info("  - 中文新闻: %d 篇", len(zh_articles))
    logger.info("  - 合计: %d 篇", len(en_articles) + len(zh_articles))

    if not en_articles and not zh_articles:
        logger.warning("未获取到任何新闻，将发送空通知邮件")

    html_body = build_newsletter_html(en_articles, zh_articles)
    plain_body = build_plain_text(en_articles, zh_articles)

    logger.info("")
    logger.info("-" * 50)
    logger.info("发送邮件...")

    success = send_email(config, html_body, plain_body)

    if success:
        logger.info("")
        logger.info("✓ 邮件推送完成！")
    else:
        logger.error("✗ 邮件推送失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
