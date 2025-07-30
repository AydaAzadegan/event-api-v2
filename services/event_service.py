from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.event import Event, EventModel
from fastapi import HTTPException
from sqlalchemy import select
from datetime import datetime, timezone, timedelta
from .database import async_session
import os
from services.email_notifier import send_notification_email

# CREATE
async def create_event(event: Event, db: AsyncSession):
    db_event = EventModel(
        title=event.title,
        description=event.description,
        datetime=event.datetime
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)

    # Send notification email (if enabled)
    if os.getenv("EMAIL_NOTIFICATIONS", "true").lower() == "true":
        subject = f"New Event Created: {db_event.title}"
        body = (
            f"A new event has been created:\n\n"
            f"Title: {db_event.title}\n"
            f"Description: {db_event.description}\n"
            f"Date & Time: {db_event.datetime}"
        )
        send_notification_email(subject, body)

    return db_event


# LIST
async def list_events(db: AsyncSession):
    result = await db.execute(select(EventModel))
    return result.scalars().all()

# GET BY ID
async def get_event_by_id(event_id: str, db: AsyncSession):
    event = await db.get(EventModel, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


