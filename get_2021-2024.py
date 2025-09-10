from __future__ import annotations
from db.db import engine
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List, Tuple
import os, json
from pipelines.get_game_data import get_game_data

def run_batch(gamePks):
    successes = 0
    failures = []

    with ThreadPoolExecutor(max_workers=20, thread_name_prefix="etl") as pool:
        futures = {pool.submit(get_game_data, int(pk)): int(pk) for pk in gamePks}
        for fut in as_completed(futures):
            pk = futures[fut]
            gamePk, status = fut.result()
            if status=="OK":
                successes += 1
                if successes % 50 == 0:
                    print(f"{successes} games successfully processed.")
            else:
                failures.append((gamePk, status))
                print(f"Game {gamePk} failed: {status}")
    if failures:
        with open("retry_failed_games.json", "w", encoding="utf-8") as f:
            json.dump([{"gamePk":g, "reason": stat} for g, stat in failures], f)
        print(f"{len(failures)} games saved to retry_failed_games.json for retry.")
    return successes, failures

if __name__ == "__main__":
    for file in ["games_2021.json"]:
        with open(file, "r", encoding="utf-8") as f:
            gamePks = json.load(f)
        run_batch(set(gamePks))