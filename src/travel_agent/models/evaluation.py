from pydantic import BaseModel


class Evaluation(BaseModel):
    valid: bool
    violations: list[str]
