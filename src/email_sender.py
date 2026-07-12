 """
 邮件发送模块

 通过 QQ 邮箱 SMTP 发送每日新闻邮件。
 支持 SSL 加密连接，需使用授权码而非密码。
 """

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
     发送邮件

     Args:
         config: 配置模块（包含 QQ_EMAIL, QQ_EMAIL_AUTH_CODE, NEWS_RECEIVER 等）
         html_body: HTML 格式邮件内容
         plain_body: 纯文本格式邮件内容（备用）

     Returns:
         bool: 发送是否成功
     """
     if not config.QQ_EMAIL_AUTH_CODE:
         logger.error("QQ_EMAIL_AUTH_CODE 未配置！请先设置 GitHub Secrets。")
         return False

     # 构建邮件
     msg = MIMEMultipart("alternative")
     msg["From"] = f"Elevator Daily News <{config.QQ_EMAIL}>"
     msg["To"] = config.NEWS_RECEIVER
     msg["Subject"] = Header(
         "🏗️ 每日电梯新闻 - Elevator Daily News",
         "utf-8",
     )

     # 纯文本备用
     if plain_body:
         msg.attach(MIMEText(plain_body, "plain", "utf-8"))

     # HTML 主内容
     msg.attach(MIMEText(html_body, "html", "utf-8"))

     # 发送
     try:
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
             "QQ 邮箱认证失败！请检查授权码是否正确。\n"
             "获取方式：登录 mail.qq.com → 设置 → 账户 → 开启 POP3/SMTP → 生成授权码"
         )
         return False
     except smtplib.SMTPException as e:
         logger.error("SMTP 发送失败: %s", e)
         return False
     except Exception as e:
         logger.error("发送邮件时发生未知错误: %s", e)
         return False
