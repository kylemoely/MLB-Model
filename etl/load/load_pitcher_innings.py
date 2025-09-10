import pandas as pd

def load_pitcher_innings(filepath, engine):

    df = pd.read_parquet(filepath)

    if len(df)==0 or list(df.columns)!=["pitcher_id","inning","hits_allowed","walks_allowed","earned_runs","outs", "gamepk", "game_date"]:
        raise Exception(f"Improper dataframe from {filepath}")

    df.to_sql("pitcher_innings",engine, if_exists="append", index=False)

    print("Pitcher innings successfully loaded.")