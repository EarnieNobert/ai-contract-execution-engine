from pydantic import BaseModel, Field
from typing import List


class PlanSchema(BaseModel):
    milestones: List[str] = Field(default_factory=list)
    tasks: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    recommended_stack: List[str] = Field(default_factory=list)
    validation_checks: List[str] = Field(default_factory=list)
    risk_register: List[str] = Field(default_factory=list)