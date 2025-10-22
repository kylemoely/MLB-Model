import json
from pathlib import Path
from .builders import builder_pitcher_innings, builder_plate_appearances, builder_fieldable_plays
from .parsers import parse_plays
import argparse
from dotenv import load_dotenv
import os
import s3fs

load_dotenv()
fs = s3fs.S3FileSystem()

DATA_DIR = Path(os.getenv("DATA_DIR"))
CLEAN_DATA_DIR = DATA_DIR / "clean"

def transform_game(filepath):
    ### Local Dev
    # with open(filepath, "r") as f:
    #     game = json.load(f)
    ### AWS Dev
    with fs.open(filepath) as f:
        game = json.load(f)
        
    filename = filepath.name

    plays = game["liveData"]["plays"]["allPlays"]
    parsed_plays = parse_plays(plays)

    #filepath should be 'gameData_{gamePk}.json'
    gamePk = int(filename.replace(".json","").replace("gameData_",""))

    pa_df = builder_plate_appearances(parsed_plays, gamePk)
    pi_df = builder_pitcher_innings(parsed_plays, gamePk)
    fp_df = builder_fieldable_plays(parsed_plays, gamePk)

    pi_filepath = str(CLEAN_DATA_DIR / filename.replace(".json","_pitcher_innings.parquet"))
    pa_filepath = str(CLEAN_DATA_DIR / filename.replace(".json","_plate_appearances.parquet"))
    fp_filepath = str(CLEAN_DATA_DIR / filename.replace(".json","_fieldable_plays.parquet"))

    pa_df.to_parquet(pa_filepath, index=False)
    pi_df.to_parquet(pi_filepath, index=False)
    fp_df.to_parquet(fp_filepath, index=False)

    #print(f"Successfully saved both parquet files at {pa_filepath} and {pi_filepath}.")

    return pi_filepath, pa_filepath, fp_filepath

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", required=True, help="Filepath where raw json is.")
    args = parser.parse_args()

    transform_game(args.filepath)

if __name__ == "__main__":
    main()
