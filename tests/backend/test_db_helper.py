import pytest
from backend import db_helper

def setup_module(module):
    """Setup test data before running tests."""
    db_helper.insert_expense("2024-08-15", 10.0, "Shopping", "Test expense")
    db_helper.insert_expense("2024-08-15", 20.0, "Food", "Lunch")

def teardown_module(module):
    """Clean up test data after tests run."""
    db_helper.delete_expenses_for_date("2024-08-15")

def test_fetch_expenses_for_date():
    expenses = db_helper.fetch_expenses_for_date("2024-08-15")
    assert len(expenses) == 2
    assert any(expense["amount"] == 10.0 and expense["category"] == "Shopping" for expense in expenses)
    assert any(expense["amount"] == 20.0 and expense["category"] == "Food" for expense in expenses)

def test_fetch_expenses_for_invalid_date():
    expenses = db_helper.fetch_expenses_for_date("2026-08-15")
    assert expenses == []

def test_insert_and_delete_expense():
    db_helper.insert_expense("2024-08-16", 15.0, "Entertainment", "Movie")
    expenses = db_helper.fetch_expenses_for_date("2024-08-16")
    assert len(expenses) == 1
    assert expenses[0]["amount"] == 15.0
    assert expenses[0]["category"] == "Entertainment"
    
    db_helper.delete_expenses_for_date("2024-08-16")
    expenses = db_helper.fetch_expenses_for_date("2024-08-16")
    assert expenses == []

def test_fetch_expense_summary():
    summary = db_helper.fetch_expense_summary("2024-08-01", "2024-08-31")
    assert isinstance(summary, list)
    assert len(summary) > 0