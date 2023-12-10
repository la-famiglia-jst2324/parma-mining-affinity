from typing import Optional
from pydantic import BaseModel


class OrganizationModel(BaseModel):
    """Base model for organization entity."""

    id: int
    name: Optional[str]
    domain: Optional[str]
    domains: Optional[list[str]]
