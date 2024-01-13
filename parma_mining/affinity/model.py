"""Pydantic models for affinity list entity."""
from pydantic import BaseModel


class OrganizationModel(BaseModel):
    """Base model for organization entity."""

    id: int
    name: str | None
    domain: str | None
    domains: list[str] | None


class AffinityListModel(BaseModel):
    """Base model for Affinity list entity."""

    id: int
    type: int | None
    name: str | None
    public: bool | None
    owner_id: int | None
    creator_id: int | None
    list_size: int | None


class ResponseModel(BaseModel):
    """Base model for response."""

    source_name: str
    company_id: str
    raw_data: OrganizationModel


class ErrorInfoModel(BaseModel):
    """Error info for the crawling_finished endpoint."""

    error_type: str
    error_description: str | None


class CrawlingFinishedInputModel(BaseModel):
    """Internal base model for the crawling_finished endpoints."""

    task_id: int
    errors: dict[str, ErrorInfoModel] | None = None
