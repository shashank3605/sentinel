from fastapi import FastAPI
from app.models import TransactionEvent, ScoreResponse
from app.feature_store import record_transaction

app= FastAPI(title="Sentinel Fraud Scoring API", version="0.0.1")

VELOCITY_LIMIT = 5  #maximum transaction per 60 sec

@app.get("/health")
def health():
    """Basic liveness check"""
    return {"status": "ok"}

@app.post("/score", response_model=ScoreResponse)
def score_transaction(event:TransactionEvent) -> ScoreResponse:
    # """
    # Phase 0 stub: no rules, no ML yet. Just proves the ingestion contract
    # works end-to-end — payload in, validated, decision out.
    # """
    # if event.amount > 100000:
    #     decision= "flag"
    #     reason= "amount_exceeds_threshold"
    # else:
    #     decision= "allow"
    #     reason= "no_rules_triggered"
    
    # return ScoreResponse(
    #     transaction_id=event.transaction_id,
    #     decision=decision,
    #     risk_score=0.0,
    #     reason=reason,
    # )
    """
    Phase 1: rules now include a real velocity check backed by Redis,
    in addition to the amount threshold from Phase 0.
    """

    txn_count= record_transaction(event.user_id)

    if txn_count > VELOCITY_LIMIT:
        decision = "flag"
        reason= "velocity_limit_exceeded"
    elif event.amount > 100000:
        decision= "flag"
        reason= "amount_exceeds_threshold"
    else:
        decision= "allow"
        reason= "no_rules_triggered"

    return ScoreResponse(
        transaction_id=event.transaction_id,
        decision=decision,
        risk_score=0.0,
        reason=reason,
    )
