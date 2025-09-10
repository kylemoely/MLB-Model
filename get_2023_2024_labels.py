from db.db import engine
import json 
import pandas as pd 
from calculate.calculate_game_label import calculate_game_label
from traceback import format_exc

def run_batch(gamePks):
    game_labels = []
    game_labels_columns = ["gamepk","label"]

    for gamePk in gamePks:
        try:
            with open(f"C:/Users/Kyle/Desktop/Projects/MLB Stats/data/raw/gameData_{gamePk}.json", "r", encoding="utf-8") as f: 
                game = json.load(f)
        except Exception as e: 
            print(f"Error while loading raw json file for game {gamePk}: {format_exc()}") 
            continue 
        try:
            game_label = [gamePk, calculate_game_label(game)]
            game_labels.append(game_label)
        except:
            print(f"Error while calculating features for game {gamePk}: {format_exc()}") 
            continue
        if len(game_labels) % 100 == 0: 
            print(f"{len(game_labels)} games successfully saved.") 
    df = pd.DataFrame(game_labels, columns=game_labels_columns)
    try:
        df.to_sql("game_labels", engine, if_exists="append", index=False)
    except:
        df.to_excel(f"game_labels{gamePks[0]}.xlsx")
        print(format_exc())

if __name__ == "__main__": 
    for file in ["games_2023.json", "games_2024.json"]: 
        with open(file, "r", encoding="utf-8") as f: 
            gamePks = json.load(f) 
        run_batch(list(set(gamePks)))