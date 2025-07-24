from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from services.database import Base
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey


# Pydantic model (for request validation)
class Event(BaseModel):
    title: str
    description: str
    datetime: datetime

    @field_validator("datetime")
    @classmethod
    def make_timezone_aware(cls, value):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

# SQLAlchemy model (for DB table)
class EventModel(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String)
    datetime = Column(DateTime(timezone=True), nullable=False)


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    message = Column(String, nullable=False)
    sent_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
