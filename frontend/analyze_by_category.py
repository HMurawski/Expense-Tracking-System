import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000"

def fetch_analytics(start_date, end_date):
    """Fetch analytics data with caching."""
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

def analyze_by_category_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Analyze!", key="analyze_by_category"):
        response_data = fetch_analytics(start_date, end_date)
        if response_data is None:
            return
        
        if not response_data:
            st.warning("No expenses found for the selected date range.")
            return
        
        data = {
            "Category": [item["category"] for item in response_data],
            "Total": [item["total"] for item in response_data],
            "Percentage": [item["percentage"] for item in response_data]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Percentage", ascending=False)

        st.title("Expense Breakdown")
        chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"], index=0)
        
        if chart_type == "Bar Chart":
            st.bar_chart(df_sorted.set_index("Category")["Total"])
        else:
            fig, ax = plt.subplots()
            ax.pie(df_sorted["Total"], labels=df_sorted["Category"], autopct='%1.1f%%', startangle=90)
            ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig)
        
        st.table(df_sorted)