# RideCo Reports Downloader

 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
 [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

RideCo reports downloader. Set your variables and bypass RideCo's 31-day at-a-time report limit.
You must retrieve your own program codes from the RideCo site to set up the config. Upon running
the script, it will cycle through the specified dates, programs, and export types, creating
a new temporary file for each before concatenating them all into a single file per export type
and removing the temporary files.

## Usage:

### As a script using the config file for variables:

1. Edit config.py to suit your report requirements.
2. Run main.py.

### Supplying variables via command line arguments:

`python menu.py [-help] [--start_date] [--end_date] [--month] [--year] [--username] [--password] [--export_types] [--programs] [--url_subdomain]`

Only 1 pair of either `--start_date` and `--end_date` OR `--month` and `--year` are required.

Note that though all arguments are optional, those omitted are filled with defaults from the config file, which may
cause an error if not set up.

Todo:
- More error handling.
- Revise docstrings and typehints.
- Tests
