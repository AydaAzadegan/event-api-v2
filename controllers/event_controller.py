from fastapi import APIRouter
from models.event import Event
from services.event_service import create_event, list_events
from fastapi import Path
from services.event_service import get_event_by_id

router = APIRouter()

@router.post("/events")
def create_event_endpoint(event: Event):
    return create_event(event)

@router.get("/events")
def list_events_endpoint():
    return list_events()

@router.get("/events/{event_id}")
def get_event_endpoint(event_id: str = Path(..., description="The ID of the event to retrieve")):
    return get_event_by_id(event_id)
