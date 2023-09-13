from datetime import datetime

from pydantic import BaseModel, constr


class EntryPayloadSchema(BaseModel):
    text: constr(min_length=1, strip_whitespace=True)
    timestamp: datetime = None


class EntryResponseSchema(EntryPayloadSchema):
    id: str
