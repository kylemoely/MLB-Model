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

load_dotenv()
DATA_DIR = Path(os.getenv("DATA_DIR"))

def main():
    for year in [2021,2022]:
        gamePks = get_game_list(year)
        results = [get_game_data(gamePk) for gamePk in gamePks]
        with open(DATA_DIR / f"results_{year}.json", "w") as f:
            json.dump(results, f, indent=4)
def write_game_catalog():
    games = []
    for year in [2021,2022]:
        gamePks = get_game_list(year)
        for gamePk in gamePks:
            print(gamePk)
            game = statsapi.get("game", params={"gamePk":gamePk})
            date = game.get("gameData",{}).get("datetime",{}).get("officialDate")
            if date is None:
                print(f"No date found for game {gamePk}")
                continue
            games.append({"gamepk":gamePk,"game_date":date})
    df = pd.DataFrame(games)
    df.to_sql("game_catalog",engine,if_exists="append",index=False)
                
# def train_models():
#     p_run_model_path = save_p_run("2021-01-01","2022-12-31")
#     p_out_model_path = save_p_out("2021-01-01","2022-12-31")


if __name__ == "__main__":
    write_game_catalog()