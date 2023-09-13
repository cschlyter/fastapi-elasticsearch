from datetime import datetime
from pydantic import BaseModel


class EntryPayloadSchema(BaseModel):
    text: str
    timestamp: datetime = None


class EntryResponseSchema(EntryPayloadSchema):
    id: str
