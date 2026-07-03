from pydantic import BaseModel

class PaymentRequest(BaseModel):
    sender_id: int
    receiver_id: int
    merchant_id: int
    amount: float
    location: str