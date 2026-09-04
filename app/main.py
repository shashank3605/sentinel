from fastapi import FastAPI
from app.models import TransactionEvent, ScoreResponse

app= FastAPI(title="Sentinel Fraud Scoring API", version="0.0.1")

@app.get("/health")
def health():
    """Basic liveness check"""
    return {"status": "ok"}

@app.post("/score", response_model=ScoreResponse)
def score_transaction(event:TransactionEvent) -> ScoreResponse:
    """
    Phase 0 stub: no rules, no ML yet. Just proves the ingestion contract
    works end-to-end — payload in, validated, decision out.
    """
    if event.amount > 100000:
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