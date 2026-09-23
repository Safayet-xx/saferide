import secrets
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend import config
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

# Simple in-memory storage. It resets whenever the server restarts.
# Swap this for a real database (e.g. Postgres on Render) when you need to keep data.
QUOTES = []
MESSAGES = []

VEHICLE_IDS = {v["id"] for v in SITE["vehicles"]}


class QuoteRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=200)
    phone: str = Field(min_length=5, max_length=30)
    pickup_address: str = Field(min_length=1, max_length=300)
    pickup_postcode: str = Field(default="", max_length=12)
    pickup_datetime: str = Field(min_length=1)
    destination_address: str = Field(min_length=1, max_length=300)
    dropoff_postcode: str = Field(default="", max_length=12)
    vehicle: str
    passengers: int = Field(ge=1, le=16)
    luggage: str = Field(default="", max_length=200)
    journey_type: str = "one_way"
    return_pickup_address: Optional[str] = None
    return_pickup_datetime: Optional[str] = None


class ContactMessage(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=200)
    phone: str = Field(default="", max_length=30)
    topic: str = Field(default="General", max_length=50)
    message: str = Field(min_length=1, max_length=3000)


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
    if "@" not in quote.email:
        raise HTTPException(status_code=422, detail="Enter a valid email address")
    if quote.vehicle not in VEHICLE_IDS:
        raise HTTPException(status_code=422, detail="Choose a vehicle from the list")
    if quote.journey_type == "return" and not quote.return_pickup_datetime:
        raise HTTPException(status_code=422, detail="Add a date and time for the return journey")

    reference = uuid.uuid4().hex[:8].upper()
    QUOTES.append({
        "reference": reference,
        "created_at": datetime.now(timezone.utc).isoformat(),
        **quote.model_dump(),
    })
    return {"reference": reference, "message": "Quote request received. We'll email your price shortly."}


@app.post("/api/messages", status_code=201)
def create_message(msg: ContactMessage):
    if "@" not in msg.email:
        raise HTTPException(status_code=422, detail="Enter a valid email address")
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
