import uuid
from typing import Dict
from models.event import Event
from fastapi import HTTPException
from datetime import datetime, timezone

# In-memory "database" to store events
# Keys are UUID strings, values are Event objects
events_db: Dict[str, Event] = {}

# Create a new event and store it in memory
def create_event(event: Event) -> dict:
    event_id = str(uuid.uuid4())  # generate a unique ID for the event
    events_db[event_id] = event   # store event 
    return {"id": event_id, "event": event}  # return the new event ID and data

# List all events, and simulate a notif for events starting in < 5 minutes
def list_events() -> dict:
    now = datetime.now(timezone.utc)
    for event_id, event in events_db.items():
        # Calculate how many seconds until the event starts
        seconds_until_start = (event.datetime - now).total_seconds()
        # If the event starts in less than 5 minutes, print a notif
        if 0 < seconds_until_start <= 300:
            print(f" Event '{event.title}' starts in {int(seconds_until_start // 60)} minute(s)!")
    return events_db  # return all events

# Fetch a specific event by ID, or return 404 if not found
def get_event_by_id(event_id: str) -> dict:
    event = events_db.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"id": event_id, "event": event}
