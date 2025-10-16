import pandas as pd

def load_daily_schedule(filepath, engine):

    df = pd.read_parquet(filepath)
    if len(df)==0 or list(df.columns)!=["gamepk","game_date"]:
        raise AssertionError(f"Improper dataframe from {filepath}")

    df.to_sql("game_catalog",engine,if_exists="append",index=False)
