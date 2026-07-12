 """
 电梯每日新闻推送 - 配置文件

 使用方法：
 1. 将此文件复制为 config.py（如果已经是 config.py 则直接编辑）
 2. 填写下方的 QQ 邮箱配置
 3. GitHub Actions 中通过 Repository Secrets 注入以下变量：
    - QQ_EMAIL: 你的 QQ 邮箱地址
    - QQ_EMAIL_AUTH_CODE: QQ 邮箱授权码（非登录密码）
    - NEWS_RECEIVER: 接收新闻的邮箱地址（可填同一个）

 获取 QQ 邮箱授权码的步骤：
 1. 登录 mail.qq.com → 设置 → 账户
 2. 找到 "POP3/SMTP服务" → 开启
 3. 按照指引发送短信获取授权码（16位字母）
 """

 import os


 # ============================================================
 # 邮箱配置（通过环境变量读取，GitHub Secrets 注入）
 # ============================================================
 QQ_EMAIL = os.environ.get("QQ_EMAIL", "noah30@qq.com")
 QQ_EMAIL_AUTH_CODE = os.environ.get("QQ_EMAIL_AUTH_CODE", "")
 NEWS_RECEIVER = os.environ.get("NEWS_RECEIVER", QQ_EMAIL)

 SMTP_SERVER = "smtp.qq.com"
 SMTP_PORT = 465  # SSL


 # ============================================================
 # 新闻源配置
 # ============================================================

 # ---- 英文源 (50%) ----
 ELEVATOR_WORLD_RSS = [
     "https://www.elevatorworld.com/feed/",
     "https://www.elevatorworld.com/rss/",
     "https://www.elevatorworld.com/rss2/",
 ]
 ELEVATOR_WORLD_NEWS_URL = "https://www.elevatorworld.com/category/news/"
 ELEVATOR_WORLD_INDUSTRY_URL = "https://www.elevatorworld.com/category/industry-news/"

 # 其他英文电梯行业源
 OTHER_ENGLISH_RSS = [
     # 可扩展：添加其他英文电梯行业 RSS
 ]

 # ---- 中文源 (50%) ----
 BAIDU_NEWS_KEYWORDS = [
     "电梯",
     "电梯行业",
     "电梯招标",
     "电梯出口",
     "电梯外贸",
     "elevator",
 ]

 # 电梯公司新闻页面
 ELEVATOR_COMPANY_NEWS = [
     # 这些网站结构不同，需要分别适配爬虫
     # 后续版本可以逐个添加
 ]

 # 招标信息
 BIDDING_URLS = [
     # 中国采招网 / 招标网等
 ]


 # ============================================================
 # 推送配置
 # ============================================================
 MAX_ARTICLES_ENGLISH = 6   # 每次推送最多英文条数
 MAX_ARTICLES_CHINESE = 6   # 每次推送最多中文条数
 NEWS_LANGUAGE_MIX = 0.5    # 中英文比例 50/50
