from sqlalchemy import Column, Integer, Float, String, DateTime
from .database import Base
from datetime import datetime, timedelta

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    sender_id = Column(Integer)

    receiver_id = Column(Integer)

    amount = Column(Float)

    status = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow().replace(tzinfo=None) + timedelta(hours=5, minutes=30))

    merchant_id = Column(Integer)

    location = Column(String)

    fraud_score = Column(Float, default=0)

    fraud_reasons = Column(String, default="")

    risk_level = Column(String, default="LOW")

class LedgerEvent(Base):
    __tablename__ = "ledger_events"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(Integer)

    user_id = Column(Integer)

    event_type = Column(String)

    amount = Column(Float)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Float)

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    category = Column(String)

    risk_score = Column(Float, default=0)

    fraud_txn_count = Column(Integer, default=0)

    total_txn_count = Column(Integer, default=0)