import pandas as pd
from db.db import engine
from pipelines.get_game_data import get_game_data
from dotenv import load_dotenv
import os
import json
from pathlib import Path
from datetime import datetime
import s3fs

load_dotenv()
fs = s3fs.S3FileSystem()

DATA_DIR = os.getenv("DATA_DIR").rstrip("/")
DIR = f"{DATA_DIR}/daily_game_datas"

def get_game_datas_daily():
	try:
		df = pd.read_sql("SELECT gamepk FROM game_catalog WHERE status = 'NEW'", engine)
		gamepks = df["gamepk"].values
		results = [get_game_data(gamepk) for gamepk in gamepks]

		with fs.open(f"{DIR}/results_{datetime.now().strftime('%Y-%m-%d')}.json", "w") as f:
			json.dump(results, f, indent=4)
	except Exception as e:
		print(f"Error trying to get daily game_datas: {e}")

if __name__ == "__main__":
	get_game_datas_daily()
