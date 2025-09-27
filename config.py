import os

# Database configuration
DB_CONFIG = {
"host": os.getenv("EAUTH_DB_HOST", "localhost"),
"port": int(os.getenv("EAUTH_DB_PORT", 1813)),
"user": os.getenv("EAUTH_DB_USER", "user1"),
"password": os.getenv("EAUTH_DB_PASSWORD", "password123"),
"database": os.getenv("EAUTH_DB_NAME", "authentication"),
}


# Camera (IP webcam) OR scanner URL
CAMERA_URL = os.getenv("EAUTH_CAMERA_URL", "http://192.168.29.216:8080/video")


# SMS provider settings
SMS_API_KEY = os.getenv("EAUTH_SMS_API_KEY", "")
SMS_SENDER = os.getenv("EAUTH_SMS_SENDER", "BVCSHC")
SMS_API_URL_TEMPLATE = (
"https://alerts.solutionsinfini.com/api/v4/?method=sms"
"&api_key={api_key}&sender={sender}&to={phone}"
)


# SMTP settings
SMTP_HOST = os.getenv("EAUTH_SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("EAUTH_SMTP_PORT", 587))
SMTP_USER = os.getenv("EAUTH_SMTP_USER", "")
SMTP_APP_PASSWORD = os.getenv("EAUTH_SMTP_PASSWORD", "")


# OTP configuration
OTP_LENGTH = int(os.getenv("EAUTH_OTP_LENGTH", 6))