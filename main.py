#!/usr/bin/python
"""Main script for SRP Price Plans."""
import argparse
import csv
from datetime import datetime as dt
import os

from dotenv import load_dotenv


def main(usage_path):
    """Fetch main data."""
    assert len(usage_path) > 0
    print(f"Using {usage_path}")

    format_data = "%m/%d/%Y %I:%M %p"

    with open(usage_path, encoding="utf-8") as usage_file:
        reader = csv.reader(usage_file, delimiter=",")

        # skip header
        next(reader)

        max_usage = 0.0
        last_datetime = dt.now()
        for date_str, hour_str, _, usage in reader:
            # 4/1/2021 2:00 AM
            cur_datetime = dt.strptime(f"{date_str} {hour_str}", format_data)
            if cur_datetime.date() != last_datetime.date():
                last_datetime = cur_datetime
                print(f"New Date: {last_datetime}")
            if float(usage) > max_usage:
                max_usage = float(usage)

        print(f"Max Usage is: {max_usage}")


if __name__ == "__main__":
    load_dotenv(".env")

    parser = argparse.ArgumentParser(
        description="SRP Price Plans.",
        add_help=True,
    )
    parser.add_argument(
        "--usage_path",
        "-u",
        help="Hourly usage data",
    )
    args = parser.parse_args()

    USAGE_PATH = args.usage_path or os.environ.get("USAGE_PATH")

    if not USAGE_PATH:
        raise ValueError(
            "Usage path is required. Have you set the USAGE_PATH env variable?"
        )

    main(USAGE_PATH)
