import logging
import smtplib
import requests
from typing import Optional


from config import SMS_API_URL_TEMPLATE, SMS_SENDER, SMTP_HOST, SMTP_PORT

class Notifier:
    def __init__(self, sms_api_key: str, sms_sender: str, smtp_user: str, smtp_password: str):
        self.sms_api_key = "A99a4ff3208f168c703ca2f60ad450088"
        self.sms_sender = 'BVCSHC'
        self.smtp_user = "bhavansclg09@gmail.com"
        self.smtp_password = "wtlxuvshwuxafxwj"


    def send_sms(self, phone: str, message: str) -> None:
        if not self.sms_api_key:
            logging.warning("SMS API key not set; skipping SMS to %s", phone)
            return
        url = SMS_API_URL_TEMPLATE.format(api_key=self.sms_api_key, sender=self.sms_sender, phone=phone)
        payload = {
            "authorization": self.sms_api_key,
            "message": message,
            "language": "english",
            "route": "q",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        headers = {"cache-control": "no-cache"}
        try:
            requests.request("POST", url, headers=headers, params=payload, timeout=10)
        except Exception as exc:
            logging.warning("Failed to send SMS to %s: %s", phone, exc)

    def send_email(self, recipient: str, message: str) -> None:
        if not self.smtp_user or not self.smtp_password:
            logging.warning("SMTP credentials not set; skipping email to %s", recipient)
            return
        try:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.smtp_user, recipient, message)
            server.quit()
        except Exception as exc:
            logging.warning("Failed to send email to %s: %s", recipient, exc)