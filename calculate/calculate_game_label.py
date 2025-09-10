def calculate_game_label(game):
    liveData = game.get("liveData",{})
    linescore = liveData.get("linescore",{})
    first_inning = linescore.get("innings",[{}])[0]
    home_runs = first_inning.get("home",{}).get("runs")
    away_runs = first_inning.get("away",{}).get("runs")
    if home_runs is None or away_runs is None:
        raise ValueError("First inning run data not found.")
    return home_runs + away_runs > 0