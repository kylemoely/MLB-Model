import lightgbm as lgb
from sklearn.model_selection import train_test_split

def preprocess_data(df):
    features = ["launch_angle","launch_speed","total_distance","location","first_base_runner", "second_base_runner", "third_base_runner"]
    target = "out"

    X = df[features]
    y = df[target]

    for col in ["first_base_runner","second_base_runner","third_base_runner"]:
        X[col] = X[col].astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)

    train_data = lgb.Dataset(X_train, label=y_train, categorical_feature=["location"])
    test_data = lgb.Dataset(X_test, label=y_test, categorical_feature=["location"])

    return train_data, test_data