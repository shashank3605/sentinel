# import pandas as pd

# df = pd.read_csv("data/PS_20174392719_1491204439457_log.csv")

# # Drop leakage/identifier columns
# df = df.drop(columns=["nameOrig", "nameDest", "isFlaggedFraud"])

# # One-hot encode the 'type' column
# df = pd.get_dummies(df, columns=["type"], drop_first=False)

# print("Columns after encoding:")
# print(df.columns.tolist())
# print()
# print("Shape after prep:", df.shape)
# print()
# print(df.head())


# Logistic regression
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import classification_report, confusion_matrix

# df = pd.read_csv("data/PS_20174392719_1491204439457_log.csv")

# df = df.drop(columns=["nameOrig", "nameDest", "isFlaggedFraud"])
# df = pd.get_dummies(df, columns=["type"], drop_first=False)

# # Separate features (X) from the target label (y)
# X = df.drop(columns=["isFraud"])
# y = df["isFraud"]

# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42, stratify=y
# )

# print("Train size:", X_train.shape)
# print("Test size:", X_test.shape)

# model = LogisticRegression(class_weight="balanced", max_iter=1000)
# model.fit(X_train, y_train)

# y_pred = model.predict(X_test)

# print()
# print("Confusion matrix:")
# print(confusion_matrix(y_test, y_pred))
# print()
# print("Classification report:")
# print(classification_report(y_test, y_pred))


# logistic regression with threshold

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("data/PS_20174392719_1491204439457_log.csv")

df = df.drop(columns=["nameOrig", "nameDest", "isFlaggedFraud"])
df = pd.get_dummies(df, columns=["type"], drop_first=False)

# Separate features (X) from the target label (y)
X = df.drop(columns=["isFraud"])
y = df["isFraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)

model = LogisticRegression(class_weight="balanced", max_iter=1000)
model.fit(X_train, y_train)

# Get fraud probabilities instead of hard yes/no labels
y_proba = model.predict_proba(X_test)[:, 1]  # probability of class "1" (fraud)

print()
print("Threshold sweep — precision/recall/f1 for the FRAUD class only:")
print(f"{'Threshold':<10} {'Precision':<10} {'Recall':<10} {'F1':<10} {'Flagged':<10}")

for threshold in [0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.99]:
    y_pred_at_threshold = (y_proba >= threshold).astype(int)

    report = classification_report(
        y_test, y_pred_at_threshold, output_dict=True, zero_division=0
    )
    fraud_metrics = report["1"]
    flagged_count = y_pred_at_threshold.sum()

    print(f"{threshold:<10} {fraud_metrics['precision']:<10.3f} {fraud_metrics['recall']:<10.3f} {fraud_metrics['f1-score']:<10.3f} {flagged_count:<10}")


#  for xgboost
from xgboost import XGBClassifier

print()
print("=" * 60)
print("XGBoost")
print("=" * 60)

# scale_pos_weight is XGBoost's equivalent of class_weight="balanced" —
# it tells the model how much more to "care" about the rare fraud class.
# Standard formula: (count of negative class) / (count of positive class)
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
print("scale_pos_weight:", scale_pos_weight)

xgb_model = XGBClassifier(
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    random_state=42,
)
xgb_model.fit(X_train, y_train)

y_proba_xgb = xgb_model.predict_proba(X_test)[:, 1]

print()
print("Threshold sweep — precision/recall/f1 for the FRAUD class only:")
print(f"{'Threshold':<10} {'Precision':<10} {'Recall':<10} {'F1':<10} {'Flagged':<10}")

for threshold in [0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.99]:
    y_pred_at_threshold = (y_proba_xgb >= threshold).astype(int)

    report = classification_report(
        y_test, y_pred_at_threshold, output_dict=True, zero_division=0
    )
    fraud_metrics = report["1"]
    flagged_count = y_pred_at_threshold.sum()

    print(f"{threshold:<10} {fraud_metrics['precision']:<10.3f} {fraud_metrics['recall']:<10.3f} {fraud_metrics['f1-score']:<10.3f} {flagged_count:<10}")


# PR-AUC (Precision-Recall Area Under Curve)

from sklearn.metrics import average_precision_score

pr_auc = average_precision_score(y_test, y_proba_xgb)
print()
print(f"PR-AUC (XGBoost): {pr_auc:.4f}")

print()
print("Fine-grained sweep between 0.90 and 0.99:")
print(f"{'Threshold':<10} {'Precision':<10} {'Recall':<10} {'F1':<10} {'Flagged':<10}")

for threshold in [0.90, 0.92, 0.94, 0.96, 0.97, 0.98, 0.99]:
    y_pred_at_threshold = (y_proba_xgb >= threshold).astype(int)
    report = classification_report(
        y_test, y_pred_at_threshold, output_dict=True, zero_division=0
    )
    fraud_metrics = report["1"]
    flagged_count = y_pred_at_threshold.sum()
    print(f"{threshold:<10} {fraud_metrics['precision']:<10.3f} {fraud_metrics['recall']:<10.3f} {fraud_metrics['f1-score']:<10.3f} {flagged_count:<10}")


import joblib
import os

os.makedirs("models", exist_ok=True)
joblib.dump(xgb_model, "models/fraud_model.joblib")
print()
print("Model saved to models/fraud_model.joblib")

# Save the exact column order too — critical detail explained below
joblib.dump(X_train.columns.tolist(), "models/feature_columns.joblib")
print("Feature column order saved to models/feature_columns.joblib")