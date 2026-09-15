from pydantic import BaseModel


class PlanningDecision(BaseModel):
    can_plan: bool
    missing_information: list[str]
