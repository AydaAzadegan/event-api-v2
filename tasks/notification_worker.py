import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from services.database import async_session
from models.event import EventModel, NotificationLog
from services.email_notifier import send_notification_email
import asyncio

async def check_upcoming_events():
    while True:
        await check_upcoming_events_once()
        await asyncio.sleep(60)

async def check_upcoming_events_once():  
    async with async_session() as session:
        now = datetime.now(timezone.utc)
        in_5_min = now + timedelta(minutes=5)
        print(f"[DEBUG] Now: {now}, In 5 minutes: {in_5_min}")

        result = await session.execute(
            select(EventModel).where(EventModel.datetime.between(now, in_5_min))
        )
        upcoming_events = result.scalars().all()
        print(f"[DEBUG] Found {len(upcoming_events)} upcoming event(s)")

        for event in upcoming_events:
            print(f"[DEBUG] Checking event: {event.title} at {event.datetime}")

            # Check if we've already sent notification
            log_check = await session.execute(
                select(NotificationLog).where(NotificationLog.event_id == event.id)
            )
            if log_check.scalar():
                print(f"[DEBUG] Skipping {event.title} — already notified")
                continue  # already sent

            msg = f"[Notify] Event '{event.title}' starts at {event.datetime}!"
            print(f"[DEBUG] New notification needed: {msg}")

            await send_notification(msg)

            session.add(NotificationLog(event_id=event.id, message=msg))
        await session.commit()

async def send_notification(message: str):
    print(f"[DEBUG] Sending email: {message}")
    send_notification_email("Upcoming Event", message)

# For legacy fallback/local dev
if __name__ == "__main__":
    print("Starting notification worker...")
    asyncio.run(check_upcoming_events())
