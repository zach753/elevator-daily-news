"""
 閭欢鍙戦€佹ā鍧?
 閫氳繃 QQ 閭 SMTP 鍙戦€佹瘡鏃ユ柊闂婚偖浠躲€? 鏀寔 SSL 鍔犲瘑杩炴帴锛岄渶浣跨敤鎺堟潈鐮佽€岄潪瀵嗙爜銆? """

 import logging
 import smtplib
 from email.mime.multipart import MIMEMultipart
 from email.mime.text import MIMEText
 from email.header import Header

 logger = logging.getLogger(__name__)


 def send_email(
     config,
     html_body: str,
     plain_body: str = "",
 ) -> bool:
     """
     鍙戦€侀偖浠?
     Args:
         config: 閰嶇疆妯″潡锛堝寘鍚?QQ_EMAIL, QQ_EMAIL_AUTH_CODE, NEWS_RECEIVER 绛夛級
         html_body: HTML 鏍煎紡閭欢鍐呭
         plain_body: 绾枃鏈牸寮忛偖浠跺唴瀹癸紙澶囩敤锛?
     Returns:
         bool: 鍙戦€佹槸鍚︽垚鍔?     """
     if not config.QQ_EMAIL_AUTH_CODE:
         logger.error("QQ_EMAIL_AUTH_CODE 鏈厤缃紒璇峰厛璁剧疆 GitHub Secrets銆?)
         return False

     # 鏋勫缓閭欢
     msg = MIMEMultipart("alternative")
     msg["From"] = f"Elevator Daily News <{config.QQ_EMAIL}>"
     msg["To"] = config.NEWS_RECEIVER
     msg["Subject"] = Header(
         "馃彈锔?姣忔棩鐢垫鏂伴椈 - Elevator Daily News",
         "utf-8",
     )

     # 绾枃鏈鐢?     if plain_body:
         msg.attach(MIMEText(plain_body, "plain", "utf-8"))

     # HTML 涓诲唴瀹?     msg.attach(MIMEText(html_body, "html", "utf-8"))

     # 鍙戦€?     try:
         logger.info(
             "Connecting to %s:%s (SSL)...",
             config.SMTP_SERVER,
             config.SMTP_PORT,
         )
         with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT, timeout=30) as server:
             server.login(config.QQ_EMAIL, config.QQ_EMAIL_AUTH_CODE)
             server.send_message(msg)

         logger.info(
             "Email sent successfully to %s",
             config.NEWS_RECEIVER,
         )
         return True

     except smtplib.SMTPAuthenticationError:
         logger.error(
             "QQ 閭璁よ瘉澶辫触锛佽妫€鏌ユ巿鏉冪爜鏄惁姝ｇ‘銆俓n"
             "鑾峰彇鏂瑰紡锛氱櫥褰?mail.qq.com 鈫?璁剧疆 鈫?璐︽埛 鈫?寮€鍚?POP3/SMTP 鈫?鐢熸垚鎺堟潈鐮?
         )
         return False
     except smtplib.SMTPException as e:
         logger.error("SMTP 鍙戦€佸け璐? %s", e)
         return False
     except Exception as e:
         logger.error("鍙戦€侀偖浠舵椂鍙戠敓鏈煡閿欒: %s", e)
         return False
