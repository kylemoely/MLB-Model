from utils.get_game_lists import get_game_list
from utils.fill_hit_data_na import fill_hit_data_na
from pipelines.get_game_data import get_game_data
import json
from dotenv import load_dotenv
import os
from pathlib import Path
from db.db import engine
import statsapi
import pandas as pd
from sqlalchemy import text
from models.p_out.model import save_model as save_p_out
from models.p_run.model import save_model as save_p_run
import lightgbm as lgb
from calculate.write_p_out_p_run import write_p_out_p_run
from traceback import format_exc
from calculate.calculate_game_features import calculate_game_features
from calculate.calculate_game_label import calculate_game_label

load_dotenv()
DATA_DIR = Path(os.getenv("DATA_DIR"))

def write_game_catalog(years):
    games = []
    for year in years:
        print(f"Starting {year}")
        gamePks = get_game_list(year)
        for gamePk in gamePks:
            game = statsapi.get("game", params={"gamePk":gamePk})
            date = game.get("gameData",{}).get("datetime",{}).get("officialDate")
            if date is None:
                print(f"No date found for game {gamePk}")
                continue
            games.append({"gamepk":gamePk,"game_date":date})
    df = pd.DataFrame(games)
    df.to_sql("game_catalog",engine,if_exists="append",index=False)
    
def fill_na():
    query = "SELECT * FROM fieldable_plays"
    with engine.begin() as conn:
        df = pd.read_sql(query, conn)

        df = fill_hit_data_na(df)
        updates = df[["id","launch_angle","launch_speed","total_distance"]]

        updates.to_sql("_fieldable_plays_updates",conn,if_exists="replace",index=False)

        conn.execute(text("""
            UPDATE fieldable_plays f
            SET
              launch_angle   = COALESCE(u.launch_angle,   f.launch_angle),
              launch_speed   = COALESCE(u.launch_speed,   f.launch_speed),
              total_distance = COALESCE(u.total_distance, f.total_distance)
            FROM _fieldable_plays_updates u
            WHERE u.id = f.id
              AND (u.launch_angle IS NOT NULL
                   OR u.launch_speed IS NOT NULL
                   OR u.total_distance IS NOT NULL);
        """))

        conn.execute(text("DROP TABLE _fieldable_plays_updates;"))

def get_games(years):
    for year in years:
        gamePks = get_game_list(year)
        results = [get_game_data(gamePk) for gamePk in gamePks]
        with open(DATA_DIR / f"results_{year}.json", "w") as f:
            json.dump(results, f, indent=4)

    fill_na()
                
def train_models():
    p_run_model_path = save_p_run("2021-01-01","2022-12-31")
    p_out_model_path = save_p_out("2021-01-01","2022-12-31")

def get_features(years):
    game_features_list = []
    game_feature_columns = ["gamepk", "away_pitcher_era","away_pitcher_whip","home_pitcher_era","home_pitcher_whip","away_batter1_ops","away_batter1_avg","away_batter2_ops","away_batter2_avg","away_batter3_ops","away_batter3_avg","away_batter4_ops","away_batter4_avg","away_batter5_ops","away_batter5_avg","home_batter1_ops","home_batter1_avg","home_batter2_ops","home_batter2_avg","home_batter3_ops","home_batter3_avg","home_batter4_ops","home_batter4_avg","home_batter5_ops","home_batter5_avg","away_oaa","away_drs","home_oaa","home_drs"]
    for year in years:
        gamePks = get_game_list(year)
        for gamePk in gamePks:
            if len(game_features_list) % 100 == 0:
                print(f"{len(game_features_list)} games processed.")
            try:
                with open(DATA_DIR / "raw" / f"gameData_{gamePk}.json") as f:
                    game = json.load(f)
            except Exception as e:
                print(f"Error while loading raw json file for game {gamePk}: {format_exc()}")
                continue
            try:
                game_features = [gamePk] + calculate_game_features(game, gamePk, engine)
                game_features_list.append(game_features)
            except Exception as e:
                print(f"Error while calculating features for game {gamePk}: {format_exc()}")
                continue
    df = pd.DataFrame(game_features_list, columns=game_feature_columns)
    try:
        df.to_sql("game_features",engine,if_exists="append",index=False)
    except Exception as e:
        df.to_excel(DATA_DIR / f"game_features_{years[0]}_{years[-1]}.xlsx")
        print(format_exc())

def get_labels(years):
    game_labels = []
    game_labels_columns = ["gamepk","label"]
    for year in years:
        gamePks = get_game_list(year)
        for gamePk in gamePks:
            try:
                with open(DATA_DIR / "raw" / f"gameData_{gamePk}.json") as f:
                    game = json.load(f)
            except Exception as e:
                print(f"Error while loading raw json file for game {gamePk}: {format_exc()}")
                continue
            try:
                game_label = [gamePk, calculate_game_label(game)]
                game_labels.append(game_label)
            except:
                print(f"Error while calculating game label for game {gamePk}: {format_exc()}")
                continue
    df = pd.DataFrame(game_labels, columns=game_labels_columns)
    try:
        df.to_sql("game_labels",engine, if_exists="append",index=False)
    except:
        df.to_excel(DATA_DIR / f"game_labels_{years[0]}_{years[-1]}.xlsx")
        print(format_exc())


def main():
    # print("Writing game catalog")
    # write_game_catalog([2021,2022,2023,2024])
    # print("Getting 2021 and 2022 games")
    # get_games([2021,2022])
    # print("Training p_out and p_run")
    # train_models()
    # print("Getting 2023 and 2024 games")
    # get_games([2023,2024])
    # print("Writing p_out and p_run stats")
    # write_p_out_p_run()
    print("Calculating game features")
    get_features([2023,2024])
    print("Calculating game labels")
    get_labels([2023,2024])

if __name__ == "__main__":
    main()
