from sqlalchemy import Column, Integer, Float, String
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    amount = Column(Float)
    status = Column(String)

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