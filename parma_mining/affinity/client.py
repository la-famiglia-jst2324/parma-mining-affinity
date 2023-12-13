from typing import Any
from urllib.parse import urljoin

import httpx
from httpx import BasicAuth, Response

from parma_mining.affinity.model import AffinityListModel, OrganizationModel


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

    def get_all_companies(self) -> list[OrganizationModel]:
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

    def get_all_lists(self) -> list[AffinityListModel]:
        path = "/lists"
        response = self.get(path).json()
        lists = []

        for result in response:
            parsed_list = AffinityListModel.model_validate(result)
            lists.append(parsed_list)

        return lists

    def get_companies_by_list(self, list_id: int) -> list[OrganizationModel]:
        path = f"/lists/{list_id}/list-entries"
        response = self.get(path).json()

        organizations = []

        for result in response:
            parsed_organization = OrganizationModel.model_validate(result["entity"])
            organizations.append(parsed_organization)

        return organizations
