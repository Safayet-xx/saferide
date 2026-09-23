"""
Sends booking and contact emails.
EMAIL_PROVIDER=sendgrid sends through SendGrid's HTTPS API (works on hosts that block SMTP).
EMAIL_PROVIDER=console prints the email in the server log instead, for local testing.
"""
import html
import json
import logging
import urllib.error
import urllib.request
from typing import Optional

from backend import config

log = logging.getLogger("uvicorn.error")


class EmailError(Exception):
    pass


def check_setup() -> list[str]:
    """Returns a list of problems with the email settings (empty when everything is set)."""
    problems = []
    if config.EMAIL_PROVIDER not in ("sendgrid", "console"):
        problems.append(f"EMAIL_PROVIDER must be 'sendgrid' or 'console', not '{config.EMAIL_PROVIDER}'")
    if config.EMAIL_PROVIDER == "sendgrid":
        if not config.SENDGRID_API_KEY:
            problems.append("SENDGRID_API_KEY is not set")
        if not config.SENDGRID_FROM_EMAIL:
            problems.append("SENDGRID_FROM_EMAIL is not set")
    if not config.BOOKINGS_EMAIL_TO:
        problems.append("BOOKINGS_EMAIL_TO is not set, so nobody receives bookings")
    return problems


def send(to: list[str], subject: str, text_body: str, html_body: str, reply_to: Optional[str] = None):
    if config.EMAIL_PROVIDER == "console":
        log.info(
            "\n----- EMAIL (console mode, not really sent) -----\nTo: %s\nReply-To: %s\nSubject: %s\n\n%s\n-------------------------------------------------",
            ", ".join(to) or "(BOOKINGS_EMAIL_TO not set)", reply_to or "-", subject, text_body,
        )
        return

    if not to:
        raise EmailError("No recipient set (BOOKINGS_EMAIL_TO)")

    problems = check_setup()
    if problems:
        raise EmailError("; ".join(problems))

    payload = {
        "personalizations": [{"to": [{"email": address} for address in to]}],
        "from": {"email": config.SENDGRID_FROM_EMAIL, "name": config.SENDGRID_FROM_NAME},
        "subject": subject,
        "content": [
            {"type": "text/plain", "value": text_body},
            {"type": "text/html", "value": html_body},
        ],
    }
    if reply_to:
        payload["reply_to"] = {"email": reply_to}

    request = urllib.request.Request(
        config.SENDGRID_API_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {config.SENDGRID_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            if response.status >= 300:
                raise EmailError(f"SendGrid returned {response.status}")
    except urllib.error.HTTPError as err:
        detail = err.read().decode(errors="replace")[:500]
        raise EmailError(f"SendGrid error {err.code}: {detail}") from err
    except urllib.error.URLError as err:
        raise EmailError(f"Could not reach SendGrid: {err.reason}") from err


def _render(title: str, rows: list[tuple[str, str]], intro: str = "") -> tuple[str, str]:
    """Builds plain-text and HTML versions of a simple label/value email."""
    rows = [(label, value) for label, value in rows if value not in (None, "")]

    width = max((len(label) for label, _ in rows), default=0)
    text_lines = [title, ""]
    if intro:
        text_lines += [intro, ""]
    text_lines += [f"{label.ljust(width)} : {value}" for label, value in rows]
    text_body = "\n".join(text_lines)

    html_rows = "".join(
        f'<tr><th align="left" style="padding:6px 12px 6px 0;vertical-align:top;color:#555">{html.escape(label)}</th>'
        f'<td style="padding:6px 0;white-space:pre-wrap">{html.escape(str(value))}</td></tr>'
        for label, value in rows
    )
    html_intro = f"<p>{html.escape(intro)}</p>" if intro else ""
    html_body = (
        '<div style="font-family:Arial,sans-serif;font-size:15px;color:#111">'
        f"<h2 style=\"margin:0 0 12px\">{html.escape(title)}</h2>{html_intro}"
        f'<table cellspacing="0" cellpadding="0">{html_rows}</table></div>'
    )
    return text_body, html_body


def _fmt_time(value) -> str:
    return value.strftime("%a %d %b %Y, %H:%M") if value else ""


def quote_rows(reference: str, quote, vehicle_name: str) -> list[tuple[str, str]]:
    rows = [
        ("Reference", reference),
        ("Name", quote.name),
        ("Phone", quote.phone),
        ("Email", quote.email),
        ("Pickup time", _fmt_time(quote.pickup_datetime)),
        ("Pickup address", quote.pickup_address),
        ("Pickup postcode", quote.pickup_postcode),
        ("Destination", quote.destination_address),
        ("Drop-off postcode", quote.dropoff_postcode),
        ("Vehicle", vehicle_name),
        ("Passengers", str(quote.passengers)),
        ("Luggage", quote.luggage),
        ("Journey", "Return" if quote.journey_type == "return" else "One way"),
    ]
    if quote.journey_type == "return":
        rows += [
            ("Return pickup time", _fmt_time(quote.return_pickup_datetime)),
            ("Return pickup address", quote.return_pickup_address),
        ]
    return rows


def send_quote_emails(reference: str, quote, vehicle_name: str):
    """Emails the booking to the business. Raises EmailError if that fails.
    The customer confirmation is best effort: a failure there is only logged."""
    rows = quote_rows(reference, quote, vehicle_name)
    pickup = _fmt_time(quote.pickup_datetime)

    text_body, html_body = _render(
        "New booking request", rows,
        "Reply to this email to contact the customer directly.",
    )
    send(
        config.BOOKINGS_EMAIL_TO,
        f"New booking {reference}: {pickup}, {quote.pickup_postcode or quote.pickup_address} to "
        f"{quote.dropoff_postcode or quote.destination_address}",
        text_body, html_body, reply_to=quote.email,
    )

    if config.SEND_CUSTOMER_CONFIRMATION:
        brand = config.BRAND
        text_body, html_body = _render(
            f"Thanks, {quote.name}. We've got your request.", rows,
            f"We'll contact you shortly with your price. Questions? Call us on {brand['phone']}.",
        )
        try:
            send([quote.email], f"Your {brand['name']} booking request ({reference})", text_body, html_body,
                 reply_to=config.BOOKINGS_EMAIL_TO[0] if config.BOOKINGS_EMAIL_TO else None)
        except EmailError as err:
            log.warning("Customer confirmation for %s not sent: %s", reference, err)


def send_message_email(msg):
    """Emails a contact / business / driver form to the business. Raises EmailError if that fails."""
    text_body, html_body = _render(
        f"New message: {msg.topic}",
        [("Topic", msg.topic), ("Name", msg.name), ("Email", msg.email), ("Phone", msg.phone), ("Message", msg.message)],
        "Reply to this email to contact the sender directly.",
    )
    send(config.BOOKINGS_EMAIL_TO, f"New {msg.topic} message from {msg.name}", text_body, html_body, reply_to=msg.email)
