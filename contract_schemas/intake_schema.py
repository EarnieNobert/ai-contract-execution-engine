from pydantic import BaseModel, Field
from typing import List


class IntakeSchema(BaseModel):
    contract_name: str = ""
    client_name: str = ""
    project_type: str = ""
    goal: str = ""
    deliverables: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    deadline: str = ""
    notes: str = ""
    assumptions: List[str] = Field(default_factory=list)
    missing_info: List[str] = Field(default_factory=list)
    source_docs_needed: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)