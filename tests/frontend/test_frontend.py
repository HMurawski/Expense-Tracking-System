import pytest
import requests
from unittest.mock import patch
import streamlit as st
from frontend.add_update_ui import add_update_tab
from frontend.analyze_by_category import analyze_by_category_tab
from frontend.analyze_by_month import analyze_by_month_tab


def test_fetch_expenses_success():
    mock_response = [
        {"amount": 20.0, "category": "Food", "notes": "Lunch"},
        {"amount": 15.0, "category": "Entertainment", "notes": "Movie"}
    ]
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        with st.container():
            add_update_tab()
        
        assert st._main._current_form is not None

def test_fetch_expenses_failure():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {"detail": "Server error"}
        
        with st.container():
            add_update_tab()
        
        assert "Failed to retrieve expenses" in st._main._messages

def test_analyze_by_category_success():
    mock_response = [
        {"category": "Food", "total": 50.0, "percentage": 50.0},
        {"category": "Shopping", "total": 50.0, "percentage": 50.0}
    ]
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response
        
        with st.container():
            analyze_by_category_tab()
        
        assert "Expense Breakdown" in st._main._titles

def test_analyze_by_category_failure():
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 500
        
        with st.container():
            analyze_by_category_tab()
        
        assert "Failed to retrieve analytics data." in st._main._messages

def test_analyze_by_month_success():
    mock_response = [
        {"category": "Rent", "total": 500.0},
        {"category": "Utilities", "total": 100.0}
    ]
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response
        
        with st.container():
            analyze_by_month_tab()
        
        assert "Monthly Expense Analysis" in st._main._titles

def test_analyze_by_month_failure():
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 500
        
        with st.container():
            analyze_by_month_tab()
        
        assert "Failed to retrieve analytics data." in st._main._messages
