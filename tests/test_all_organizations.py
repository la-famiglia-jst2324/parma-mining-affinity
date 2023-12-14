from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from parma_mining.affinity.api.main import app
from parma_mining.mining_common.const import HTTP_200

client = TestClient(app)


@pytest.fixture
def mock_affinity_client(mocker) -> MagicMock:
    mock = mocker.patch(
        "parma_mining.affinity.api.main.AffinityClient.get_all_companies"
    )
    mock.return_value = [
        {
            "id": 1,
            "name": "testname",
            "domain": "testdomain",
            "domains": ["testdomains1", "testdomains2"],
        }
    ]

    return mock


@pytest.fixture
def mock_analytics_client(mocker) -> MagicMock:
    """Mocking the AnalyticsClient's method to avoid actual API calls during testing."""
    mock = mocker.patch("parma_mining.affinity.api.main.AnalyticsClient.feed_raw_data")
    # No return value needed, but you can add side effects or exceptions if necessary
    return mock


def test_get_all_companies(mock_affinity_client: MagicMock):
    response = client.get("/all-companies")

    assert response.status_code == HTTP_200
    assert response.json() == [
        {
            "id": 1,
            "name": "testname",
            "domain": "testdomain",
            "domains": ["testdomains1", "testdomains2"],
        }
    ]


"""
def test_get_companies(
    mock_affinity_client: MagicMock, mock_analytics_client: MagicMock
):
    response = client.get("/companies")

    mock_analytics_client.assert_called()

    assert response.status_code == 200
"""
