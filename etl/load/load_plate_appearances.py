import pandas as pd

def load_plate_appearances(filepath, engine):

    df = pd.read_parquet(filepath)

    if len(df)==0 or list(df.columns)!=["batter_id","pitcher_id","inning","event_type","is_at_bat","is_walk","is_sac","is_hit","bases", "gamepk"]:
        raise Exception(f"Improper dataframe from {filepath}")

    df.to_sql("plate_appearances", engine, if_exists="append",index=False)

    print("Plate appearances successfully loaded.")