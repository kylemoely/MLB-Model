import pandas as pd

def load_fieldable_plays(filepath, engine):

    df = pd.read_parquet(filepath)

    if len(df)==0 or list(df.columns)!=["launch_speed","launch_angle","total_distance","trajectory","hardness","hit_location","coord_x","coord_y","fielder","fielder_id","putouter","putouter_id", "errer","errer_id","in_play_out","pickoff_out","has_out","has_score","first_base_runner","second_base_runner","third_base_runner","num_outs","responsibility","gamepk"]:
        raise Exception(f"Improper dataframe from {filepath}")

    df.to_sql("fieldable_plays",engine, if_exists="append", index=False)
