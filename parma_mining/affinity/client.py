from typing import List
from parma_mining.affinity.model import OrganizationModel
import httpx
from httpx import Response, BasicAuth


class AffinityClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get(self, path: str, params: dict[str, str]) -> Response:
        return httpx.get(
            self.base_url + path,
            auth=BasicAuth("", self.api_key),
            headers={"Content-Type": "application/json"},
            params=params,
        )

    def collect_companies(self) -> List[OrganizationModel]:
        path = "/organizations"
        response = self.get(path, {"": ""}).json()
        organizations = []

        while response["next_page_token"]:
            for result in response["organizations"]:
                parsed_organization = OrganizationModel.model_validate(
                    {
                        "id": result["id"],
                        "name": result["name"],
                        "domain": result["domain"] or "",
                        "domains": result["domains"],
                        "crunchbase_uuid": result["crunchbase_uuid"] or "",
                    }
                )
                organizations.append(parsed_organization)
            response = self.get(
                path, params={"page_token": response["next_page_token"]}
            ).json()

        return organizations
