from sklearn.metrics import roc_auc_score, brier_score_loss, log_loss, accuracy_score

def evaluate_p_run(p_run, X, y):
    y_pred_proba_outs = p_run.predict(X, num_iteration=p_run.best_iteration)

    p_run_auc = roc_auc_score(y, y_pred_proba_outs)
    p_run_brier = brier_score_loss(y, y_pred_proba_outs)
    p_run_logloss = log_loss(y, y_pred_proba_outs)
    p_run_accuracy = accuracy_score(y, (y_pred_proba_outs>=0.5).astype(int))

    print(f"AUC: {p_run_auc:.3f}, Brier: {p_run_brier:.3f}, LogLoss: {p_run_logloss:.3f}, Accuracy: {p_run_accuracy}")