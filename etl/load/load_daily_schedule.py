import pandas as pd

def load_daily_schedule(filepath, engine):

    df = pd.read_parquet(filepath)

    df.to_sql("game_catalog",engine,if_exists="append",index=False)
