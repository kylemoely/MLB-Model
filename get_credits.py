import statsapi
import pandas as pd
import json
from tqdm import tqdm

def get_credits():
    with open("games_2024.json") as f:
        gamePks = json.load(f)
    
    gamePks = set(gamePks)
    
    columns = ["gamePk","inning", "play_description", "player_id", "credit"]
    df_credits = []

    for gamePk in tqdm(gamePks):
        game = statsapi.get("game", params={"gamePk":gamePk})

        plays = game["liveData"]["plays"]["allPlays"]

        for play in plays:
            inning = play["about"]["inning"]
            play_description = play["result"]["description"]

            runners = play.get("runners", [])
            for runner in runners:
                credits = runner.get("credits", [])
                for credit in credits:
                    player_id = credit.get("player",{}).get("id")
                    credit_type = credit.get("credit")
                    df_credit = [gamePk, inning, play_description, player_id, credit_type]
                    df_credits.append(df_credit)
    
    df = pd.DataFrame(df_credits, columns=columns)
    df.to_excel("df_credits.xlsx")
    return df


if __name__ == "__main__":
    get_credits()