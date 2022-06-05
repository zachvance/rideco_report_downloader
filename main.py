import calendar
import csv
from glob import glob
from pathlib import Path
from shutil import rmtree
from typing import Any, List

import pandas as pd
import requests
from pandas import DataFrame, Series
from pandas.core.generic import NDFrame
from pandas.io.parsers import TextFileReader

from config import (EXPORT_TYPES, FIRST_DATE, PASSWORD, PROGRAMS, SECOND_DATE,
                    URL_SUBDOMAIN, USERNAME)


def download_reports(
    date_list,
    url_subdomain=URL_SUBDOMAIN,
    export_types=EXPORT_TYPES,
    programs=PROGRAMS,
    username=USERNAME,
    password=PASSWORD,
) -> None:

    """
    Downloads and concatenates exported files from the RideCo. dashboard site based on parameters from the config file.
    :return: None
    """

    payload = {"username": username, "password": password}

    with requests.Session() as session:
        post_response = session.post(
            f"https://{url_subdomain}.rideco.com/dash-token-auth/",
            data=payload,
            headers={
                "accept": "application/json; version=dash-0.43.1",
                "path": "/dash-token-auth/",
            },
        )
        post_json = post_response.json()
        token = post_json["token"]

        cwd = Path.cwd()
        temp_path = f"{str(cwd)}\\files"

        for export_type in export_types:
            print(f"[+] Now downloading {export_type} reports.")
            Path(temp_path).mkdir(parents=True, exist_ok=True)
            for date in date_list:
                print(f"[+] Date: {date}")
                for program in programs:
                    path = (
                        f"/dash/rest/exports?"
                        f"export_type={export_type}"
                        f"&first_date={date}"
                        f"&programs={program}"
                        f"&second_date={date}"
                        f"&timezone=America/Toronto"
                    )

                    headers = {
                        "authority": f"{url_subdomain}.rideco.com",
                        "path": path,
                        "accept": "application/json; version=dash-0.43.1",
                        "authorization": f"Token {token}",
                    }

                    url = f"https://{url_subdomain}.rideco.com{path}"

                    file_name = f"{date}-{date}-{export_type}-{program}.csv"

                    r = requests.get(
                        url=url,
                        headers=headers,
                    )

                    # Write the initial file.
                    with open("files\\temp.csv", "w", encoding="utf-8") as file:
                        file.write(r.text)

                    # Remove the blank lines from the CSV.
                    in_file = "files\\temp.csv"
                    out_file = f"files\\{file_name}"
                    with open(in_file) as input_file, open(
                        out_file, "w", newline=""
                    ) as output:
                        writer = csv.writer(output)
                        for row in csv.reader(input_file):
                            if any(field.strip() for field in row):
                                writer.writerow(row)

            temp_path = f"{str(cwd)}\\files"
            all_files = glob(f"{temp_path}\\*.csv")
            li: list[TextFileReader | Series | DataFrame | None | NDFrame | Any] = []
            for filename in all_files:
                df = pd.read_csv(filename, index_col=None)
                li.append(df)
            df = pd.concat(li, axis=0, ignore_index=True)
            # noinspection PyTypeChecker
            df.to_csv(f"{export_type}.csv", index=False)

            rmtree(temp_path)


def create_date_range(
    start_date: str = None, end_date: str = None, month: int = None, year: int = None
) -> [List | str]:
    """
    Creates a list of dates as strings, in the format of 'YYYY-MM-DD'. Requires either the parameters 'start_date' and
    'end_date', or 'month' and 'year' to work.

    :param start_date: The starting date of the desired date range. Formatted as 'YYYY-MM-DD'.
    :type start_date: str
    :param end_date: The ending date of the desired date range. Formatted as 'YYYY-MM-DD'.
    :type end_date: str
    :param month: The month of the desired date range.
    :type month: int
    :param year: The year of the desired date range.
    :type year: int
    :return: A list of generated dates or a message as a string.
    :rtype: List or str
    """
    if month and year:
        start_date = f"{year}-{month:01}-01"
        end_date = f"{year}-{month:01}-{calendar.monthrange(year, month)[1]}"

    if not start_date and end_date:
        raise ValueError(
            "No valid argument combinations provided. "
            "Must provide either a start date and end date, "
            "or a month and year."
        )
    return [d.strftime("%Y-%m-%d") for d in pd.date_range(start_date, end_date)]


if __name__ == "__main__":
    dl = create_date_range(start_date=FIRST_DATE, end_date=SECOND_DATE)
    download_reports(
        date_list=dl,
        url_subdomain=URL_SUBDOMAIN,
        export_types=EXPORT_TYPES,
        programs=PROGRAMS,
        username=USERNAME,
        password=PASSWORD,
    )
