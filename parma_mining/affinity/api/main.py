"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI
from ..client import AffinityClient
from ..secrets import api_key

base_url = "https://api.affinity.co"

app = FastAPI()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-affinity"}


@app.get("/organizations", status_code=200)
def get_all_organizations() -> dict:
    """Fetch all tracked companies from Affiniy CRM."""

    _affinityCrawler = AffinityClient(api_key, base_url)
    return _affinityCrawler.collect_companies()
