# tabs/dashboard_home.py

import streamlit as st
import pandas as pd

def show(customers, sales):
    st.title("📊 Marketing Dashboard Home")

    st.markdown("Welcome to the dashboard. Use the sidebar to navigate through analysis sections.")

    # --- Basic KPIs ---
    total_customers = customers['Customer_ID'].nunique()
    total_revenue = (sales['Quantity'] * sales['Sale_Price']).sum()
    total_orders = sales['Sale_ID'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("🧍‍♂️ Total Customers", f"{total_customers}")
    kpi2.metric("💰 Total Revenue (€)", f"{total_revenue:,.2f}")
    kpi3.metric("🧾 Avg Order Value (€)", f"{avg_order_value:,.2f}")

    st.markdown("---")
    st.markdown("You can now explore customer segmentation, product trends, and campaign KPIs using the tabs on the left.")
