from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped
from database import Base
from datetime import datetime
from sqlalchemy.sql import func



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15))
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())

    transactions = relationship("Transaction", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    recipient_user_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="transactions")