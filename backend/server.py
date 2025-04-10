from fastapi import FastAPI, HTTPException, Depends
from datetime import date
from typing import List
from pydantic import BaseModel
from logging_setup import setup_logger
import db_helper

logger = setup_logger("FastAPI")

app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

class ExpenseAnalytics(BaseModel):
    category: str
    total: float
    percentage: float

@app.on_event("startup")
def startup_event():
    logger.info("FastAPI server is starting...")

@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    try:
        expenses = db_helper.fetch_expenses_for_date(expense_date)
        if not expenses:
            raise HTTPException(status_code=404, detail="No expenses found for this date")
        return expenses
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    try:
        db_helper.delete_expenses_for_date(expense_date)
        for expense in expenses:
            db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
        return {"message": "Expenses updated successfully"}
    except Exception as e:
        logger.error(f"Error updating expenses: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating expenses: {str(e)}")

@app.post("/analytics/", response_model=List[ExpenseAnalytics])
def get_analytics(date_range: DateRange):
    logger.info(f"Fetching analytics for range: {date_range.start_date} - {date_range.end_date}")
    try:
        data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
        if not data:
            raise HTTPException(status_code=404, detail="No data available for the given date range")
        total = sum(row["total"] for row in data)
        breakdown = [
            ExpenseAnalytics(
                category=row["category"],
                total=row["total"],
                percentage=(row["total"] / total) * 100 if total != 0 else 0
            ) for row in data
        ]
        return breakdown
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
