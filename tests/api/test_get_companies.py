import logging
from unittest.mock import MagicMock

import httpx
import pytest
from fastapi.testclient import TestClient

from parma_mining.affinity.api.dependencies.auth import authenticate
from parma_mining.affinity.api.main import app
from parma_mining.affinity.model import AffinityListModel
from parma_mining.mining_common.const import HTTP_200
from tests.dependencies.mock_auth import mock_authenticate


@pytest.fixture
def client():
    assert app
    app.dependency_overrides.update(
        {
            authenticate: mock_authenticate,
        }
    )
    return TestClient(app)


logger = logging.getLogger(__name__)


@pytest.fixture
def mock_affinity_client(mocker) -> MagicMock:
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
    mock_get = mocker.patch("parma_mining.affinity.api.main.AffinityClient.get")
    mock_get.return_value = httpx.Response(json=test_data, status_code=200)
    mock_get_all_lists = mocker.patch(
        "parma_mining.affinity.api.main.AffinityClient.get_all_lists"
    )
    mock_get_all_lists.return_value = [
        AffinityListModel.model_validate(
            {
                "id": 123,
                "type": 123,
                "name": "Dealflow",  # hardcoded for now
                "public": True,
                "owner_id": 123,
                "creator_id": 123,
                "list_size": 123,
            }
        )
    ]
    # No return value needed, but you can add side effects or exceptions if necessary
    return mock_get_all_lists


@pytest.fixture
def mock_analytics_client(mocker) -> MagicMock:
    """Mocking the AnalyticClient's method to avoid actual API calls during testing."""
    mock = mocker.patch("parma_mining.affinity.api.main.AnalyticsClient.feed_raw_data")
    mock = mocker.patch(
        "parma_mining.affinity.api.main.AnalyticsClient.crawling_finished"
    )
    mock.return_value = {}
    # No return value needed, but you can add side effects or exceptions if necessary
    return mock


def test_get_companies_success(
    client: TestClient,
    mock_affinity_client: MagicMock,
    mock_analytics_client: MagicMock,
):
    payload = {
        "task_id": 123,
    }

    headers = {"Authorization": "Bearer test"}
    response = client.post("/companies", json=payload, headers=headers)

    assert response.status_code == HTTP_200
