from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, db

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=schemas.ExpenseRead)
def create_expense(expense: schemas.ExpenseCreate, user_id: int, db_: Session = Depends(db.get_db)):
    try:
        new_expense = models.Expense(**expense.model_dump(), user_id=user_id)
        db_.add(new_expense)
        db_.commit()
        db_.refresh(new_expense)
        return new_expense
    except Exception as e:
        db_.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating expense: {str(e)}")

@router.get("/{user_id}", response_model=list[schemas.ExpenseRead])
def get_expenses(user_id: int, db_: Session = Depends(db.get_db)):
    try:
        return db_.query(models.Expense).filter(models.Expense.user_id == user_id).all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching expenses: {str(e)}")
