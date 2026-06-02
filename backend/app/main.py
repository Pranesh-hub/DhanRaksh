from fastapi import FastAPI
from .models import Transaction, LedgerEvent
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

@app.get("/transactions")
def get_transactions(
    db: Session = Depends(get_db)
):
    return db.query(Transaction).all()

@app.get("/ledger")
def get_ledger(
    db: Session = Depends(get_db)
):
    return db.query(LedgerEvent).all()

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

    debit_event = LedgerEvent(
        transaction_id=txn.id,
        user_id=payment.sender_id,
        event_type="DEBIT",
        amount=payment.amount
    )

    credit_event = LedgerEvent(
        transaction_id=txn.id,
        user_id=payment.receiver_id,
        event_type="CREDIT",
        amount=payment.amount
    )

    db.add(debit_event)
    db.add(credit_event)

    db.commit()

    return {
        "transaction_id": txn.id,
        "status": txn.status
    }