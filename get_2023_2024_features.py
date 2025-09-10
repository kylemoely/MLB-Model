# run_game_features.py
from __future__ import annotations
import os, json, logging, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List, Tuple, Optional
import traceback

import pandas as pd
from sqlalchemy import text
from db.db import engine
from calculate.calculate_game_features import calculate_game_features

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(threadName)s %(message)s"
)

RAW_DIR = r"C:/Users/Kyle/Desktop/Projects/MLB Stats/data/raw"
FEATURE_COLUMNS = [
    "gamepk",
    "away_pitcher_era","away_pitcher_whip","home_pitcher_era","home_pitcher_whip",
    "away_batter1_ops","away_batter1_avg","away_batter2_ops","away_batter2_avg",
    "away_batter3_ops","away_batter3_avg","away_batter4_ops","away_batter4_avg",
    "away_batter5_ops","away_batter5_avg",
    "home_batter1_ops","home_batter1_avg","home_batter2_ops","home_batter2_avg",
    "home_batter3_ops","home_batter3_avg","home_batter4_ops","home_batter4_avg",
    "home_batter5_ops","home_batter5_avg",
]

def process_one(gamepk: int) -> Optional[List]:
    """
    Load raw JSON for a single game, compute features, and return a row list:
    [gamepk, feat1, feat2, ...]. Returns None on failure.
    """
    try:
        raw_path = os.path.join(RAW_DIR, f"gameData_{gamepk}.json")
        with open(raw_path, "r", encoding="utf-8") as f:
            game = json.load(f)
    except Exception as e:
        logging.warning(f"[{gamepk}] Failed to load raw JSON: {e}")
        return None

    try:
        features = calculate_game_features(game, gamepk, engine)  # must return list in expected order
        return [gamepk] + features
    except Exception as e:
        logging.warning(f"[{gamepk}] Feature calc failed: {e}")
        return None

def run_batch(gamepks: Iterable[int]) -> Tuple[int, int]:
    rows: List[List] = []
    successes = 0
    failures = 0

    with ThreadPoolExecutor(max_workers=1, thread_name_prefix="features") as pool:
        futs = {pool.submit(process_one, int(pk)): int(pk) for pk in gamepks}
        for i, fut in enumerate(as_completed(futs), 1):
            pk = futs[fut]
            row = fut.result()
            if row is None:
                failures += 1
            else:
                rows.append(row)
                successes += 1
                if successes % 100 == 0:
                    logging.info(f"Saved {successes} games so far...")

    logging.info(f"Complete. Success={successes}, Failed={failures}")

    if rows:
        df = pd.DataFrame(rows, columns=FEATURE_COLUMNS)
        # write in chunks to avoid giant single transaction
        try:
            df.to_sql("game_features", engine, if_exists="append", index=False, chunksize=1000, method=None)
        except Exception as e:
            df.to_excel("game_features.xlsx")
            print(traceback.format_exc())
            sys.exit()
        logging.info(f"Wrote {len(df)} rows to game_features.")
    return successes, failures

if __name__ == "__main__":
    for file in ["games_2023.json", "games_2024.json"]:
        with open(file, "r", encoding="utf-8") as f:
            gamepks = set(json.load(f))  # e.g., [716001, 716002, ...]
        run_batch(gamepks)
