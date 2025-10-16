from models.p_run.train import train_p_run
from models.p_run.data import preprocess_data, get_data
from db.db import engine
from pathlib import Path
from datetime import datetime
import lightgbm as lgb

root = Path(__file__).resolve().parents[2]
artifacts = root / "artifacts" / "p_run"

def save_model(start_date, end_date):
    df = get_data(start_date, end_date, engine)

    train_data, test_data = preprocess_data(df)

    p_run = train_p_run(train_data,test_data)

    date_folder = artifacts / datetime.now().strftime("%Y-%m-%d")
    date_folder.mkdir(exist_ok=True)
    model_path = date_folder / "model.txt"

    p_run.save_model(str(model_path))

    return model_path

def get_model(training_date=None):
    if training_date is not None:
        model_file = artifacts / training_date / "model.txt"
        if not model_file.exists():
            raise Exception(f"No model found at {str(model_file)}")
    else:
        training_dates = [(datetime.strptime(f.name,"%Y-%m-%d"),f / "model.txt") for f in artifacts.iterdir() if f.is_dir()]
        if len(training_dates)==0:
            raise Exception(f"No models found")
        model_file = max(training_dates, key=lambda x:x[0])[1]
   
    p_run = lgb.Booster(model_file=model_file)
    
    return p_run
