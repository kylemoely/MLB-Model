import statsapi
import json
import argparse
from dotenv import load_dotenv
import os
import s3fs

load_dotenv()
fs = s3fs.S3FileSystem()

DATA_DIR = os.getenv("DATA_DIR").rstrip("/")
RAW_DATA_DIR = f"{DATA_DIR}/raw/game-datas"

def fetch_game(gamePk: int):

    game = statsapi.get("game", params={"gamePk":gamePk})
    filepath = f"{RAW_DATA_DIR}/gameData_{gamePk}.json"
    ### Local Dev
    # with open(filepath, "w", encoding="utf-8") as f:
    #     json.dump(game, f, indent=4)
    ### AWS Dev
    with fs.open(filepath, "w", encoding="utf-8") as f:
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
