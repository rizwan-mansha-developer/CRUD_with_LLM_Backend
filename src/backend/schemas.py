from pydantic import BaseModel
from datetime import date
from typing import Optional

class ExpenseBase(BaseModel):
    amount: float
    category: str
    date: date

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseRead(ExpenseBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    class Config:
        from_attributes = True
