import statsapi
import json

def get_game_list(year):
    season = statsapi.get("season", params={"seasonId":year, "sportId":1})
    season = season["seasons"][0]
    start_date = season["regularSeasonStartDate"]
    end_date = season["regularSeasonEndDate"]

    schedule = statsapi.get("schedule", params={"sportId":1, "startDate": start_date, "endDate": end_date})

    gamePks = []

    for date in schedule["dates"]:
        for game in date["games"]:
            if game["seriesDescription"]=="Regular Season" and game["status"]["detailedState"] not in ["Cancelled","Postponed"]:
                gamePks.append(game["gamePk"])
    return list(set(gamePks))