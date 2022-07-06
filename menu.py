import argparse

from config import EXPORT_TYPES, PASSWORD, PROGRAMS, URL_SUBDOMAIN, USERNAME
from main import create_date_range, download_reports, start_session_and_get_token

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download reports from RideCo's dashboard."
    )

    parser.add_argument(
        "-sd",
        "--start_date",
        default=None,
        type=str,
        help="Starting date for the reports.",
    )
    parser.add_argument(
        "-ed", "--end_date", default=None, type=str, help="Ending date for the reports."
    )
    parser.add_argument(
        "-m", "--month", default=None, type=int, help="The month for the report."
    )
    parser.add_argument(
        "-y", "--year", default=None, type=int, help="The year for the report."
    )
    parser.add_argument(
        "-u",
        "--username",
        type=str,
        default=USERNAME,
        help="Your username/email associated with your rideco account.",
    )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        default=PASSWORD,
        help="Your rideco account password.",
    )
    parser.add_argument(
        "-e",
        "--export_types",
        type=str,
        default=EXPORT_TYPES,
        help="The export types to download.",
    )
    parser.add_argument(
        "-pr",
        "--programs",
        type=str,
        default=PROGRAMS,
        help="The rideco program codes to use.",
    )
    parser.add_argument(
        "-url",
        "--url_subdomain",
        type=str,
        default=URL_SUBDOMAIN,
        help="The url subdomain.",
    )

    args = parser.parse_args()
    date_list = create_date_range(
        start_date=args.start_date,
        end_date=args.end_date,
        month=args.month,
        year=args.year,
    )
    token = start_session_and_get_token(
        username=args.username, password=args.password, url_subdomain=args.url_subdomain
    )
    download_reports(
        date_list=date_list,
        url_subdomain=args.url_subdomain,
        export_types=args.export_types,
        programs=args.programs,
        token=token,
    )
