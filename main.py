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

from config import EXPORT_TYPES, FIRST_DATE, PROGRAMS, SECOND_DATE, PAYLOAD, URL_SUBDOMAIN


with requests.Session() as session:
    post_response = session.post('https://' + URL_SUBDOMAIN + '.rideco.com/dash-token-auth/', data=PAYLOAD,
              headers={'accept': 'application/json; version=dash-0.43.1', 'path': '/dash-token-auth/'})
    post_json = post_response.json()
    token = post_json['token']

    cwd = Path.cwd()
    temp_path = str(cwd) + '\\files'

    date_list = [d.strftime('%Y-%m-%d') for d in pd.date_range(FIRST_DATE, SECOND_DATE)]
    for export_type in EXPORT_TYPES:
        Path(temp_path).mkdir(parents=True, exist_ok=True)
        for date in date_list:
            for program in PROGRAMS:
                path = (
                    '/dash/rest/exports?'
                    'export_type='
                    + export_type
                    + '&first_date='
                    + date
                    + '&programs='
                    + program
                    + '&second_date='
                    + date
                    + '&timezone=America/Toronto'
                )

                headers = {
                    'authority': URL_SUBDOMAIN + '.rideco.com',
                    'path': path,
                    'accept': 'application/json; version=dash-0.43.1',
                    'authorization': 'Token ' + token,
                }

                url = 'https://sctc.rideco.com' + path

                file_name = date + '-' + date + '-' + export_type + '-' + program + '.csv'

                r = requests.get(
                    url=url,
                    headers=headers,
                )

                # Write the initial file.
                with open('files\\temp.csv', 'w') as file:
                    file.write(r.text)

                # Remove the blank lines from the CSV.
                in_file = 'files\\temp.csv'
                out_file = 'files\\'' + file_name
                with open(in_file) as input, open(out_file, 'w', newline='') as output:
                    writer = csv.writer(output)
                    for row in csv.reader(input):
                        if any(field.strip() for field in row):
                            writer.writerow(row)

        temp_path = str(cwd) + '\\files'
        all_files = glob(temp_path + '\\*.csv')
        li: list[TextFileReader | Series | DataFrame | None | NDFrame | Any] = []
        for filename in all_files:
            df = pd.read_csv(filename, index_col=None)
            li.append(df)
        df = pd.concat(li, axis=0, ignore_index=True)
        df.to_csv(export_type + '.csv', index=False)

        rmtree(temp_path)
