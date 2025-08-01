# tabs/kpi_insights.py

import streamlit as st
import pandas as pd

def show(kpi_summary, segments_summary):
    st.header("KPI Insights")


    # Textual insights
    top_segment = segments_summary.sort_values("Count_in_cluster", ascending=False).iloc[0]
    st.info(f"📌 Largest segment is Cluster {top_segment['Cluster']} with {top_segment['Count_in_cluster']} customers.")


    total_impressions = kpi_summary["Impressions"].sum()
    total_conversions = kpi_summary["Conversions"].sum()
    total_budget = kpi_summary["Budget"].sum()

    ctr = (kpi_summary["CTR"].mean()) * 100
    conversion_rate = (kpi_summary["Conversion_Rate"].mean()) * 100
    roi = ((total_conversions * 50) - total_budget) / total_budget * 100 if total_budget > 0 else 0

    st.metric("Total Impressions", f"{total_impressions:,}")
    st.metric("Total Conversions", f"{total_conversions:,}")
    st.metric("Total Budget (€)", f"{total_budget:,.2f}")
    st.metric("CTR (%)", f"{ctr:.2f}")
    st.metric("Conversion Rate (%)", f"{conversion_rate:.2f}")
    st.metric("ROI (%)", f"{roi:.2f}")

    st.markdown("---")
    st.markdown("Use other tabs for deep dives on customers, products, and campaigns.")
