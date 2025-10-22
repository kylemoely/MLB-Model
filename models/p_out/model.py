from models.p_out.train import train_p_out
from models.p_out.data import preprocess_data, get_data
from db.db import engine
from datetime import datetime
import lightgbm as lgb
from dotenv import load_dotenv
import os
import s3fs
import tempfile

load_dotenv()
fs = s3fs.S3FileSystem()

### Local Dev
# root = Path(__file__).resolve().parents[2]
# artifacts = root / "artifacts" / "p_out"

### AWS Dev
DATA_DIR = os.getenv("DATA_DIR").rstrip("/")
artifacts = f"{DATA_DIR}/artifacts/p_out"

def save_model(start_date, end_date):
    df = get_data(start_date, end_date, engine)

    train_data, test_data = preprocess_data(df)

    p_out = train_p_out(train_data,test_data)

    date_folder = f"{artifacts}/{datetime.now().strftime('%Y-%m-%d')}"
    model_path = f"{date_folder}/model.txt"
    
    ### Local Dev
    # Path(date_folder).mkdir(exist_ok=True)
    # p_out.save_model(str(model_path))
    ### AWS Dev
    with tempfile.NamedTemporaryFile() as tmp:
        p_out.save_model(tmp.name)
        fs.put(tmp.name, model_path)

    return model_path

def get_model(training_date=None):
    if training_date is not None:
        model_file = f"{artifacts}/{training_date}/model.txt"
        if not fs.exists(model_file):
            raise Exception(f"No model found at {model_file}")
    else:
        ### Local Dev
        # training_dates = [(datetime.strptime(f.name,"%Y-%m-%d"),f / "model.txt") for f in artifacts.iterdir() if f.is_dir()]
        
        ### AWS Dev
        dirs = fs.ls(artifacts,detail=True)
        training_dates = []
        for d in dirs:
            if d["name"].endswith("/"):
                dir_name = d["name"].rstrip("/").split("/")[-1]
                try:
                    date = datetime.strptime(dir_name, "%Y-%m-%d")
                    model_path = f"{artifacts}/{dir_name}/model.txt"
                    training_dates.append((date,model_path))
                except ValueError:
                    continue
                    
        if len(training_dates)==0:
            raise Exception(f"No models found")
        model_file = max(training_dates, key=lambda x:x[0])[1]
   
    ### Local Dev
    # p_out = lgb.Booster(model_file=model_file)

    ### AWS Dev
    with fs.open(model_file, "r") as f:
        model_str = f.read()
    p_out = lgb.Booster(model_str=model_str)
    
    return p_out
