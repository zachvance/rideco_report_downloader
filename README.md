# RideCo Reports Downloader

## What this script does

RideCo reports downloader. Set your variables and bypass RideCo's 31-day at-a-time report limit.
You must retrieve your own program codes from the RideCo site to set up the config. Upon running
the script, it will cycle through the specified dates, programs, and export types, creating
a new temporary file for each before concatenating them all into a single file per export type
and removing the temporary files.

## Usage

1. Edit config.py to suit your report requirements.
2. Run main.py.

## Reasoning

The purpose of this script is two-fold: to ease the workload of downloading the required reports each month, and to figure out a work-around for RideCo's report limit.

Part of what made downloading monthly reports from the RideCo dashboard so time consuming was that they only allowed for up to 31 reports to be downloaded at once. This is not so much a problem if you were downloading one report type for one property - 1 export type x 1 program x 31 days (max) allows for a monthly download just fine. But if you require multiple export types and/or multiple programs, you could spend considerable amounts of time adjusting the settings, waiting for the reports to generate, and download. In my case, up to 4 export types and 2 programs per month.

This script sends a new request query for each program, export type, and day within the specified date range - so only downloading 1 report at a time, regardless of the number of programs, export types, or dates - before concatenating all pieces into a single output file (per export type).

## Todo

- Break up the main 'download_reports()' function into more logical pieces.
- Maybe add a prompt for the date input insetad of changing the config file for the date range.
