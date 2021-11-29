"""
RideCo reports downloader. Set your variables and bypass RideCo's 31-day at-a-time report limit. You must retrieve your
own program codes from the RideCo site to set up this script.

.. todo::
    -   Add authentication
    -   Stitch downloaded reports together into a single file (per export_type)
"""

import pandas as pd
import requests
import csv

first_date = '2021-10-01'
second_date = '2021-11-05'
export_types = ['ride', 'fare', 'vehicle_hours']
tho = 'a0b63f37-a251-4e15-a769-36432ad8c00d'  # Thorold program code
stc = '268298b4-73bb-415c-8fb5-6a5524ccceb6'  # St. Catharines program code
programs = [stc, tho]
programs_dictionary = {'St. Catharines': '268298b4-73bb-415c-8fb5-6a5524ccceb6',
                       'Thorold': 'a0b63f37-a251-4e15-a769-36432ad8c00d',
                       }
date_list = [d.strftime('%Y-%m-%d') for d in pd.date_range(first_date, second_date)]

for date in date_list:
    for export_type in export_types:
        for program in programs:
            path = '/dash/rest/exports?' \
                   'export_type=' + export_type + \
                   '&first_date=' + date + \
                   '&programs=' + program + \
                   '&second_date=' + date + \
                   '&timezone=America/Toronto'

            headers = {'authority': 'sctc.rideco.com',
                       'path': path,
                       'accept': 'application/json; version=dash-0.43.1',
                       'authorization': 'Token 0e78db1173d17ebad26a5472b9393031d11abf0b',
                       }

            url = 'https://sctc.rideco.com' + path

            file_name = date + '-' + \
                        date + '-' + \
                        export_type + '-' + \
                        program + \
                        '.csv'

            r = requests.get(
              url=url,
              headers=headers,
            )

            with open('temp.csv', 'w') as file:
              file.write(r.text)

            in_fnam = 'temp.csv'
            out_fnam = file_name

            with open(in_fnam) as input, open(out_fnam, 'w', newline='') as output:
                writer = csv.writer(output)
                for row in csv.reader(input):
                    if any(field.strip() for field in row):
                        writer.writerow(row)