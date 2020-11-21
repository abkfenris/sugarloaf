#!/usr/bin/env python
# coding: utf-8
import requests
import pandas as pd

MOBILE_SUNDAY_RIVER_CONDITIONS_URL = (
    "http://spotlio-snowconditions.s3.amazonaws.com/sugarloaf/status.json"
)

response = requests.get(MOBILE_SUNDAY_RIVER_CONDITIONS_URL)
json = response.json()


def flatten_item(item):
    """ Returns a flattened version of the item """
    output = {}
    for key in item.keys():
        if key not in ["status", "properties"]:
            output[key] = item[key]

    for status in item["status"]:
        output[status["status_name"]] = status["status_value"]

    for key, obj in item["properties"].items():
        if key == "features":
            for feature_key, feature_obj in obj.items():
                output[feature_key] = feature_obj

        else:
            output[key] = obj

    return output


trails_df = pd.DataFrame(
    [flatten_item(item) for item in json if "type" in item and item["type"] == "trail"]
)
lifts_df = pd.DataFrame(
    [flatten_item(item) for item in json if "type" in item and item["type"] == "lift"]
)

trails_df = trails_df.sort_values("name")
trails_df.to_csv("trails.csv", index=False)

lifts_df = lifts_df.sort_values("name")
lifts_df.to_csv("lifts.csv", index=False)
