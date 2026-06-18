from fastapi import FastAPI
from .models import Transaction, LedgerEvent
from .database import engine
from .models import Base

from fastapi import Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import Transaction
from .models import LedgerEvent
from .models import User
from .schemas import PaymentRequest
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    sender = db.query(User).filter(
        User.id == payment.sender_id
    ).first()

    receiver = db.query(User).filter(
        User.id == payment.receiver_id
    ).first()

    if sender is None:
        raise HTTPException(
            status_code=404,
            detail="Sender not found"
        )

    if receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver not found"
        )

    if sender.id == receiver.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot pay yourself"
        )

    if sender.balance < payment.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    # update balances
    sender.balance -= payment.amount
    receiver.balance += payment.amount

    txn = Transaction(
        sender_id=payment.sender_id,
        receiver_id=payment.receiver_id,
        amount=payment.amount,
        status="SUCCESS"
    )

    db.add(txn)
    db.commit()
    db.refresh(txn)

    # ledger creation code here

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

@app.get("/seed-users")
def seed_users(db: Session = Depends(get_db)):

    users = [
        User(id=1, name="Alice", balance=10000),
        User(id=2, name="Bob", balance=5000),
        User(id=3, name="Charlie", balance=8000),
        User(id=4, name="David", balance=7000),
        User(id=5, name="Emma", balance=12000),
    ]

    for user in users:
        db.add(user)

    db.commit()

    return {"message": "Users seeded"}

@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()