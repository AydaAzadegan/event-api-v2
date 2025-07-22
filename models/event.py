from pydantic import BaseModel, field_validator
from datetime import datetime, timezone

# Event data model using Pydantic
# This defines the shape of the data we accept 
class Event(BaseModel):
    title: str           # Name of the event
    description: str     # Details about the event
    datetime: datetime   # When the event will happen

    # Validator to ensure datetime has a timezone
    # If no timezone is provided, assume UTC
    @field_validator("datetime")
    @classmethod
    def make_timezone_aware(cls, value):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
