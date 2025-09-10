import lightgbm as lgb

def train_p_out(train_data, test_data):
    params = {
        "objective": "binary",
        "metric": ["binary_logloss", "auc"],
        "boosting_type": "gbdt",
        "num_leaves": 31,
        "learning_rate": 0.05,
        "feature_fraction": 0.9,
        "bagging_fraction": 0.8,
        "bagging_freq": 5,
        "verbose": -1
    }

    p_out = lgb.train(
        params,
        train_data,
        valid_sets=[train_data, test_data],
        num_boost_round=1000
    )