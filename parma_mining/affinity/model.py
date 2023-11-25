from pydantic import BaseModel
from typing import List


class OrganizationModel(BaseModel):
    """Base model for organization entity."""

    id: int
    name: str
    domain: str
    domains: List[str]
    crunchbase_uuid: str
