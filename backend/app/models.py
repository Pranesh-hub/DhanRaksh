from sqlalchemy import Column, Integer, Float, String
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    amount = Column(Float)
    status = Column(String)