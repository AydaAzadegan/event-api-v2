import sys
import io
import os
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient

# Add the parent folder to sys.path so we can import main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

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
    start_time = (datetime.now(timezone.utc) + timedelta(minutes=2)).isoformat()
    response = client.post("/events", json={
        "title": "Soon Event",
        "description": "Starting soon!",
        "datetime": start_time
    })
    assert response.status_code == 200

    captured_output = io.StringIO()
    sys.stdout = captured_output

    client.get("/events")

    sys.stdout = sys.__stdout__
    printed_text = captured_output.getvalue()
    assert " Event 'Soon Event' starts in" in printed_text
