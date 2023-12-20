"""Normalization map for affinity data."""


class AffinityNormalizationMap:
    """Normalization map for affinity data."""

    map_json = {
        "Source": "Affinity",
        "Mappings": [
            {
                "SourceField": "id",
                "DataType": "int",
                "MeasurementName": "affinity company id",
            },
            {
                "SourceField": "name",
                "DataType": "text",
                "MeasurementName": "company name",
            },
            {
                "SourceField": "domain",
                "DataType": "text",
                "MeasurementName": "company domain",
            },
            {
                "SourceField": "domains",
                "DataType": "text",
                "MeasurementName": "company all domains",
            },
        ],
    }

    def get_normalization_map(self):
        """Return the normalization map."""
        return self.map_json
