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
    return os.getenv(key, default).strip()


def env_bool(key: str, default: bool = False) -> bool:
    return env(key, str(default)).lower() in ("1", "true", "yes", "on")


def env_list(key: str, default: str = "") -> list[str]:
    return [item.strip() for item in env(key, default).split(",") if item.strip()]


APP_ENV = env("APP_ENV", "production")
ADMIN_KEY = env("ADMIN_KEY")
CORS_ORIGINS = env_list("CORS_ORIGINS")
ENABLE_API_DOCS = env_bool("ENABLE_API_DOCS", False)

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
