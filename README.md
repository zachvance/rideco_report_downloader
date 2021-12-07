####RideCo Reports Downloader

RideCo reports downloader. Set your variables and bypass RideCo's 31-day at-a-time report limit.
You must retrieve your own program codes from the RideCo site to set up the config. Upon running
the script, it will cycle through the specified dates, programs, and export types, creating
a new temporary file for each before concatenating them all into a single file per export type
and removing the temporary files.

Usage:
1. Edit config.py to suit your report requirements.
2. Run main.py.

Todo:
- Break up the main 'download_reports()' function into more logical pieces.
