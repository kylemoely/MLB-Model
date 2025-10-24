from db.db import engine
from etl.extract.fetch_daily_schedule import fetch_daily_schedule
from etl.transform.transform_daily_schedule import transform_daily_schedule
from etl.load.load_daily_schedule import load_daily_schedule
from datetime import datetime, timedelta

def get_game_catalog_daily():
    try:
        now = datetime.now()
        then = now - timedelta(days=211)
        raw_filepath = fetch_daily_schedule(then.strftime("%Y-%m-%d"))

        sched_filepath = transform_daily_schedule(raw_filepath)

        load_daily_schedule(sched_filepath, engine)
    except Exception as e:
        print(f"Daily schedule ingestion failed: {e}")

if __name__ == "__main__":
    get_game_catalog_daily()

