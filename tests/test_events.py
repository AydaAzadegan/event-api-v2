import io
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from services.event_service import events_db
from models.event import Event
from tasks.notification_worker import check_events_once

client = TestClient(app)

def test_create_event():
    response = client.post("/events", json={
        "title": "Test Event",
        "description": "This is a test",
        "datetime": "2030-01-01T12:00:00"
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["event"]["title"] == "Test Event"

def test_get_all_events():
    response = client.get("/events")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_event_not_found():
    fake_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"/events/{fake_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}

def test_notification_triggered_for_upcoming_event():
    # Create event starting in 2 min
    start_time = (datetime.now(timezone.utc) + timedelta(minutes=2)).isoformat()
    response = client.post("/events", json={
        "title": "Soon Event",
        "description": "Starting soon!",
        "datetime": start_time
    })
    assert response.status_code == 200

    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output
    client.get("/events")
    sys.stdout = sys.__stdout__

    assert "Soon Event" in captured_output.getvalue()

def test_background_notification_logic_direct_call():
    now = datetime.now(timezone.utc)
    event_time = now + timedelta(minutes=3)

    # Add directly to DB
    events_db["test-direct"] = Event(
        title="Direct Worker Test",
        description="Created for background test",
        datetime=event_time
    )

    messages = check_events_once(now)
    assert any("Direct Worker Test" in msg for msg in messages)
