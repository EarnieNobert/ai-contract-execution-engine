from pydantic import BaseModel, Field
from typing import List


class QASchema(BaseModel):
    coverage_score: int = 0
    missing_items: List[str] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)
    revision_suggestions: List[str] = Field(default_factory=list)
    ready_for_review: bool = False