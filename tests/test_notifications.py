import sys
import os
import asyncio
from unittest.mock import patch
from datetime import datetime, timedelta, timezone

from httpx import AsyncClient, ASGITransport
from sqlalchemy.future import select

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from models.event import EventModel, NotificationLog
from services.database import async_session
from tasks.notification_worker import check_upcoming_events_once


def test_event_notification_flow():
    asyncio.run(_test_event_notification_flow())


async def _test_event_notification_flow():
    event_time = datetime.now(timezone.utc) + timedelta(minutes=3)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/events", json={
            "title": "Notify Test Event",
            "description": "Testing notification logic",
            "datetime": event_time.isoformat()
        })
    assert response.status_code == 200
    data = response.json()
    event_id = data["id"]

    async with async_session() as session:
        result = await session.execute(select(EventModel).where(EventModel.id == event_id))
        event = result.scalar()
        assert event is not None

    with patch("tasks.notification_worker.send_notification_email") as mock_send_email:
        await check_upcoming_events_once()
        mock_send_email.assert_called_once()

    async with async_session() as session:
        result = await session.execute(select(NotificationLog).where(NotificationLog.event_id == event_id))
        log_entry = result.scalar()
        assert log_entry is not None

    with patch("tasks.notification_worker.send_notification_email") as mock_send_email:
        await check_upcoming_events_once()
        mock_send_email.assert_not_called()

