"""
RideCo reports downloader. Set your variables and bypass RideCo's 31-day at-a-time report limit. You must retrieve your
own program codes from the RideCo site to set up this script.

.. todo::
    -   Add authentication
    -   Stitch downloaded reports together into a single file (per export_type)
"""

import csv
from pathlib import Path

import pandas as pd
import requests

from config import EXPORT_TYPES, FIRST_DATE, PROGRAMS, SECOND_DATE

cwd = Path.cwd()
path = str(cwd) + "\\files"
Path(path).mkdir(parents=True, exist_ok=True)

date_list = [d.strftime("%Y-%m-%d") for d in pd.date_range(FIRST_DATE, SECOND_DATE)]

for date in date_list:
    for export_type in EXPORT_TYPES:
        for program in PROGRAMS:
            path = (
                "/dash/rest/exports?"
                "export_type="
                + export_type
                + "&first_date="
                + date
                + "&programs="
                + program
                + "&second_date="
                + date
                + "&timezone=America/Toronto"
            )

            headers = {
                "authority": "sctc.rideco.com",
                "path": path,
                "accept": "application/json; version=dash-0.43.1",
                "authorization": "Token 0e78db1173d17ebad26a5472b9393031d11abf0b",
            }

            url = "https://sctc.rideco.com" + path

            file_name = date + "-" + date + "-" + export_type + "-" + program + ".csv"

            r = requests.get(
                url=url,
                headers=headers,
            )

            # Write the initial file.
            with open("files\\temp.csv", "w") as file:
                file.write(r.text)

            # Remove the blank lines from the CSV.
            in_file = "files\\temp.csv"
            out_file = "files\\" + file_name
            with open(in_file) as input, open(out_file, "w", newline="") as output:
                writer = csv.writer(output)
                for row in csv.reader(input):
                    if any(field.strip() for field in row):
                        writer.writerow(row)
