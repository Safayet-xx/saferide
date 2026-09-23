"""
All settings come from environment variables.
Locally they are read from the .env file in the project root (copy .env.example to start).
On Render, set them in the dashboard (or render.yaml) instead.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env(key: str, default: str = "") -> str:
    # An empty value (e.g. "SENDGRID_API_KEY=" in .env) counts as not set
    return (os.getenv(key) or "").strip() or default


def env_bool(key: str, default: bool = False) -> bool:
    return env(key, str(default)).lower() in ("1", "true", "yes", "on")


def env_list(key: str, default: str = "") -> list[str]:
    return [item.strip() for item in env(key, default).split(",") if item.strip()]


APP_ENV = env("APP_ENV", "production")
ADMIN_KEY = env("ADMIN_KEY")
CORS_ORIGINS = env_list("CORS_ORIGINS")
ENABLE_API_DOCS = env_bool("ENABLE_API_DOCS", False)
# Customer-entered pickup times are read in this timezone (used to reject past bookings)
TIMEZONE = env("TIMEZONE", "Europe/London")

# ---- Email ----
# "sendgrid" sends real email. "console" only prints emails in the server log (for local testing).
# Left empty, it picks sendgrid when SENDGRID_API_KEY is set, otherwise console.
SENDGRID_API_KEY = env("SENDGRID_API_KEY")
EMAIL_PROVIDER = env("EMAIL_PROVIDER", "sendgrid" if SENDGRID_API_KEY else "console").lower()
# Must be an address verified in SendGrid (Single Sender Verification or a verified domain)
SENDGRID_FROM_EMAIL = env("SENDGRID_FROM_EMAIL")
SENDGRID_FROM_NAME = env("SENDGRID_FROM_NAME")
SENDGRID_API_URL = env("SENDGRID_API_URL", "https://api.sendgrid.com/v3/mail/send")
# Where new bookings and messages are sent. Comma-separated for more than one inbox.
BOOKINGS_EMAIL_TO = env_list("BOOKINGS_EMAIL_TO")
# Also email the customer a "we've got your request" confirmation
SEND_CUSTOMER_CONFIRMATION = env_bool("SEND_CUSTOMER_CONFIRMATION", True)

BRAND = {
    "name": env("BRAND_NAME", "SafeRide Airport Taxis"),
    "legal_name": env("BRAND_LEGAL_NAME", "SafeRide Airport Taxis Limited"),
    "tagline": env("BRAND_TAGLINE", "Airport transfers, day and night."),
    "phone": env("BRAND_PHONE", "01234 567890"),
    "whatsapp": env("BRAND_WHATSAPP", "01234 567890"),
    "email": env("BRAND_EMAIL", "hello@example.com"),
    "address": env("BRAND_ADDRESS", "1 Example Street, Your Town, AB1 2CD"),
    "app_links": {
        "ios": env("APP_LINK_IOS", "#"),
        "android": env("APP_LINK_ANDROID", "#"),
    },
    "socials": {
        "Facebook": env("SOCIAL_FACEBOOK", "#"),
        "Instagram": env("SOCIAL_INSTAGRAM", "#"),
        "X": env("SOCIAL_X", "#"),
        "LinkedIn": env("SOCIAL_LINKEDIN", "#"),
        "TikTok": env("SOCIAL_TIKTOK", "#"),
    },
}

if not SENDGRID_FROM_NAME:
    SENDGRID_FROM_NAME = BRAND["name"]
