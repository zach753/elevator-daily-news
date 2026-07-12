"""Email sender via QQ SMTP."""
import logging, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

logger = logging.getLogger(__name__)

def send_email(config, html_body, plain_body=""):
    if not config.QQ_EMAIL_AUTH_CODE:
        logger.error("QQ_EMAIL_AUTH_CODE not configured!")
        return False
    msg = MIMEMultipart("alternative")
    msg["From"] = f"Elevator Daily News <{config.QQ_EMAIL}>"
    msg["To"] = config.NEWS_RECEIVER
    msg["Subject"] = Header("Elevator Daily News - Daily Digest", "utf-8")
    if plain_body:
        msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    try:
        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT, timeout=30) as s:
            s.login(config.QQ_EMAIL, config.QQ_EMAIL_AUTH_CODE)
            s.send_message(msg)
        logger.info("Email sent to %s", config.NEWS_RECEIVER)
        return True
    except smtplib.SMTPAuthenticationError:
        logger.error("QQ email auth failed. Check your auth code."); return False
    except Exception as e:
        logger.error("Send failed: %s", e); return False
