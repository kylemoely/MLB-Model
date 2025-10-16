import pandas as pd

def get_batter_df(batter_id, game_date, engine):
    query = f"SELECT is_at_bat, is_hit, is_walk, is_sac, bases FROM plate_appearances p INNER JOIN game_catalog g ON p.gamepk = g.gamepk WHERE batter_id = {batter_id}  AND game_date < '{game_date}' ORDER BY game_date DESC LIMIT 50"
    df = pd.read_sql(query, engine)

    return df

def get_pitcher_df(pitcher_id, game_date, engine):
    query = f"WITH ordered AS (SELECT *, SUM(outs) OVER(ORDER BY game_date DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_outs FROM pitcher_innings p INNER JOIN game_catalog g ON p.gamepk = g.gamepk WHERE pitcher_id = {pitcher_id} AND game_date < '{game_date}') SELECT hits_allowed, walks_allowed, earned_runs, outs FROM ordered WHERE running_outs<=60"
    df = pd.read_sql(query, engine)

    return df

def get_new_fieldable_plays(conn):
    query = f"SELECT * FROM fieldable_plays WHERE p_out IS NULL OR p_run IS NULL"
    df = pd.read_sql(query, conn)

    return df

def get_fielder_df(fielder_id, game_date, engine):
    query = f"SELECT in_play_out, has_score, p_out, p_run FROM fieldable_plays f INNER JOIN game_catalog g ON f.gamepk = g.gamepk WHERE game_date < '{game_date}' AND responsibility = {fielder_id} ORDER BY game_date DESC LIMIT 50"
    df = pd.read_sql(query,engine)

    return df
