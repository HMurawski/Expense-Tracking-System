import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000"

def fetch_monthly_analytics(start_date, end_date):
    """Fetch monthly analytics data with caching."""
    @st.cache_data(ttl=60)
    def get_data(start, end):
        payload = {"start_date": start.strftime("%Y-%m-%d"), "end_date": end.strftime("%Y-%m-%d")}
        response = requests.post(f"{API_URL}/analytics/", json=payload)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return None
    return get_data(start_date, end_date)

def analyze_by_month_tab():
    st.title("Monthly Expense Analysis")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 1, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 12, 31))

    if st.button("Analyze!", key="analyze_by_month"):
        response_data = fetch_monthly_analytics(start_date, end_date)
        if response_data is None:
            return
        
        if not response_data:
            st.warning("No expenses found for the selected date range.")
            return
        
        data = {
            "Category": [item["category"] for item in response_data],
            "Total": [item["total"] for item in response_data]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Total", ascending=False)

        st.subheader("Expense Distribution by Category")
        fig, ax = plt.subplots()
        ax.bar(df_sorted["Category"], df_sorted["Total"], color="skyblue")
        ax.set_xlabel("Category")
        ax.set_ylabel("Total Expenses")
        ax.set_title("Expenses by Category")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        st.table(df_sorted)
