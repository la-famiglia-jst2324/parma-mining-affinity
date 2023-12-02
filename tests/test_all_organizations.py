import pytest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from parma_mining.affinity.api.main import app

client = TestClient(app)


@pytest.fixture
def mock_affinity_client(mocker) -> MagicMock:
    mock = mocker.patch(
        "parma_mining.affinity.api.main.AffinityClient.collect_companies"
    )
    mock.return_value = [
        {
            "id": 1,
            "name": "testname",
            "domain": "testdomain",
            "domains": ["testdomains1", "testdomains2"],
            "crunchbase_uuid": "testcrunchbase_uuid",
        }
    ]

    return mock


def test_get_all_organizations(mock_affinity_client: MagicMock):
    response = client.get("/organizations")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "testname",
            "domain": "testdomain",
            "domains": ["testdomains1", "testdomains2"],
            "crunchbase_uuid": "testcrunchbase_uuid",
        }
    ]