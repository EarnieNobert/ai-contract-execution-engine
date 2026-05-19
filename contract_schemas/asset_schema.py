from pydantic import BaseModel


class AssetSchema(BaseModel):
    artifact_type: str = ""
    filename: str = ""
    content: str = ""
    contract_type: str = ""