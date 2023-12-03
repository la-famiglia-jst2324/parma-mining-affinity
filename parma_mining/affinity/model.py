from pydantic import BaseModel


class OrganizationModel(BaseModel):
    """Base model for organization entity."""

    id: int
    name: str
    domain: str
    domains: list[str]
    crunchbase_uuid: str
