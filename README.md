# 🏗️ Elevator Daily News - 每日电梯新闻推送

每天北京时间 **07:00** 自动推送电梯行业新闻到你的邮箱。
无需保持电脑开机，代码运行在 **GitHub Actions** 云端。

## 功能特点

- 🌍 **英文源** — elevatorworld.com（RSS + 网页抓取），可扩展更多
- 🇨🇳 **中文源** — 百度新闻搜索 + 行业网站（36氪等），可扩展
- 📧 **邮件推送** — 简洁版每日摘要（标题 + 摘要 + 原文链接）
- ⚖️ **中英均衡** — 默认各 50%
- ☁️ **云端运行** — 基于 GitHub Actions 免费定时任务，关电脑也能跑

## 部署步骤

### 第一步：获取 QQ 邮箱授权码

1. 打开 https://mail.qq.com → 登录 **noah30@qq.com**
2. 设置 → 账户 → POP3/SMTP服务 → **开启**
3. 按照指引发送短信 → 获取 16 位授权码（**不是你的QQ密码**）

### 第二步：推送到 GitHub

```bash
# 1. 打开终端（在项目目录下）
cd elevator-daily-news

# 2. 初始化 Git
git init
git add .
git commit -m "🎉 init: elevator daily news system"

# 3. 在 GitHub 上创建一个新仓库（不要勾选 README）
#    https://github.com/new
#    仓库名：elevator-daily-news

# 4. 推送到 GitHub
git remote add origin https://github.com/你的用户名/elevator-daily-news.git
git branch -M main
git push -u origin main
```

### 第三步：配置 GitHub Secrets

1. 打开你的 GitHub 仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**，添加以下三个 Secret：

| Secret 名称            | 值                          |
|------------------------|----------------------------|
| QQ_EMAIL               | noah30@qq.com              |
| QQ_EMAIL_AUTH_CODE     | 你获取的 16 位授权码         |
| NEWS_RECEIVER          | noah30@qq.com              |

### 第四步：验证

1. 回到仓库 → **Actions** 标签页
2. 在左侧找到 **Daily Elevator Newsletter**
3. 点击 **Run workflow** → **Run workflow**（手动跑一次测试）
4. 等 1-2 分钟运行完成，检查 **noah30@qq.com** 收件箱

之后每天北京时间 07:00 会自动运行，无需任何操作。

## 本地测试（可选）

```bash
cd elevator-daily-news
pip install -r requirements.txt
set QQ_EMAIL_AUTH_CODE=你的16位授权码
python run.py
```

## 扩展更多新闻源

编辑 `config.py`，在对应列表中添加即可：

```python
# 添加更多英文 RSS
OTHER_ENGLISH_RSS = ["https://another-site.com/feed/"]

# 添加更多中文搜索关键词
BAIDU_NEWS_KEYWORDS = ["电梯出口", "家用电梯", "电梯维保"]
```

## 技术栈

- Python 3.12 + requests / BeautifulSoup / feedparser
- GitHub Actions（schedule / cron）
- QQ 邮箱 SMTP（SSL 465）
- 邮件格式：HTML 多部分（纯文本备用）

---

*有问题？联系 noah30@qq.com 或在 GitHub 上提 Issue。*
