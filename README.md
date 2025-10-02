# MLB-Model ⚾  
*A machine learning pipeline for predicting first-inning runs in Major League Baseball games.*

---

## 📖 Overview  

This project is an end-to-end machine learning system designed to predict **first inning runs (FIR)** in Major League Baseball (MLB) games. While FIR is the primary target, the architecture is built to scale to other prediction tasks across the sport.  

The project demonstrates:
- Full **data engineering** lifecycle: ingestion, transformation, storage, validation  
- Modular **feature engineering** and **label generation** strategies for sports analytics  
- Application of advanced **machine learning methods** with temporal cross-validation  
- A production-ready pipeline structure that could be deployed for daily predictions  

The work highlights not only predictive modeling but also the **engineering rigor** required to support reproducible, maintainable, and scalable data science in a real-world setting.  

---

## 📂 Repository Structure  

MLB-Model/
├── calculate/ # Custom baseball metrics (ERA, WHIP, OAA, etc.)
├── db/ # Database connection helpers & SQL schema utilities
├── etl/ # ETL workflows for ingesting and cleaning raw MLB data
├── models/ # Training, saving, loading, and calibration of ML models
├── pipelines/ # Orchestrated workflows for training, scoring, and backtesting
├── utils/ # Logging, configuration, validation, and shared utilities
├── get_2021-2024.py # Multi-season ingestion example
├── get_2023_2024_features.py # Feature set construction
├── get_2023_2024_labels.py # Label construction for targets
└── README.md


This structure separates concerns between **data, modeling, and orchestration**, following modern data engineering best practices.  

---

## 📊 Problem Definition  

The central predictive task is:  
**"Will a run be scored in the first inning of a given game?"**  

This task is:
- **Highly imbalanced** (majority class = no run)  
- **Time-sensitive** (data must reflect only pre-game information)  
- **Dynamic** (player performance, team lineups, and contextual factors shift throughout the season)  

By solving FIR prediction, the system establishes a foundation for expanding into additional game-level or player-level outcomes.  

---

## 🏗️ System Architecture  

The project is built around a clear, modular workflow:  

1. **ETL (Extract, Transform, Load)**  
   - Ingest historical play-by-play, game, and player data  
   - Normalize and validate for downstream modeling  

2. **Feature Engineering**  
   - Pitcher and batter performance metrics  
   - Rolling-window stats (recent form, fatigue, rest days)  
   - Contextual features (ballpark factors, weather, umpire tendencies, future integration)  

3. **Label Generation**  
   - Aligns game-level outcomes with engineered features  
   - Supports FIR (binary) and is extendable to regression or multi-class targets  

4. **Modeling & Training**  
   - Gradient boosted decision trees (XGBoost/LightGBM)  
   - Temporal cross-validation to prevent data leakage  
   - Probability calibration for reliable predicted probabilities  

5. **Evaluation**  
   - AUC, Precision/Recall, F1-score  
   - Brier score and calibration curves  
   - Backtesting across multiple seasons (2021–2024)  

6. **Pipelines & Orchestration**  
   - Daily scoring pipelines  
   - Backtest pipelines for historical evaluation  
   - Artifacts (models, metrics, feature sets) stored reproducibly  

---

## 📦 Artifacts  

The system produces reproducible outputs:  
- **Models**: Serialized with feature schema for future inference  
- **Features**: Versioned parquet datasets for transparency  
- **Logs**: Detailed logs for traceability and debugging  
- **Metrics**: Stored and tracked per experiment  

---

## 📈 Key Technical Highlights  

- **Temporal Cross-Validation**: Rolling origin splits ensure fairness and robustness in evaluation.  
- **Class Imbalance Handling**: Re-weighted loss functions and calibrated thresholds improve FIR predictions.  
- **Feature Stability**: Consistent schema enforcement and validation checks prevent drift.  
- **Reproducibility**: Modular structure ensures any season or dataset can be re-ingested and modeled with consistent results.  
- **Extensibility**: Designed to evolve into predicting other baseball outcomes (player performance, win probabilities, in-game scoring events).  

---

## 🛠️ Roadmap  

- Expand **feature set** with real-time data feeds (weather, betting odds, line movements).  
- Add **experiment tracking** (MLflow, Weights & Biases) for parameter sweeps and reproducibility.  
- Build **API service** (FastAPI) for serving predictions in real time.  
- Explore **deep learning architectures** (RNNs, Transformers) for sequence-aware modeling of games.  
- Integrate **model monitoring** for drift detection during live deployment.  

---

## 📜 License  

MIT License © 2025 Kyle Moellenkamp  
