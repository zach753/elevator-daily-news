 """
 邮件构建模块

 将采集到的新闻组装成简洁的 HTML 邮件。
 用户要求：简洁版（标题 + 2-3句摘要 + 原文链接）
 """

 import logging
 from datetime import datetime, timezone, timedelta

 from .news_collector import Article

 logger = logging.getLogger(__name__)


 def _beijing_now() -> str:
     """获取北京时间字符串"""
     bj_tz = timezone(timedelta(hours=8))
     return datetime.now(bj_tz).strftime("%Y年%m月%d日 %A")


 def _build_article_list(articles: list[Article], lang_label: str) -> str:
     """生成一组文章的 HTML 列表"""
     if not articles:
         return f'<p style="color: #999; font-style: italic;">暂无 {lang_label} 新闻，自动跳过。</p>'

     items = []
     for i, art in enumerate(articles, 1):
         title = art.title or "(无标题)"
         url = art.url
         summary = art.summary or "点击标题查看全文"

         item = f"""
         <tr>
           <td style="padding: 12px 0 4px 0; border-bottom: 1px solid #eee;">
             <span style="color: #999; font-size: 12px;">{i:02d}.</span>
             <a href="{url}" target="_blank"
                style="color: #333; text-decoration: none; font-weight: bold; font-size: 14px;
                       line-height: 1.5;">
               {title}
             </a>
             <div style="color: #666; font-size: 13px; line-height: 1.6; margin: 4px 0 2px 0;">
               {summary}
             </div>
             <div style="color: #aaa; font-size: 11px; margin-bottom: 4px;">
               {art.source}
             </div>
           </td>
         </tr>
         """
         items.append(item)

     return """
     <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
     """ + "\n".join(items) + "\n     </table>"


 def build_newsletter_html(
     en_articles: list[Article],
     zh_articles: list[Article],
 ) -> str:
     """
     构建完整的 HTML 邮件内容。
     简洁版：标题 + 摘要 + 来源 + 链接
     """
     date_str = _beijing_now()
     total = len(en_articles) + len(zh_articles)

     en_section = _build_article_list(en_articles, "EN")
     zh_section = _build_article_list(zh_articles, "中文")

     html = f"""<!DOCTYPE html>
 <html>
 <head>
   <meta charset="utf-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
 </head>
 <body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;">

   <!-- 外层容器 -->
   <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5;">
     <tr>
       <td align="center" style="padding: 20px 10px;">
         <table width="600" cellpadding="0" cellspacing="0"
                style="max-width: 600px; width: 100%; background-color: #ffffff;
                       border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">

           <!-- 头部 -->
           <tr>
             <td style="background: linear-gradient(135deg, #1a365d, #2d6da8);
                        padding: 28px 30px 24px 30px;">
               <table width="100%" cellpadding="0" cellspacing="0">
                 <tr>
                   <td>
                     <div style="color: #ffffff; font-size: 22px; font-weight: bold; letter-spacing: 1px;">
                       🏗️ 每日电梯新闻
                     </div>
                     <div style="color: rgba(255,255,255,0.75); font-size: 13px; margin-top: 6px;">
                       {date_str} · 共 {total} 篇 · 中英双语
                     </div>
                   </td>
                 </tr>
               </table>
             </td>
           </tr>

           <!-- 内容区 -->
           <tr>
             <td style="padding: 24px 30px 10px 30px;">

               <!-- English Section -->
               <div style="margin-bottom: 24px;">
                 <div style="font-size: 15px; font-weight: bold; color: #1a365d;
                             padding-bottom: 8px; border-bottom: 2px solid #1a365d; margin-bottom: 8px;">
                   🌍 English News
                 </div>
                 {en_section}
               </div>

               <!-- Divider -->
               <div style="height: 1px; background: #e0e0e0; margin: 16px 0;"></div>

               <!-- Chinese Section -->
               <div style="margin-bottom: 24px;">
                 <div style="font-size: 15px; font-weight: bold; color: #c0392b;
                             padding-bottom: 8px; border-bottom: 2px solid #c0392b; margin-bottom: 8px;">
                   🇨🇳 中文新闻
                 </div>
                 {zh_section}
               </div>

             </td>
           </tr>

           <!-- 底部 -->
           <tr>
             <td style="background-color: #fafafa; padding: 20px 30px;
                        border-top: 1px solid #eee;">
               <table width="100%" cellpadding="0" cellspacing="0">
                 <tr>
                   <td style="font-size: 12px; color: #999; line-height: 1.6;">
                     本邮件由 Elevator Daily News 自动生成 ·
                     数据来源：elevatorworld.com / 百度新闻 / 36氪等<br>
                     如有问题请联系：noah30@qq.com
                   </td>
                 </tr>
               </table>
             </td>
           </tr>

         </table>
       </td>
     </tr>
   </table>

 </body>
 </html>"""

     return html


 def build_plain_text(
     en_articles: list[Article],
     zh_articles: list[Article],
 ) -> str:
     """生成纯文本版本（备用/调试用）"""
     lines = []
     lines.append("=" * 50)
     lines.append(f"  每日电梯新闻 - {_beijing_now()}")
     lines.append("=" * 50)
     lines.append("")

     lines.append("--- English News ---")
     for i, art in enumerate(en_articles, 1):
         lines.append(f"{i:02d}. {art.title}")
         lines.append(f"     {art.summary}")
         lines.append(f"     {art.url}")
         lines.append("")

     lines.append("--- 中文新闻 ---")
     for i, art in enumerate(zh_articles, 1):
         lines.append(f"{i:02d}. {art.title}")
         lines.append(f"     {art.summary}")
         lines.append(f"     {art.url}")
         lines.append("")

     return "\n".join(lines)
