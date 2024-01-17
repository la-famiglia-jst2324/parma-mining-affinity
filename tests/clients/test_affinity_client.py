from unittest.mock import patch

import httpx
import pytest

from parma_mining.affinity.client import AffinityClient
from parma_mining.affinity.model import OrganizationModel
from parma_mining.mining_common.exceptions import CrawlingError


@pytest.fixture
def affinity_client():
    return AffinityClient("dummy_api_key", "dummy_base_url")


@patch("parma_mining.affinity.client.AffinityClient.get")
def test_get_companies_by_list_success(mock_get, affinity_client: AffinityClient):
    test_data = [
        {
            "entity": {
                "id": 123,
                "name": "TestOrg",
                "domain": "TestDomain",
                "domains": ["TestDomain1", "TestDomain2"],
            }
        }
    ]
    mock_get.return_value = httpx.Response(json=test_data, status_code=200)

    result = affinity_client.get_companies_by_list(1)

    assert len(result) == 1
    assert isinstance(result[0], OrganizationModel)
    assert result[0].name == "TestOrg"


@patch("parma_mining.affinity.client.AffinityClient.get")
def test_get_companies_by_list_exception(mock_get, affinity_client: AffinityClient):
    exception_instance = CrawlingError("Error fetching organization details!")
    mock_get.side_effect = exception_instance
    with pytest.raises(CrawlingError):
        affinity_client.get_companies_by_list(1)
