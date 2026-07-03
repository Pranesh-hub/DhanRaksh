from datetime import timedelta
from datetime import datetime
from collections import Counter

from fastapi import FastAPI

from .kafka_producer import publish_payment
from .models import Transaction, LedgerEvent
from .database import engine
from .models import Base

from fastapi import Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import Transaction
from .models import LedgerEvent
from .models import User
from .models import Merchant
from .schemas import PaymentRequest
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .fraud_engine import calculate_fraud, risk_level

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
    
    merchant = db.query(Merchant).filter(
        Merchant.id == payment.merchant_id
    ).first()

    if merchant is None:
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

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

    now = datetime.utcnow()

    one_minute_ago = now - timedelta(minutes=1)
    five_minutes_ago = now - timedelta(minutes=5)
    one_hour_ago = now - timedelta(hours=1)

    count_1m = db.query(Transaction).filter(
        Transaction.sender_id == payment.sender_id,
        Transaction.timestamp >= one_minute_ago
    ).count()

    count_5m = db.query(Transaction).filter(
        Transaction.sender_id == payment.sender_id,
        Transaction.timestamp >= five_minutes_ago
    ).count()

    count_1h = db.query(Transaction).filter(
        Transaction.sender_id == payment.sender_id,
        Transaction.timestamp >= one_hour_ago
    ).count()

    # Base fraud checks
    score, reasons = calculate_fraud(
        payment.amount,
        merchant,
        payment.location,
        count_1m,
        count_5m,
        count_1h
    )

    # Transaction history
    past_transactions = db.query(Transaction).filter(
        Transaction.sender_id == payment.sender_id
    ).all()

    # ---------------------------
    # Merchant Category Anomaly
    # ---------------------------

    categories = []

    for txn in past_transactions:

        old_merchant = db.query(Merchant).filter(
            Merchant.id == txn.merchant_id
        ).first()

        if old_merchant:
            categories.append(
                old_merchant.category
            )

    if len(categories) >= 5:

        dominant_category = Counter(
            categories
        ).most_common(1)[0][0]

        if dominant_category != merchant.category:

            score += 15

            reasons.append(
                "Merchant Category Anomaly"
            )

    # ---------------------------
    # Location Anomaly
    # ---------------------------

    last_transaction = db.query(Transaction).filter(
        Transaction.sender_id == payment.sender_id
    ).order_by(
        Transaction.timestamp.desc()
    ).first()

    if (
        last_transaction
        and
        len(past_transactions) >= 3
    ):

        previous_location = (
            last_transaction.location
        )

        if (
            previous_location
            and
            previous_location != payment.location
        ):

            score += 20

            reasons.append(
                "Location Anomaly"
            )

    # ---------------------------
    # Self-learning Merchant Risk
    # ---------------------------

    merchant.total_txn_count += 1

    if score >= 50:
        merchant.fraud_txn_count += 1

    merchant.risk_score = (
        100 *
        merchant.fraud_txn_count
        /
        merchant.total_txn_count
    )

    txn = Transaction(
        sender_id=payment.sender_id,
        receiver_id=payment.receiver_id,
        amount=payment.amount,
        fraud_score=score,
        fraud_reasons=", ".join(reasons),
        risk_level=risk_level(score),
        status="SUCCESS",
        location=payment.location,
        merchant_id=payment.merchant_id
    )

    db.add(txn)
    db.commit()
    event = {
        "sender_id":
            payment.sender_id,

        "receiver_id":
            payment.receiver_id,

        "merchant_id":
            payment.merchant_id,

        "amount":
            payment.amount,

        "location":
            payment.location
    }
    publish_payment(event)
    # db.refresh(txn)

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

@app.get("/seed-merchants")
def seed_merchants(db: Session = Depends(get_db)):
    merchants = [
        Merchant(id=1, name="Amazon", category="Electronics", risk_score=10),
        Merchant(id=2, name="Swiggy", category="Food", risk_score=5),
        Merchant(id=3, name="Uber", category="Transport", risk_score=15),
        Merchant(id=4, name="UnknownStore", category="Retail", risk_score=75)
    ]

    for merchant in merchants:
        db.add(merchant)

    db.commit()

    return {"message": "Merchants seeded"}

@app.get("/merchants")
def get_merchants(
    db: Session = Depends(get_db)
):
    return db.query(Merchant).all()

@app.get("/fraud-transactions")
def get_fraud_transactions(
    db: Session = Depends(get_db)
):
    return db.query(Transaction).filter(Transaction.fraud_score >0).all()

@app.get("/fraud-summary")
def fraud_summary(
    db: Session = Depends(get_db)
):

    transactions = db.query(Transaction).all()

    total_transactions = len(transactions)

    suspicious_transactions = len([
        t for t in transactions
        if t.fraud_score > 0
    ])

    critical_transactions = len([
        t for t in transactions
        if t.risk_level == "CRITICAL"
    ])

    avg_fraud_score = 0

    if total_transactions > 0:
        avg_fraud_score = (
            sum(
                t.fraud_score
                for t in transactions
            )
            /
            total_transactions
        )

    return {
        "total_transactions":
            total_transactions,

        "suspicious_transactions":
            suspicious_transactions,

        "critical_transactions":
            critical_transactions,

        "avg_fraud_score":
            round(avg_fraud_score, 2)
    }

@app.get("/top-risky-merchants")
def top_risky_merchants(
    db: Session = Depends(get_db)
):

    return (
        db.query(Merchant)
        .order_by(
            Merchant.risk_score.desc()
        )
        .limit(5)
        .all()
    )

@app.get("/top-risky-users")
def top_risky_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    result = []

    for user in users:

        txns = db.query(Transaction).filter(
            Transaction.sender_id == user.id
        ).all()

        risk = sum(
            t.fraud_score
            for t in txns
        )

        result.append({
            "user_id": user.id,
            "name": user.name,
            "risk_score": risk
        })

    result.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    return result[:5]

