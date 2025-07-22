from datetime import datetime, timezone
from services.event_service import events_db
import asyncio

def check_events_once(now):
    messages = []
    for event_id, event in events_db.items():
        seconds_until_start = (event.datetime - now).total_seconds()
        if 0 < seconds_until_start <= 300:
            msg = f"[Background] Event '{event.title}' starts in {int(seconds_until_start // 60)} minute(s)!"
            print(msg)
            messages.append(msg)
    return messages

# Background loop
async def check_upcoming_events():
    while True:
        now = datetime.now(timezone.utc)
        check_events_once(now)
        await asyncio.sleep(60)