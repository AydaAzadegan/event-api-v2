from fastapi import APIRouter, Path
from models.event import Event
from services.event_service import create_event, list_events, get_event_by_id

# Create a router to organize event-related API endpoints
router = APIRouter()

# POST /events → Create a new event
# Receives an Event object in the request body and stores it
@router.post("/events")
def create_event_endpoint(event: Event):
    return create_event(event)

# GET /events → List all stored events
# Also triggers print-based notifications if any event starts in < 5 minutes
@router.get("/events")
def list_events_endpoint():
    return list_events()

# GET /events/{event_id} → Get details of a specific event by ID
# If the event is not found, raises a 404 error
@router.get("/events/{event_id}")
def get_event_endpoint(event_id: str = Path(..., description="The ID of the event to retrieve")):
    return get_event_by_id(event_id)

