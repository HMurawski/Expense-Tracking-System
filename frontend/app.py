import streamlit as st

st.title("Expense Tracking System")

expense_dt = st.date_input("Expense Date:")
if expense_dt:
    st.write(f"Fetching expenses for {expense_dt}")
