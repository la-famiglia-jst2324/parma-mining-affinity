"""This module contains the AnalyticsClient class.

AnalyticsClient class is used to send data to the Analytics API.
"""
import json
import logging
import os
import urllib.parse

import httpx
from dotenv import load_dotenv

from parma_mining.affinity.model import ResponseModel

logger = logging.getLogger(__name__)


class AnalyticsClient:
    """Client for Analytics API."""

    load_dotenv()

    analytics_base = str(os.getenv("ANALYTICS_BASE_URL") or "")

    measurement_url = urllib.parse.urljoin(analytics_base, "/source-measurement")
    feed_raw_url = urllib.parse.urljoin(analytics_base, "/feed-raw-data")

    def send_post_request(self, token: str, api_endpoint, data):
        """Send a POST request to the Analytics API."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        response = httpx.post(api_endpoint, json=data, headers=headers)

        if response.status_code in [200, 201]:
            return response.json()
        else:
            logger.error(
                f"API request failed with status code {response.status_code},"
                f"response: {response.text}"
            )
            raise Exception(
                f"API request failed with status code {response.status_code},"
                f"response: {response.text}"
            )

    def register_measurements(
        self, token: str, mapping, parent_id=None, source_module_id=None
    ):
        """Register measurements in the Analytics API."""
        result = []

        for field_mapping in mapping["Mappings"]:
            measurement_data = {
                "source_module_id": source_module_id,
                "type": field_mapping["DataType"],
                "measurement_name": field_mapping["MeasurementName"],
            }
            if parent_id is not None:
                measurement_data["parent_measurement_id"] = parent_id
            else:
                logger.debug(
                    f"No parent id provided for "
                    f"measurement {measurement_data['measurement_name']}"
                )
            measurement_data["source_measurement_id"] = self.send_post_request(
                token, self.measurement_url, measurement_data
            ).get("id")

            # add the source measurement id to mapping
            field_mapping["source_measurement_id"] = measurement_data[
                "source_measurement_id"
            ]

            if "NestedMappings" in field_mapping:
                nested_measurements = self.register_measurements(
                    token,
                    {"Mappings": field_mapping["NestedMappings"]},
                    parent_id=measurement_data["source_measurement_id"],
                    source_module_id=source_module_id,
                )[0]
                result.extend(nested_measurements)
            result.append(measurement_data)
        return result, mapping

    def feed_raw_data(self, token: str, input_data: ResponseModel):
        """Feed raw data to the Analytics API."""
        organization_json = json.loads(input_data.raw_data.model_dump_json())

        data = {
            "source_name": input_data.source_name,
            "company_id": input_data.company_id,
            "raw_data": organization_json,
        }

        return self.send_post_request(token, self.feed_raw_url, data)
