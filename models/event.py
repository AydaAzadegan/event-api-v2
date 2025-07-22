from pydantic import BaseModel, field_validator
from datetime import datetime, timezone

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
