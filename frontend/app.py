import streamlit as st
from add_update_ui import add_update_tab
from analyze_by_category import analyze_by_category_tab
from analyze_by_month import analyze_by_month_tab

API_URL = "http://localhost:8000"

st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analyze by Category", "Analyze by Month"])

with tab1:
    add_update_tab()
with tab2:
    analyze_by_category_tab()
with tab3:
    analyze_by_month_tab()