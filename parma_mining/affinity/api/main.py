"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI
from typing import List
from parma_mining.affinity.model import OrganizationModel
from ..client import AffinityClient
from dotenv import load_dotenv
import os

load_dotenv()

base_url = os.getenv("AFFINITY_BASE_URL")
api_key = os.getenv("AFFINITY_API_KEY")

app = FastAPI()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-affinity"}


@app.get("/organizations", status_code=200)
def get_all_organizations() -> List[OrganizationModel]:
    """Fetch all tracked companies from Affiniy CRM."""

    _affinityCrawler = AffinityClient(api_key, base_url)
    return _affinityCrawler.collect_companies()
