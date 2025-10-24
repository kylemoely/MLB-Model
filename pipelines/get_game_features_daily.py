from ast import Try
from db.db import engine
from calculate.calculate_game_features import calculate_game_features
import json
from dotenv import load_dotenv
import os
from pathlib import Path
import pandas as pd

DATA_DIR = f"{os.getenv('DATA_DIR').rstrip('/')}/raw"

def get_game_features_daily():
    try:
        df = pd.read_sql("SELECT g.gamepk FROM game_catalog g LEFT JOIN game_features gf ON g.gamepk = gf.gamepk WHERE gf.gamepk IS NULL", engine)
    except Exception as e:
        raise Exception(f"Error while selecting new gamepks: {e}")
    gamepks = df["gamepk"].values
    features = []
    for gamepk in gamepks:
        try:
            with open(f"{DATA_DIR}/gameData_{gamepk}.json") as f:
                game = json.load(f)
            features.append(calculate_game_features(game,gamepk,engine))
        except Exception as e:
            print(f"Error while calculating features for game {gamepk}: {e}")
            continue
    if len(features) > 0:
        columns = ["gamepk","away_pitcher_era","away_pitcher_whip","home_pitcher_era","home_pitcher_whip","away_batter1_ops","away_batter1_avg","away_batter2_ops","away_batter2_avg","away_batter3_ops","away_batter3_avg","away_batter4_ops","away_batter4_avg","away_batter5_ops","away_batter5_avg","home_batter1_ops","home_batter1_avg","home_batter2_ops","home_batter2_avg","home_batter3_ops","home_batter3_avg","home_batter4_ops","home_batter4_avg","home_batter5_ops","home_batter5_avg","away_oaa","away_drs","home_oaa","home_drs"]
        df_features = pd.DataFrame(features, columns=columns)
        df_features.to_sql("game_features",engine, if_exists="append",index=False)
        print(f"{len(df_features)} records added to game_features.")
    else:
        print("No game features successfully added for today.")
