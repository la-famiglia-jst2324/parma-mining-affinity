from typing import List, Optional
from parma_mining.affinity.model import OrganizationModel
import httpx
from httpx import Response, BasicAuth
from urllib.parse import urljoin


class AffinityClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get(self, path: str, params: Optional[dict[str, str]] = None) -> Response:
        full_path = urljoin(self.base_url, path)
        return httpx.get(
            url=full_path,
            auth=BasicAuth("", self.api_key),
            headers={"Content-Type": "application/json"},
            params=params,
        )

    def collect_companies(self) -> List[OrganizationModel]:
        path = "/organizations"
        response = self.get(path).json()
        organizations = []

        while True:
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

            if response["next_page_token"] == None:
                break

        return organizations
