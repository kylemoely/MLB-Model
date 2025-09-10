import pandas as pd

def builder_plate_appearances(plays):

    columns = ["batter_id","pitcher_id","inning","event_type","is_at_bat","is_walk","is_sac","is_hit","bases"]
    records = []
    for play in plays:
        records.append([play[col] for col in columns])

    df = pd.DataFrame(records, columns=columns)

    return df

def builder_pitcher_innings(plays):

    columns = ["pitcher_id","inning","hits_allowed","walks_allowed","earned_runs","outs"]
    records = []
    pitcher_id = plays[0]["pitcher_id"]
    hits_allowed = 0
    walks_allowed = 0
    earned_runs = 0
    outs = 0
    for play in plays:
        if play["pitcher_id"]!=pitcher_id:
            records.append([pitcher_id, inning, hits_allowed, walks_allowed, earned_runs, outs])
            pitcher_id = play["pitcher_id"]
            hits_allowed = 0
            walks_allowed = 0
            earned_runs = 0
            outs = 0
        inning = play["inning"]
        if play["is_hit"]:
            hits_allowed += 1
        if play["is_walk"]:
            walks_allowed += 1
        earned_runs += play["earned_runs"]
        outs += play["outs"]
    df = pd.DataFrame(records, columns=columns)

    return df