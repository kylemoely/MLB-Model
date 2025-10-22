import statsapi
import json
import argparse
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
DATA_DIR = Path(os.getenv("DATA_DIR"))

### AWS Dev
import s3fs
fs = s3fs.S3FileSystem()

def fetch_daily_schedule(date):
    schedule = statsapi.get("schedule", params={"sportId":1, "startDate": date, "endDate":date})
    filepath = str(DATA_DIR / f"raw/daily-schedules/schedule_{date}.json")
    ### Local Dev
    # with open(filepath, "w", encoding="utf-8") as f:
    #     json.dump(schedule, f, indent=4)
    ### AWS Dev
    with fs.open(filepath, "w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=4)
    return filepath

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Date for which you want to fetch games, format `YYYY-MM-DD`.")
    args = parser.parse_args()

    fetch_daily_schedule(args.date)

if __name__ == "__main__":
    main()
