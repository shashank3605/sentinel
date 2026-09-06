import joblib
import pandas as pd

model = joblib.load("models/fraud_model.joblib")
feature_columns = joblib.load("models/feature_columns.joblib")

FRAUD_THRESHOLD = 0.99


def score_with_model(event) -> tuple[float, bool]:
    """
    Runs the transaction through the trained XGBoost model.
    Returns (fraud_probability, is_fraud_flagged).

    Note: this uses placeholder zeros for balance fields, since Sentinel's
    live API doesn't have access to a bank's real account balance data —
    that's an external integration point for a real deployment, out of
    scope for this portfolio project. This is an explicit, documented
    simplification, not an oversight.
    """
    row = {col: 0 for col in feature_columns}  # start every column at 0

    row["amount"] = event.amount
    row["step"] = 1  # placeholder; real deployment would use actual time-based step

    type_column = f"type_{event.channel}"
    if type_column in row:
        row[type_column] = 1

    X = pd.DataFrame([row])[feature_columns]  # enforce exact training column order

    fraud_probability = model.predict_proba(X)[0][1]
    is_fraud_flagged = fraud_probability >= FRAUD_THRESHOLD

    return fraud_probability, is_fraud_flagged