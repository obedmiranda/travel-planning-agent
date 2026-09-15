from pydantic import BaseModel


class ParsedRequest(BaseModel):
    destination: str
    travelers: int | None = None
    trip_duration: int | None = None
    budget: float | None = None
