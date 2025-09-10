import statsapi
import json

def get_game_lists():
    for year in [2021,2022,2023,2024]:
        gamePks = []
        season = statsapi.get("season", params = {"sportId":1, "seasonId":year})
        start = season["seasons"][0]["regularSeasonStartDate"]
        end = season["seasons"][0]["regularSeasonEndDate"]

        schedule = statsapi.get("schedule", params={"sportId":1,"startDate":start, "endDate": end})

        dates = schedule["dates"]
        for date in dates:
            games = date["games"]
            for game in games:
                if game["seriesDescription"]=="Regular Season" and game["status"]["detailedState"] not in ["Cancelled", "Postponed"]:
                    gamePks.append(game["gamePk"])

        with open(f"games_{year}.json", "w", encoding="utf-8") as f:
            json.dump(gamePks, f)
        print(f"Succesfully saved {len(set(gamePks))} games to games_{year}.json")

if __name__ == "__main__":
    get_game_lists()