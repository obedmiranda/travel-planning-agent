from pydantic import BaseModel


class ParsedRequest(BaseModel):
    destination: str
