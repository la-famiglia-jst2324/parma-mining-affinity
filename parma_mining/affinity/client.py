import requests
from requests.auth import HTTPBasicAuth


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
        return response.json()
