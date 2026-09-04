from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TransactionEvent(BaseModel):
    """
    A single transaction/login/payment event submitted to Sentinel for scoring.
    """
    transaction_id: str = Field(..., description="Unique Id for this tracsaction.")
    user_id: str = Field(..., description="Id of the user/account initiating the traansaction.")
    amount: float = Field(..., gt=0, description="Transaction amount, must be positive.")
    currency: str = Field(..., description="ISO currency code")
    timestamp: datetime = Field(..., description="When the transaction occurred")
    channel:str = Field(..., description="Payment rail, e.g. UPI, IMPS, card")
    merchant_id: Optional[str] = Field(default=None, description="Merchant ID, if applicable")
    device_id: Optional[str] = Field(default=None, description="Device fingerprint, if available")


class ScoreResponse(BaseModel):
    """What Sentinel returns after scoring a transaction."""
    transaction_id:str
    decision:str
    risk_score:float
    reason:str