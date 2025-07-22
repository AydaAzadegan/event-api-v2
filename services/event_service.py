import uuid
from typing import Dict
from models.event import Event
from fastapi import HTTPException
from datetime import datetime, timezone

# in-memory database
events_db: Dict[str, Event] = {}

def create_event(event: Event) -> dict:
    event_id = str(uuid.uuid4())
    events_db[event_id] = event
    return {"id": event_id, "event": event}


def list_events() -> dict:
    now = datetime.now(timezone.utc)
    for event_id, event in events_db.items():
        seconds_until_start = (event.datetime - now).total_seconds()
        if 0 < seconds_until_start <= 300:
            print(f" Event '{event.title}' starts in {int(seconds_until_start // 60)} minute(s)!")
    return events_db


def get_event_by_id(event_id: str) -> dict:
    event = events_db.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"id": event_id, "event": event}
