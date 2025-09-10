from sklearn.metrics import roc_auc_score, brier_score_loss, log_loss, accuracy_score

def evaluate_p_out(p_out, X, y):
    y_pred_proba_outs = p_out.predict(X, num_iteration=p_out.best_iteration)

    p_out_auc = roc_auc_score(y, y_pred_proba_outs)
    p_out_brier = brier_score_loss(y, y_pred_proba_outs)
    p_out_logloss = log_loss(y, y_pred_proba_outs)
    p_out_accuracy = accuracy_score(y, (y_pred_proba_outs>=0.5).astype(int))

    print(f"AUC: {p_out_auc:.3f}, Brier: {p_out_brier:.3f}, LogLoss: {p_out_logloss:.3f}, Accuracy: {p_out_accuracy}")