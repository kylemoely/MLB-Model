import statsapi
import json
from pathlib import Path
import argparse
from dotenv import load_dotenv
import os

load_dotenv()

DATA_DIR = Path(os.getenv("DATA_DIR"))
RAW_DATA_DIR = DATA_DIR / "raw"

def fetch_game(gamePk: int) -> Path:

    game = statsapi.get("game", params={"gamePk":gamePk})
    filepath = RAW_DATA_DIR / f"gameData_{gamePk}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(game, f, indent=4)

    #print(f"Succesfully saved raw JSON file at {filepath}.")
    return filepath

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gamePk", required=True, help="gamePk as recognized by MLB Stats API.")
    args = parser.parse_args()

    fetch_game(args.gamePk)

if __name__ == "__main__":
    main()