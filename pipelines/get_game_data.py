import argparse
import os
from db.db import engine
from etl.extract.fetch_game import fetch_game
from etl.transform.transform_game import transform_game
from etl.load.load_plate_appearances import load_plate_appearances
from etl.load.load_pitcher_innings import load_pitcher_innings
from etl.load.load_fieldable_plays import load_fieldable_plays

def get_game_data(gamePk: int):

    try:
        raw_filepath = fetch_game(gamePk)

        pi_filepath, pa_filepath, fp_filepath = transform_game(raw_filepath)

        load_plate_appearances(pa_filepath, engine)
        load_pitcher_innings(pi_filepath, engine)
        load_fieldable_plays(fp_filepath, engine)

        return (gamePk, "OK")
    except Exception as e:
        print(f"ETL failed for game {gamePk}: {e}")
        return (gamePk, f"ERROR: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gamePk", required=True, help="gamePk as recognized by MLB Stats API.")
    args = parser.parse_args()

    get_game_data(args.gamePk)

if __name__ == "__main__":
    main()