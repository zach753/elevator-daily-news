"""
 閭欢鏋勫缓妯″潡

 灏嗛噰闆嗗埌鐨勬柊闂荤粍瑁呮垚绠€娲佺殑 HTML 閭欢銆? 鐢ㄦ埛瑕佹眰锛氱畝娲佺増锛堟爣棰?+ 2-3鍙ユ憳瑕?+ 鍘熸枃閾炬帴锛? """

 import logging
 from datetime import datetime, timezone, timedelta

 from .news_collector import Article

 logger = logging.getLogger(__name__)


 def _beijing_now() -> str:
     """鑾峰彇鍖椾含鏃堕棿瀛楃涓?""
     bj_tz = timezone(timedelta(hours=8))
     return datetime.now(bj_tz).strftime("%Y骞?m鏈?d鏃?%A")


 def _build_article_list(articles: list[Article], lang_label: str) -> str:
     """鐢熸垚涓€缁勬枃绔犵殑 HTML 鍒楄〃"""
     if not articles:
         return f'<p style="color: #999; font-style: italic;">鏆傛棤 {lang_label} 鏂伴椈锛岃嚜鍔ㄨ烦杩囥€?/p>'

     items = []
     for i, art in enumerate(articles, 1):
         title = art.title or "(鏃犳爣棰?"
         url = art.url
         summary = art.summary or "鐐瑰嚮鏍囬鏌ョ湅鍏ㄦ枃"

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
     鏋勫缓瀹屾暣鐨?HTML 閭欢鍐呭銆?     绠€娲佺増锛氭爣棰?+ 鎽樿 + 鏉ユ簮 + 閾炬帴
     """
     date_str = _beijing_now()
     total = len(en_articles) + len(zh_articles)

     en_section = _build_article_list(en_articles, "EN")
     zh_section = _build_article_list(zh_articles, "涓枃")

     html = f"""<!DOCTYPE html>
 <html>
 <head>
   <meta charset="utf-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
 </head>
 <body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;">

   <!-- 澶栧眰瀹瑰櫒 -->
   <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5;">
     <tr>
       <td align="center" style="padding: 20px 10px;">
         <table width="600" cellpadding="0" cellspacing="0"
                style="max-width: 600px; width: 100%; background-color: #ffffff;
                       border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">

           <!-- 澶撮儴 -->
           <tr>
             <td style="background: linear-gradient(135deg, #1a365d, #2d6da8);
                        padding: 28px 30px 24px 30px;">
               <table width="100%" cellpadding="0" cellspacing="0">
                 <tr>
                   <td>
                     <div style="color: #ffffff; font-size: 22px; font-weight: bold; letter-spacing: 1px;">
                       馃彈锔?姣忔棩鐢垫鏂伴椈
                     </div>
                     <div style="color: rgba(255,255,255,0.75); font-size: 13px; margin-top: 6px;">
                       {date_str} 路 鍏?{total} 绡?路 涓嫳鍙岃
                     </div>
                   </td>
                 </tr>
               </table>
             </td>
           </tr>

           <!-- 鍐呭鍖?-->
           <tr>
             <td style="padding: 24px 30px 10px 30px;">

               <!-- English Section -->
               <div style="margin-bottom: 24px;">
                 <div style="font-size: 15px; font-weight: bold; color: #1a365d;
                             padding-bottom: 8px; border-bottom: 2px solid #1a365d; margin-bottom: 8px;">
                   馃實 English News
                 </div>
                 {en_section}
               </div>

               <!-- Divider -->
               <div style="height: 1px; background: #e0e0e0; margin: 16px 0;"></div>

               <!-- Chinese Section -->
               <div style="margin-bottom: 24px;">
                 <div style="font-size: 15px; font-weight: bold; color: #c0392b;
                             padding-bottom: 8px; border-bottom: 2px solid #c0392b; margin-bottom: 8px;">
                   馃嚚馃嚦 涓枃鏂伴椈
                 </div>
                 {zh_section}
               </div>

             </td>
           </tr>

           <!-- 搴曢儴 -->
           <tr>
             <td style="background-color: #fafafa; padding: 20px 30px;
                        border-top: 1px solid #eee;">
               <table width="100%" cellpadding="0" cellspacing="0">
                 <tr>
                   <td style="font-size: 12px; color: #999; line-height: 1.6;">
                     鏈偖浠剁敱 Elevator Daily News 鑷姩鐢熸垚 路
                     鏁版嵁鏉ユ簮锛歟levatorworld.com / 鐧惧害鏂伴椈 / 36姘瓑<br>
                     濡傛湁闂璇疯仈绯伙細noah30@qq.com
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
     """鐢熸垚绾枃鏈増鏈紙澶囩敤/璋冭瘯鐢級"""
     lines = []
     lines.append("=" * 50)
     lines.append(f"  姣忔棩鐢垫鏂伴椈 - {_beijing_now()}")
     lines.append("=" * 50)
     lines.append("")

     lines.append("--- English News ---")
     for i, art in enumerate(en_articles, 1):
         lines.append(f"{i:02d}. {art.title}")
         lines.append(f"     {art.summary}")
         lines.append(f"     {art.url}")
         lines.append("")

     lines.append("--- 涓枃鏂伴椈 ---")
     for i, art in enumerate(zh_articles, 1):
         lines.append(f"{i:02d}. {art.title}")
         lines.append(f"     {art.summary}")
         lines.append(f"     {art.url}")
         lines.append("")

     return "\n".join(lines)
