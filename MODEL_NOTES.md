# Sentinel — Model Notes

## Phase 1 — Scoring model selection

**Dataset:** PaySim synthetic mobile-money transactions (Kaggle: rupakroy/online-payments-fraud-detection-dataset)
6,362,620 transactions, 8,213 fraud (0.13%) — severely imbalanced, structurally representative of UPI/IMPS-style P2P transfers rather than real UPI data (no public real UPI fraud dataset exists due to privacy/regulatory restrictions).

**Features used:** step, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, one-hot encoded transaction type (CASH_IN/CASH_OUT/DEBIT/PAYMENT/TRANSFER)
**Dropped:** nameOrig, nameDest (unique identifiers, no generalizable signal), isFlaggedFraud (a different pre-existing rule in the dataset — including it would leak label information)

**Models compared, both trained on identical 80/20 stratified split:**

| Model               | Class imbalance handling | Best threshold | Precision | Recall | F1    |
| ------------------- | ------------------------ | -------------- | --------- | ------ | ----- |
| Logistic Regression | class_weight="balanced"  | 0.99           | 0.266     | 0.635  | 0.375 |
| XGBoost             | scale_pos_weight=773.75  | 0.99           | 0.926     | 0.893  | 0.909 |

**PR-AUC (XGBoost): 0.9662**

**Decision: XGBoost, threshold = 0.99**

Logistic regression's precision ceiling remained low (26.6% even at its most conservative threshold) — its linear decision boundary couldn't capture the non-linear interactions in the data (e.g. transaction type combined with near-total balance depletion). XGBoost resolved this directly on identical data/split, confirming the hypothesis rather than assuming it.

Threshold 0.99 chosen because F1 increases monotonically from 0.90→0.99 with no trade-off dip in between — at 0.99 we get the best precision (92.6%) and best F1 (0.909) in the sweep, while still catching 89.3% of fraud. Since Sentinel's design routes flagged transactions to a human review queue (not auto-block), minimizing false-alarm noise for analysts was prioritized over maximizing raw recall.

This threshold is a config value, not hardcoded logic — adjustable without retraining if a client's risk tolerance differs.
