from pipelines.get_game_catalog_daily import get_game_catalog_daily
from pipelines.get_game_datas_daily import get_game_datas_daily
from pipelines.get_game_features_daily import get_game_features_daily
from datetime import datetime

def main():
    try:
        get_game_datas_daily()
    except Exception as e:
        print(f"Error getting game datas from yesterday: {e}")

    try:
        try:
            get_game_catalog_daily()
        except Exception as e:
            raise Exception(e)
        
        try:
            get_game_features_daily()
        except Exception as e:
            raise Exception(e)
    except Exception as e:
        print(f"Error while ingesting game data for upcoming games: {e}")

if __name__ == "__main__":
    main()