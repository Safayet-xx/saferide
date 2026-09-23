import logging
import re
import secrets
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator, model_validator

from backend import config, emailer
from backend.content import SITE

DIST_DIR = config.BASE_DIR / "frontend" / "dist"

# /docs and /redoc are only exposed when ENABLE_API_DOCS=true
app = FastAPI(
    title=f"{config.BRAND['name']} API",
    docs_url="/docs" if config.ENABLE_API_DOCS else None,
    redoc_url="/redoc" if config.ENABLE_API_DOCS else None,
    openapi_url="/openapi.json" if config.ENABLE_API_DOCS else None,
)

# Only needed when running React on the Vite dev server.
# In production React is served by this same app, so CORS_ORIGINS can stay empty.
if config.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

log = logging.getLogger("uvicorn.error")
TZ = ZoneInfo(config.TIMEZONE)

for problem in emailer.check_setup():
    log.warning("Email setup: %s", problem)
if config.EMAIL_PROVIDER == "console":
    log.warning("EMAIL_PROVIDER=console: bookings are only printed in this log, no email is sent")

# Copies of recent submissions for the admin endpoints. They reset whenever the server restarts;
# the email sent for each submission is the permanent record.
QUOTES = []
MESSAGES = []

VEHICLES = {v["id"]: v for v in SITE["vehicles"]}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^\+?[0-9 ()-]{7,20}$")
CONTACT_TOPICS = ("General", "Personal account", "Business account", "Driving for us", "Lost property", "Feedback")
EMAIL_FAILED = "We couldn't send your request just now. Please try again or call us on {phone}."


def clean_email(value: str) -> str:
    value = value.strip()
    if not EMAIL_PATTERN.match(value):
        raise ValueError("Enter a valid email address")
    return value


def clean_phone(value: str) -> str:
    value = value.strip()
    if value and not PHONE_PATTERN.match(value):
        raise ValueError("Enter a valid phone number")
    return value


class QuoteRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=200)
    phone: str = Field(min_length=1, max_length=30)
    pickup_address: str = Field(min_length=1, max_length=300)
    pickup_postcode: str = Field(default="", max_length=12)
    # Sent by <input type="datetime-local"> as "2026-09-25T12:30", in UK local time
    pickup_datetime: datetime
    destination_address: str = Field(min_length=1, max_length=300)
    dropoff_postcode: str = Field(default="", max_length=12)
    vehicle: str
    passengers: int = Field(ge=1, le=16)
    luggage: str = Field(default="", max_length=200)
    journey_type: Literal["one_way", "return"] = "one_way"
    return_pickup_address: str = Field(default="", max_length=300)
    return_pickup_datetime: Optional[datetime] = None

    _email = field_validator("email")(clean_email)
    _phone = field_validator("phone")(clean_phone)

    @field_validator("return_pickup_datetime", mode="before")
    @classmethod
    def blank_is_none(cls, value):
        return value or None

    @model_validator(mode="after")
    def check_journey(self):
        now = datetime.now(TZ).replace(tzinfo=None)
        if self.pickup_datetime.replace(tzinfo=None) < now:
            raise ValueError("Pickup time must be in the future")
        vehicle = VEHICLES.get(self.vehicle)
        if not vehicle:
            raise ValueError("Choose a vehicle from the list")
        if self.passengers > vehicle["seats"]:
            raise ValueError(f"The {vehicle['name']} seats up to {vehicle['seats']}. Choose a bigger vehicle.")
        if self.journey_type == "return":
            if not self.return_pickup_datetime:
                raise ValueError("Add a date and time for the return journey")
            if self.return_pickup_datetime.replace(tzinfo=None) <= self.pickup_datetime.replace(tzinfo=None):
                raise ValueError("The return journey must be after the outward pickup")
        else:
            self.return_pickup_address = ""
            self.return_pickup_datetime = None
        return self


class ContactMessage(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=200)
    phone: str = Field(default="", max_length=30)
    topic: Literal[CONTACT_TOPICS] = "General"
    message: str = Field(min_length=1, max_length=3000)

    _email = field_validator("email")(clean_email)
    _phone = field_validator("phone")(clean_phone)


def check_admin(key: Optional[str]):
    if not config.ADMIN_KEY or not key or not secrets.compare_digest(key, config.ADMIN_KEY):
        raise HTTPException(status_code=403, detail="Not allowed")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/site")
def site():
    return SITE


@app.post("/api/quotes", status_code=201)
def create_quote(quote: QuoteRequest):
    reference = uuid.uuid4().hex[:8].upper()
    try:
        emailer.send_quote_emails(reference, quote, VEHICLES[quote.vehicle]["name"])
    except emailer.EmailError as err:
        log.error("Booking %s email failed: %s", reference, err)
        raise HTTPException(status_code=502, detail=EMAIL_FAILED.format(phone=config.BRAND["phone"]))

    QUOTES.append({
        "reference": reference,
        "created_at": datetime.now(timezone.utc).isoformat(),
        **quote.model_dump(mode="json"),
    })
    return {"reference": reference, "message": "Quote request received. We'll be in touch with your price shortly."}


@app.post("/api/messages", status_code=201)
def create_message(msg: ContactMessage):
    try:
        emailer.send_message_email(msg)
    except emailer.EmailError as err:
        log.error("Message email failed: %s", err)
        raise HTTPException(status_code=502, detail=EMAIL_FAILED.format(phone=config.BRAND["phone"]))

    MESSAGES.append({"created_at": datetime.now(timezone.utc).isoformat(), **msg.model_dump()})
    return {"message": "Message sent. We'll get back to you soon."}


# Admin views. Set ADMIN_KEY in .env / on Render, then send it in the x-admin-key header.
@app.get("/api/quotes")
def list_quotes(x_admin_key: Optional[str] = Header(default=None)):
    check_admin(x_admin_key)
    return QUOTES


@app.get("/api/messages")
def list_messages(x_admin_key: Optional[str] = Header(default=None)):
    check_admin(x_admin_key)
    return MESSAGES


# ---- Serve the React build. Keep this below all API routes. ----
if (DIST_DIR / "index.html").exists():
    app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_react(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")
        file = (DIST_DIR / full_path).resolve()
        if full_path and file.is_file() and DIST_DIR in file.parents:
            return FileResponse(file)
        # Anything else is a React page, so send index.html and let React Router handle it
        return FileResponse(DIST_DIR / "index.html")
