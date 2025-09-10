import pandas as pd

def get_batter_df(batter_id, game_date, engine):
    query = f"SELECT is_at_bat, is_hit, is_walk, is_sac, bases FROM plate_appearances WHERE batter_id = {batter_id}  AND game_date < CAST('{game_date}' AS date) ORDER BY game_date DESC LIMIT 50"
    df = pd.read_sql(query, engine)

    return df

def get_pitcher_df(pitcher_id, game_date, engine):
    query = f"WITH ordered AS (SELECT *, SUM(outs) OVER(ORDER BY game_date DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_outs FROM pitcher_innings WHERE pitcher_id = {pitcher_id} AND game_date < CAST('{game_date}' AS date)) SELECT hits_allowed, walks_allowed, earned_runs, outs FROM ordered WHERE running_outs<=32"
    df= pd.read_sql(query, engine)

    return df