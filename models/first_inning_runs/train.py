import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

def train_model():
    features_df = pd.read_excel("C:/Users/Kyle/Desktop/Projects/MLB Stats/df_features.xlsx")
    labels_df = pd.read_excel("C:/Users/Kyle/Desktop/Projects/MLB Stats/df_labels.xlsx")

    df = features_df.merge(labels_df, on="gamepk", how="inner").copy()
    df['label'] = df['label'].astype(int)
    def row_to_sequence(row):
        away_matchups = [[row[f"away_batter{i}_ops"],row[f"away_batter{i}_avg"],row["home_pitcher_era"],row["home_pitcher_whip"]] for i in range(1,6)]
        home_matchups = [[row[f"away_batter{i}_ops"],row[f"away_batter{i}_avg"],row["home_pitcher_era"],row["home_pitcher_whip"]] for i in range(1,6)]
        return np.array(away_matchups + home_matchups, dtype=float) 
        
    X = df.drop(columns=["Unnamed: 0_x","gamepk","Unnamed: 0_y","label"])
    X = X.fillna(X.median(numeric_only=True))
    X_seq = np.stack(X.apply(row_to_sequence, axis=1).values)
    y = df['label'].values

    X_tr, X_te, y_tr, y_te = train_test_split(X_seq, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_tr_2d = X_tr.reshape(-1, X_tr.shape[-1])
    X_te_2d = X_te.reshape(-1, X_te.shape[-1])

    X_tr_2d = scaler.fit_transform(X_tr_2d)
    X_te_2d = scaler.transform(X_te_2d)

    X_tr = X_tr_2d.reshape(X_tr.shape)
    X_te = X_te_2d.reshape(X_te.shape)

    tf.random.set_seed(42)

    model = models.Sequential([
        layers.Input(shape=(10, 4)),
        layers.GRU(32, return_sequences=False),
        layers.Dropout(0.3),
        layers.Dense(16, activation="relu"),
        layers.Dense(1, activation="sigmoid")
    ])

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy", tf.keras.metrics.AUC(name="auc")]
    )

    history = model.fit(
        X_tr, y_tr,
        validation_split=0.2,
        epochs=25,
        batch_size=64,
        verbose=1
    )

if __name__ == "__main__":
    train_model()