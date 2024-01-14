"""Main entrypoint for the API routes in of parma-analytics."""

import json
import logging
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, status

from parma_mining.affinity.analytics_client import AnalyticsClient
from parma_mining.affinity.api.dependencies.auth import authenticate
from parma_mining.affinity.client import AffinityClient
from parma_mining.affinity.helper import collect_errors
from parma_mining.affinity.model import (
    CrawlingFinishedInputModel,
    ErrorInfoModel,
    OrganizationModel,
    ResponseModel,
)
from parma_mining.affinity.normalization_map import AffinityNormalizationMap
from parma_mining.mining_common.exceptions import AnalyticsError

env = os.getenv("env", "local")

if env == "prod":
    logging.basicConfig(level=logging.INFO)
elif env in ["staging", "local"]:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.warning(f"Unknown environment '{env}'. Defaulting to INFO level.")
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

base_url = str(os.getenv("AFFINITY_BASE_URL") or "")
api_key = str(os.getenv("AFFINITY_API_KEY") or "")

analytics_client = AnalyticsClient()
normalization = AffinityNormalizationMap()

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    logger.debug("Root endpoint called")
    return {"welcome": "at parma-mining-affinity"}


@app.get("/all-companies", status_code=status.HTTP_200_OK)
def get_all_companies(token=Depends(authenticate)) -> list[OrganizationModel]:
    """Fetch all companies from Affiniy CRM."""
    affinity_crawler = AffinityClient(api_key, base_url)
    return affinity_crawler.get_all_companies()


@app.get("/companies", status_code=status.HTTP_200_OK)
def get_companies(token=Depends(authenticate)):
    """Fetch companies in the list from Affinity CRM.

    Currently (12/13/2023) fetch from Dealflow list, in future make list name a query
    parameter
    """
    errors: dict[str, ErrorInfoModel] = {}
    affinity_crawler = AffinityClient(api_key, base_url)

    lists = affinity_crawler.get_all_lists()
    [dealflow] = [
        x for x in lists if x.name == "Dealflow"
    ]  # TODO: Make the list name a query parameter after midterm

    response = affinity_crawler.get_companies_by_list(dealflow.id)
    for org_details in response[:50]:
        data = ResponseModel(
            source_name="affinity", company_id=str(org_details.id), raw_data=org_details
        )
        try:
            analytics_client.feed_raw_data(token, data)
        except AnalyticsError as e:
            logger.error(f"Can't send crawling data to the Analytics. Error: {e}")
            collect_errors(str(org_details.id), errors, e)

    return analytics_client.crawling_finished(
        token,
        json.loads(
            CrawlingFinishedInputModel(task_id=None, errors=errors).model_dump_json()
        ),
    )


@app.get("/initialize", status_code=status.HTTP_200_OK)
def initialize(source_id: int, token=Depends(authenticate)) -> str:
    """Initialize the Affinity CRM source."""
    ## TODO: Register measurements using analytics endpoints
    ##  affinity_crawler = AffinityClient(api_key, base_url)

    # init frequency
    time = "daily"

    normalization_map = AffinityNormalizationMap().get_normalization_map()
    # register the measurements to analytics
    analytics_client.register_measurements(
        token, normalization_map, source_module_id=source_id
    )
    # set and return results
    results = {}
    results["frequency"] = time
    results["normalization_map"] = str(normalization_map)

    return json.dumps(results)
