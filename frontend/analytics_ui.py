import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }
        response = requests.post(f"{API_URL}/analytics/", json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            
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
            st.bar_chart(df_sorted.set_index("Category")["Total"])
            st.table(df_sorted)
        else:
            st.error("Failed to retrieve analytics data.")

            
            