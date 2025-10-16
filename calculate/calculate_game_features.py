from .calculators import calculate_AVG, calculate_ERA, calculate_OPS, calculate_WHIP, calculate_OAA, calculate_DRS
from .queries import get_batter_df, get_pitcher_df, get_fielder_df
import pandas as pd

def calculate_defense_features(fielders, game_date, engine):
    fielder_dfs = [get_fielder_df(fielder, game_date, engine) for fielder in fielders]
    fielder_dfs = [df for df in fielder_dfs if not df.empty and not df.isna().all().all()]
    team_df = pd.concat(fielder_dfs,ignore_index=True)
    oaa = calculate_OAA(team_df)
    drs = calculate_DRS(team_df)

    return oaa, drs


def calculate_game_features(game, gamePk, engine):
    gameData = game.get("gameData", {})
    game_date = gameData.get("datetime", {}).get("officialDate")
    if game_date is None:
        raise AttributeError("Cannot find game_date.")
    
    features = []
    
    probable_pitchers = gameData.get("probablePitchers",{})
    away_pitcher_id = probable_pitchers.get("away",{}).get("id")
    home_pitcher_id = probable_pitchers.get("home",{}).get("id")
    if away_pitcher_id is None or home_pitcher_id is None:
        plays = game.get("liveData",{}).get("plays", {}).get("allPlays",[{}])
        home_pitcher_id = plays[0].get("matchup",{}).get("pitcher",{}).get("id")
        for play in plays:
            if play.get("halfInning")=="bottom":
                away_pitcher_id = play.get("matchup",{}).get("pitcher",{}).get("id")
                break
    if away_pitcher_id is None:
        raise AttributeError("Cannot find away pitcher's id.")
    if home_pitcher_id is None:
        raise AttributeError("Cannot find home pitcher's id.")
        
    boxscore_teams = game.get("liveData",{}).get("boxscore",{}).get("teams")
    away = boxscore_teams.get("away",{})
    home = boxscore_teams.get("home",{})
    away_batters = away.get("battingOrder")
    home_batters = home.get("battingOrder")
    if home_batters is None or len(home_batters)==0:
        raise AttributeError("Cannot find batting order for home team.")
    if away_batters is None:
        raise AttributeError("Cannot find batting order for away team.")
    
    away_players = away.get("players")
    home_players = home.get("players")
    if away_players is None or len(away_players)==0:
        raise AttributeError("Cannot find player information for away team.")
    if home_players is None or len(home_players)==0:
        raise AttributeError("Cannot find player information for home team.")
    away_fielders = []
    home_fielders = []
    for batter in away_batters:
        player = away_players.get(f"ID{batter}")
        if player.get("position",{}).get("abbreviation")!="DH":
            away_fielders.append(batter)
    for batter in home_batters:
        player = home_players.get(f"ID{batter}")
        if player.get("position",{}).get("abbreviation")!="DH":
            home_fielders.append(batter)
    away_fielders.append(away_pitcher_id)
    home_fielders.append(home_pitcher_id)
    
    away_batters = away_batters[:5]
    home_batters = home_batters[:5]

    for pitcher_id in [away_pitcher_id, home_pitcher_id]:
        pitcher_df = get_pitcher_df(pitcher_id, game_date, engine)
        era = calculate_ERA(pitcher_df)
        whip = calculate_WHIP(pitcher_df)

        features += [era, whip]

    for batters in [away_batters,home_batters]:
        for batter_id in batters:
            batter_df = get_batter_df(batter_id,game_date,engine)
            ops = calculate_OPS(batter_df)
            avg = calculate_AVG(batter_df)
            
            features += [ops, avg]

    away_OAA, away_DRS = calculate_defense_features(away_fielders, game_date, engine)
    home_OAA, home_DRS = calculate_defense_features(home_fielders, game_date, engine)
    features += [away_OAA,away_DRS,home_OAA,home_DRS]

    return features
