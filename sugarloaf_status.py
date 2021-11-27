#!/usr/bin/env python
# coding: utf-8
from bs4 import BeautifulSoup
import requests
import pandas as pd

MOBILE_SUGARLOAF_CONDITIONS_URL = (
    "http://spotlio-snowconditions.s3.amazonaws.com/sugarloaf/status.json"
)

MOUNTAIN_REPORT_HTML = "https://www.sugarloaf.com/mountain-report"

response = requests.get(MOBILE_SUGARLOAF_CONDITIONS_URL)
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

response = requests.get(MOUNTAIN_REPORT_HTML)
soup = BeautifulSoup(response.text)

longest_div = None

for div in soup.findAll("div", class_="content"):
    div_text = div.getText()

    if (
        "Last Updated" not in div_text
        and "Trail Status" not in div_text
        and "Snow Making" not in div_text
        and "Swedish Fiddle Glade" not in div_text
    ):

        try:
            if len(longest_div.getText()) < len(div_text):
                longest_div = div
        except AttributeError:
            longest_div = div

with open("report.html", "w") as f:
    f.write(str(longest_div))
