"""Main entrypoint for the API routes in of parma-analytics."""

import os

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


@app.get("/organizations", status_code=status.HTTP_200_OK)
def get_all_organizations() -> list[OrganizationModel]:
    """Fetch all tracked companies from Affiniy CRM."""
    affinity_crawler = AffinityClient(api_key, base_url)
    return affinity_crawler.collect_companies()
