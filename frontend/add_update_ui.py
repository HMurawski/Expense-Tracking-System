import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

def fetch_expenses(selected_date):
    """Fetch expenses for the given date with caching."""
    @st.cache_data(ttl=60)
    def get_data(date):
        response = requests.get(f"{API_URL}/expenses/{date}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return None
    return get_data(selected_date)

def add_update_tab():
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")
    existing_expenses = fetch_expenses(selected_date)
    
    if existing_expenses is None:
        st.error("Could not fetch expenses. Please try again later.")
        return
    
    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]
    expenses = existing_expenses if existing_expenses else [{"amount": 0.0, "category": "Rent", "notes": ""}]
    
    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")
        
        new_expenses = []
        for i, expense in enumerate(expenses):
            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=expense["amount"], key=f"amount_{i}", label_visibility='hidden')
            with col2:
                category_input = st.selectbox(label="Category", options=categories, index=categories.index(expense["category"]), key=f"category_{i}", label_visibility="hidden")
            with col3:
                notes_input = st.text_input(label="Notes", value=expense["notes"], key=f"notes_{i}", label_visibility="hidden")
            
            new_expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })
        
        if st.button("Add More", key="add_more_expenses"):
            new_expenses.append({"amount": 0.0, "category": "Rent", "notes": ""})
            st.rerun()
        
        submit_button = st.form_submit_button()
        if submit_button:
            filtered_expenses = [expense for expense in new_expenses if expense["amount"] > 0]
            
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error(f"Failed to update expenses. Error {response.status_code}: {response.text}")
