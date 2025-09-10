import pandas as pd
import json
import argparse

def transform_daily_schedule(filepath):
    with open(filepath, "r") as f:
        schedule = json.load(f)

    gamePks = []
                                                                            
    for item in schedule.get("dates",[]):
        date = item.get("date")
        for game in item.get("games",[]):
            gamePk = game.get("gamePk")
            gamePks.append({"gamePk":gamePk,"date":date})
    parq_filepath = filepath.replace(".json",".parquet")

    df = pd.DataFrame(gamePks)
    df.to_parquet(parq_filepath, engine="pyarrow", index=False)

    return parq_filepath

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", required=True, help="Filepath where raw json file is.")
    args = parser.parse_args()

    transform_daily_schedule(args.filepath)

if __name__ == "__main__":
    main()