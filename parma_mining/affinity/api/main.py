"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI, status
from typing import List
from parma_mining.affinity.model import OrganizationModel
from parma_mining.affinity.client import AffinityClient
from dotenv import load_dotenv
import os

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
def get_all_organizations() -> List[OrganizationModel]:
    """Fetch all tracked companies from Affiniy CRM."""

    _affinityCrawler = AffinityClient(api_key, base_url)
    return _affinityCrawler.collect_companies()
