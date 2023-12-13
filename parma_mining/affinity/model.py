from typing import Optional
from pydantic import BaseModel


class OrganizationModel(BaseModel):
    """Base model for organization entity."""

    id: int
    name: Optional[str]
    domain: Optional[str]
    domains: Optional[list[str]]


class AffinityListModel(BaseModel):
    """Base model for Affinity list entity."""

    id: int
    type: Optional[int]
    name: Optional[str]
    public: Optional[bool]
    owner_id: Optional[int]
    creator_id: Optional[int]
    list_size: Optional[int]
