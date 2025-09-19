import pandas as pd

def load_fieldable_plays(filepath, engine):

    df = pd.read_parquet(filepath)

    if len(df)==0 or list(df.columns)!=["launch_speed","launch_angle","total_distance","trajectory","hardness","location","coord_x","coord_y","fielder","fielder_id","outer","outer_id", "errer","errer_id","out","pickoff_out","has_out","has_score","first_base_runner","second_base_runner","third_base_runner","num_outs","gamepk","date"]:
        raise Exception(f"Improper dataframe from {filepath}")

    df.to_sql("fieldable_plays",engine, if_exists="append", index=False)
