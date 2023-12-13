"""Main entrypoint for the API routes in of parma-analytics."""

import os
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, status

from parma_mining.affinity.client import AffinityClient
from parma_mining.affinity.model import OrganizationModel

load_dotenv()

base_url = str(os.getenv("AFFINITY_BASE_URL") or "")
api_key = str(os.getenv("AFFINITY_API_KEY") or "")

app = FastAPI()


# root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-affinity"}


@app.get("/all-companies", status_code=status.HTTP_200_OK)
def get_all_companies() -> list[OrganizationModel]:
    """Fetch all companies from Affiniy CRM."""
    affinity_crawler = AffinityClient(api_key, base_url)
    ## TODO: Send the response to analytics by endpoints
    return affinity_crawler.get_all_companies()


@app.get("/companies", status_code=status.HTTP_200_OK)
def get_companies() -> list[OrganizationModel]:
    """Fetch companies in the list from Affinity CRM.

    Currently (12/13/2023) fetch from Dealflow list, in future make list name a query
    parameter
    """
    affinity_crawler = AffinityClient(api_key, base_url)

    lists = affinity_crawler.get_all_lists()
    [dealflow] = [
        x for x in lists if x.name == "Dealflow"
    ]  # TODO: Make the list name a query parameter after midterm

    return affinity_crawler.get_companies_by_list(dealflow.id)


@app.get("/initialize", status_code=status.HTTP_200_OK)
def initialize() -> dict[str, Any]:
    affinity_crawler = AffinityClient(api_key, base_url)
    ## TODO: Register measurements using analytics endpoints
    return affinity_crawler.normalization_map
