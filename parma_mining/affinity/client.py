from urllib.parse import urljoin

import httpx
from httpx import BasicAuth, Response

from parma_mining.affinity.model import OrganizationModel


class AffinityClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get(self, path: str, params: dict[str, str] | None = None) -> Response:
        full_path = urljoin(self.base_url, path)
        return httpx.get(
            url=full_path,
            auth=BasicAuth("", self.api_key),
            headers={"Content-Type": "application/json"},
            params=params,
        )

    def collect_companies(self) -> list[OrganizationModel]:
        path = "/organizations"
        response = self.get(path).json()
        organizations = []

        while True:
            for result in response["organizations"]:
                parsed_organization = OrganizationModel.model_validate(result)
                organizations.append(parsed_organization)

            if response["next_page_token"] is None:
                break

            response = self.get(
                path, params={"page_token": response["next_page_token"]}
            ).json()

        return organizations
