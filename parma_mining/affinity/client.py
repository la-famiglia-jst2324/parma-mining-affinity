import requests
from requests.auth import HTTPBasicAuth

from parma_mining.affinity.model import OrganizationModel


class AffinityClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def get(self, path):
        return requests.get(
            self.base_url + path,
            auth=HTTPBasicAuth("", self.api_key),
            headers={"Content-Type": "application/json"},
        )

    def collect_companies(self):
        path = "/organizations"
        response = self.get(path)
        organizations = []

        for result in response.json()["organizations"]:
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

        return organizations
