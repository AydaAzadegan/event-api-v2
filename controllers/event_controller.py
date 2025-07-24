from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from models.event import Event
from services.event_service import create_event, list_events, get_event_by_id
from services.database import get_db

router = APIRouter()

@router.post("/events")
async def create_event_endpoint(event: Event, db: AsyncSession = Depends(get_db)):
    return await create_event(event, db)

@router.get("/events")
async def list_events_endpoint(db: AsyncSession = Depends(get_db)):
    return await list_events(db)

@router.get("/events/{event_id}")
async def get_event_endpoint(event_id: str = Path(...), db: AsyncSession = Depends(get_db)):
    return await get_event_by_id(event_id, db)
