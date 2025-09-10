import json
from pathlib import Path
from .builders import builder_pitcher_innings, builder_plate_appearances
from .parsers import parse_plays
import argparse
from dotenv import load_dotenv
import os

load_dotenv()

DATA_DIR = Path(os.getenv("DATA_DIR"))
CLEAN_DATA_DIR = DATA_DIR / "clean"

def transform_game(filepath: Path):

    with open(filepath, "r") as f:
        game = json.load(f)
    #prolly check for some errors here but we'll do that later
        
    filename = filepath.name

    date = game.get("gameData",{}).get("datetime",{}).get("officialDate")
    plays = game["liveData"]["plays"]["allPlays"]
    parsed_plays = parse_plays(plays)

    #filepath should be 'gameData_{gamePk}.json'
    gamePk = int(filename.replace(".json","").replace("gameData_",""))

    pa_df = builder_plate_appearances(parsed_plays)
    pi_df = builder_pitcher_innings(parsed_plays)
    pa_df["gamepk"] = gamePk
    pi_df["gamepk"] = gamePk
    pa_df["game_date"] = date
    pi_df["game_date"] = date

    pi_filepath = CLEAN_DATA_DIR / filename.replace(".json","_pitcher_innings.parquet")
    pa_filepath = CLEAN_DATA_DIR / filename.replace(".json","_plate_appearances.parquet")

    pa_df.to_parquet(pa_filepath, engine="pyarrow", index=False)
    pi_df.to_parquet(pi_filepath, engine="pyarrow", index=False)

    #print(f"Successfully saved both parquet files at {pa_filepath} and {pi_filepath}.")

    return pi_filepath, pa_filepath

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", required=True, help="Filepath where raw json is.")
    args = parser.parse_args()

    transform_game(Path(args.filepath))

if __name__ == "__main__":
    main()