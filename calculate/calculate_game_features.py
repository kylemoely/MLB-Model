from .calculators import calculate_AVG, calculate_ERA, calculate_OPS, calculate_WHIP
from .queries import get_batter_df, get_pitcher_df

def calculate_game_features(game, gamePk, engine, home_pitcher_id=None, away_pitcher_id=None):
    gameData = game.get("gameData", {})
    game_date = gameData.get("datetime", {}).get("officialDate")
    if game_date is None:
        raise ValueError(f"Cannot find game_date for game {gamePk}.")
    
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
    if away_pitcher_id is None or home_pitcher_id is None:
        raise ValueError("pitcher_ids not found.")
        
    boxscore_teams = game.get("liveData",{}).get("boxscore",{}).get("teams")
    away_batters = boxscore_teams.get("away",{}).get("battingOrder")
    home_batters = boxscore_teams.get("home",{}).get("battingOrder")
    if home_batters is None or away_batters is None:
        raise ValueError("batter_ids not found.")
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

    return features