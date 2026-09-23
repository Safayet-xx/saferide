"""
All website content lives here.
Edit this file to change text, phone numbers, vehicles, locations, reviews and blog posts.
The React frontend loads everything from /api/site, so you never need to touch the JSX for content.
"""
from backend.config import BRAND

SITE = {
    # Brand name, phone, email, address and links come from env vars (see backend/config.py)
    "brand": BRAND,
    "hero": {
        "title": "Book a taxi in under a minute",
        "subtitle": "Tell us where you're going and we'll send you a fixed price before you confirm.",
    },
    "booking_options": [
        {
            "title": "Book by phone",
            "text": "Call our dispatch team and they'll book your ride while you're on the line. No app needed.",
            "action": "Call us",
            "link_type": "phone",
        },
        {
            "title": "Book in the app",
            "text": "Request a ride, see your price and track your driver from your phone.",
            "action": "Get the app",
            "link_type": "app",
        },
    ],
    "features": [
        {"title": "Book without an app", "text": "Our phone line is open around the clock."},
        {"title": "Fixed price upfront", "text": "You see the final fare before the ride is confirmed."},
        {"title": "Live tracking", "text": "We text you a link so you and your family can follow the trip."},
        {"title": "Pre-book any time", "text": "Schedule rides days ahead for early flights or appointments."},
        {"title": "Vetted drivers", "text": "Every driver is licensed, checked and trained by us."},
    ],
    "accounts": [
        {"title": "Personal account", "text": "For you, your family or a regular group. Save addresses and pay faster."},
        {"title": "Business account", "text": "Priority bookings, monthly invoicing and discounted rates for your team."},
    ],
    "app_features": [
        {"title": "Quick search", "text": "Add pickup and drop-off and you're ready to go."},
        {"title": "Fast pickups", "text": "Watch your driver on the map as they arrive."},
        {"title": "Clear pricing", "text": "See the estimated fare before you book."},
    ],
    "vehicles": [
        {"id": "standard", "name": "Standard", "seats": 4, "bags": 2, "text": "Everyday saloon for most trips."},
        {"id": "estate", "name": "Estate", "seats": 4, "bags": 4, "text": "Extra boot space for luggage."},
        {"id": "mpv", "name": "MPV", "seats": 6, "bags": 4, "text": "Room for small groups and families."},
        {"id": "suv", "name": "SUV", "seats": 4, "bags": 3, "text": "A more comfortable, higher ride."},
        {"id": "minibus", "name": "Minibus", "seats": 8, "bags": 8, "text": "Groups, events and airport runs."},
    ],
    "airports": [
        {"name": "Birmingham Airport", "code": "BHX"},
        {"name": "Manchester Airport", "code": "MAN"},
        {"name": "London Heathrow", "code": "LHR"},
        {"name": "London Gatwick", "code": "LGW"},
        {"name": "East Midlands Airport", "code": "EMA"},
    ],
    "locations": [
        {"slug": "london", "name": "London", "text": "Taxis and airport transfers across London, day and night."},
        {"slug": "birmingham", "name": "Birmingham", "text": "Add a short description of your service in Birmingham."},
        {"slug": "wolverhampton", "name": "Wolverhampton", "text": "Add a short description of your service in Wolverhampton."},
        {"slug": "walsall", "name": "Walsall", "text": "Add a short description of your service in Walsall."},
        {"slug": "dudley", "name": "Dudley", "text": "Add a short description of your service in Dudley."},
    ],
    "reviews": [
        {"name": "Customer name", "rating": 5, "text": "Replace this with a real review from a customer."},
        {"name": "Customer name", "rating": 5, "text": "Replace this with a real review from a customer."},
        {"name": "Customer name", "rating": 4, "text": "Replace this with a real review from a customer."},
    ],
    "review_summary": {"rating": 4.8, "count": 0, "source": "Google"},
    "blogs": [
        {
            "slug": "airport-travel-tips",
            "title": "Airport travel tips",
            "date": "2026-01-10",
            "excerpt": "A short summary of the post goes here.",
            "body": "Write the full post here. Separate paragraphs with a blank line.\n\nThis is a second paragraph.",
        },
        {
            "slug": "safe-driving-for-new-drivers",
            "title": "Safe driving for new drivers",
            "date": "2026-02-02",
            "excerpt": "A short summary of the post goes here.",
            "body": "Write the full post here.",
        },
        {
            "slug": "a-day-on-the-road",
            "title": "A day on the road",
            "date": "2026-03-15",
            "excerpt": "A short summary of the post goes here.",
            "body": "Write the full post here.",
        },
    ],
    "legal": {
        "terms": "Add your terms and conditions here.",
        "privacy": "Add your privacy policy here.",
    },
}
