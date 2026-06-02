from fastapi import FastAPI

from .database import engine
from .models import Base

from fastapi import Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import Transaction
from .schemas import PaymentRequest

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "PayShield Running"}

@app.post("/payment")
def make_payment(
    payment: PaymentRequest,
    db: Session = Depends(get_db)
):
    txn = Transaction(
        sender_id=payment.sender_id,
        receiver_id=payment.receiver_id,
        amount=payment.amount,
        status="SUCCESS"
    )

    db.add(txn)
    db.commit()
    db.refresh(txn)

    return {
        "transaction_id": txn.id,
        "status": txn.status
    }