import calendar
import csv
from glob import glob
from pathlib import Path
from shutil import rmtree
from typing import Any

import pandas as pd
import requests
from pandas import DataFrame, Series
from pandas.core.generic import NDFrame
from pandas.io.parsers import TextFileReader

from config import (EXPORT_TYPES, FIRST_DATE, PASSWORD, PROGRAMS, SECOND_DATE,
                    URL_SUBDOMAIN, USERNAME)


def start_session_and_get_token(
    username=USERNAME, password=PASSWORD, url_subdomain=URL_SUBDOMAIN
) -> str:
    # Start a session and get a token for future get requests #
    print("[+] Starting session and getting token.")
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
        return token


def create_temp_path() -> str:
    print("[+] Creating a temporary file path.")
    # Create temporary file path
    cwd = get_cwd()
    temp_path = f"{str(cwd)}\\files"
    return temp_path


def remove_temp_path(path) -> None:
    print("[+] Removing temporary file path.")
    # Remove the temp path
    rmtree(path)


def get_cwd() -> Path:
    # Get CWD
    cwd = Path.cwd()
    return cwd


def download_reports(
    date_list, url_subdomain=URL_SUBDOMAIN, export_types=EXPORT_TYPES, programs=PROGRAMS, token=None,
) -> None:

    """
    Downloads and concatenates exported files from the RideCo. dashboard site based on parameters from the config file.
    :return: None
    """

    temp_path = create_temp_path()

    # For each report type and each date, download report
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

                response = requests.get(url=url, headers=headers)

                write_initial_file(response)

                remove_blank_lines_from_csv(file_name)

        append_all_temp_files_to_single_file(export_type)

        remove_temp_path(temp_path)


def write_initial_file(data) -> None:
    # Write the initial file.
    with open("files\\temp.csv", "w", encoding="utf-8") as file:
        file.write(data.text)


def remove_blank_lines_from_csv(file_name) -> None:
    # Remove the blank lines from the CSV.
    in_file = "files\\temp.csv"
    out_file = f"files\\{file_name}"
    with open(in_file) as input_file, open(out_file, "w", newline="") as output:
        writer = csv.writer(output)
        for row in csv.reader(input_file):
            if any(field.strip() for field in row):
                writer.writerow(row)


def append_all_temp_files_to_single_file(export_type) -> None:
    print("[+] Appending temporary files to a single file output.")
    # Append all files in the temp path to a single file
    cwd = get_cwd()
    temp_path = f"{str(cwd)}\\files"
    all_files = glob(f"{temp_path}\\*.csv")
    li: list[TextFileReader | Series | DataFrame | None | NDFrame | Any] = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None)
        li.append(df)
    df = pd.concat(li, axis=0, ignore_index=True)
    # noinspection PyTypeChecker
    df.to_csv(f"{export_type}.csv", index=False)


def create_date_range(
    start_date: str = None, end_date: str = None, month: int = None, year: int = None
) -> list:
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
    t = start_session_and_get_token(username=USERNAME, password=PASSWORD)
    download_reports(
        date_list=dl,
        url_subdomain=URL_SUBDOMAIN,
        export_types=EXPORT_TYPES,
        programs=PROGRAMS,
        token=t,
    )
    print("[+] Done.")
