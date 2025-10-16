import lightgbm as lgb
from sklearn.model_selection import train_test_split
import pandas as pd

def preprocess_data(df):
    features = ["launch_angle","launch_speed","total_distance","hit_location","first_base_runner", "second_base_runner", "third_base_runner", "num_outs"]
    target = "has_score"

    X = df[features].copy()
    y = df[target]

    for col in ["first_base_runner","second_base_runner","third_base_runner"]:
        X[col] = X[col].astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)

    train_data = lgb.Dataset(X_train, label=y_train, categorical_feature=["hit_location","num_outs"])
    test_data = lgb.Dataset(X_test, label=y_test, categorical_feature=["hit_location","num_outs"])

    return train_data, test_data

def get_data(start_date, end_date, engine):
    query = f"SELECT * FROM fieldable_plays f INNER JOIN game_catalog g ON f.gamepk = g.gamepk WHERE g.status = 'PROCESSED' AND g.game_date BETWEEN CAST('{start_date}' AS date) AND CAST('{end_date}' AS date)"
    df = pd.read_sql(query, engine)

    return df
