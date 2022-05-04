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


def download_reports() -> None:

    """
    Downloads and concatenates exported files from the RideCo. dashboard site based on parameters from the config file.
    :return: None
    """

    with requests.Session() as session:
        post_response = session.post(f'https://{URL_SUBDOMAIN}.rideco.com/dash-token-auth/',
                                     data=PAYLOAD,
                                     headers={'accept': 'application/json; version=dash-0.43.1',
                                              'path': '/dash-token-auth/',
                                              }
                                     )
        post_json = post_response.json()
        token = post_json['token']

        cwd = Path.cwd()
        temp_path = f'{str(cwd)}\\files'

        date_list = [d.strftime('%Y-%m-%d') for d in pd.date_range(FIRST_DATE, SECOND_DATE)]
        for export_type in EXPORT_TYPES:
            print(f'[+] Now downloading {export_type} reports.')
            Path(temp_path).mkdir(parents=True, exist_ok=True)
            for date in date_list:
                print(f'[+] Date: {date}')
                for program in PROGRAMS:
                    path = (
                        f'/dash/rest/exports?'
                        f'export_type={export_type}'
                        f'&first_date={date}'
                        f'&programs={program}'
                        f'&second_date={date}'
                        f'&timezone=America/Toronto'
                    )

                    headers = {
                        'authority': f'{URL_SUBDOMAIN}.rideco.com',
                        'path': path,
                        'accept': 'application/json; version=dash-0.43.1',
                        'authorization': f'Token {token}',
                    }

                    url = f'https://{URL_SUBDOMAIN}.rideco.com{path}'

                    file_name = f'{date}-{date}-{export_type}-{program}.csv'

                    r = requests.get(
                        url=url,
                        headers=headers,
                    )

                    # Write the initial file.
                    with open('files\\temp.csv', 'w', encoding='utf-8') as file:
                        file.write(r.text)

                    # Remove the blank lines from the CSV.
                    in_file = 'files\\temp.csv'
                    out_file = f'files\\{file_name}'
                    with open(in_file) as input_file, open(out_file, 'w', newline='') as output:
                        writer = csv.writer(output)
                        for row in csv.reader(input_file):
                            if any(field.strip() for field in row):
                                writer.writerow(row)

            temp_path = f'{str(cwd)}\\files'
            all_files = glob(f'{temp_path}\\*.csv')
            li: list[TextFileReader | Series | DataFrame | None | NDFrame | Any] = []
            for filename in all_files:
                df = pd.read_csv(filename, index_col=None)
                li.append(df)
            df = pd.concat(li, axis=0, ignore_index=True)
            # noinspection PyTypeChecker
            df.to_csv(f'{export_type}.csv', index=False)

            rmtree(temp_path)


if __name__ == '__main__':
    download_reports()
