from typing import Literal

from pydantic import BaseModel


class Task(BaseModel):
    description: str
    status: Literal["pending", "in_progress", "completed", "failed"] = "pending"
    result: str | None = None
