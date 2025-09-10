from db.db import engine
import json 
import pandas as pd 
from calculate.calculate_game_features import calculate_game_features
from traceback import format_exc

def run_batch(gamePks): 
    game_features_list = [] 
    game_feature_columns = ["gamepk", "away_pitcher_era","away_pitcher_whip","home_pitcher_era","home_pitcher_whip","away_batter1_ops","away_batter1_avg","away_batter2_ops","away_batter2_avg","away_batter3_ops","away_batter3_avg","away_batter4_ops","away_batter4_avg","away_batter5_ops","away_batter5_avg","home_batter1_ops","home_batter1_avg","home_batter2_ops","home_batter2_avg","home_batter3_ops","home_batter3_avg","home_batter4_ops","home_batter4_avg","home_batter5_ops","home_batter5_avg"]
    print(f"Starting with game {list(gamePks)[0]}!")
    for gamePk in gamePks: 
        try: 
            with open(f"C:/Users/Kyle/Desktop/Projects/MLB Stats/data/raw/gameData_{gamePk}.json", "r", encoding="utf-8") as f: 
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
        if len(game_features_list) % 100 == 0: 
            print(f"{len(game_features_list)} games successfully saved.") 
    df = pd.DataFrame(game_features_list, columns=game_feature_columns) 
    try:
        df.to_sql("game_features", engine, if_exists="append", index=False) 
    except Exception as e:
        df.to_excel(f"game_features_{list(gamePks)[0]}.xlsx")
        print(format_exc())

if __name__ == "__main__": 
    for file in ["games_2023.json", "games_2024.json"]: 
        with open(file, "r", encoding="utf-8") as f: 
            gamePks = json.load(f) 
        run_batch(set(gamePks))