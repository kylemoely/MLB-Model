import statsapi
import json
import argparse

def fetch_daily_schedule(date):
    schedule = statsapi.get("schedule", params={"sportId":1, "startDate": date, "endDate":date})
    filepath = f"schedule_{date}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=4)
    return filepath

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Date for which you want to fetch games, format `YYYY-MM-DD`.")
    args = parser.parse_args()

    fetch_daily_schedule(args.date)

if __name__ == "__main__":
    main()