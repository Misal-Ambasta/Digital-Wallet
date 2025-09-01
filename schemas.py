from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    phone_number: str
    balance: float = 0.0


class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone_number: Optional[str]


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    password: str
    phone_number: str
    created_at: datetime
    model_config=ConfigDict(from_attributes=True)

class TrasactionBase(BaseModel):
    user_id: int
    transaction_type: str
    amount: float
    description: str

class TransactionCreate(TrasactionBase):
    pass

class TransactionResponse(BaseModel):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True