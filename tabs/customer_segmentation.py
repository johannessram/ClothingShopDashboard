# tabs/customer_segmentation.py

import streamlit as st
import pandas as pd
import plotly.express as px


def show(customers, segments_summary, selected_segments):
    st.header("Customer Segmentation")
    top_cluster = segments_summary.sort_values('Count_in_cluster', ascending=False).iloc[0]
    st.info(f"📌 Most customers belong to Cluster {top_cluster['Cluster']} with average spending of €{top_cluster['Total_Spent']:.2f}.")

    # Filter customers by selected segment(s)
    filtered_customers = customers[customers['Cluster'].isin(selected_segments)]

    # --- Segment Summary Table ---
    st.subheader("Segment Overview")
    st.dataframe(segments_summary[segments_summary['Cluster'].isin(selected_segments)])

    # --- Scatter Plot: Age vs Total Spent ---
    st.subheader("Age vs Total Spent (by Segment)")
    fig = px.scatter(
        filtered_customers,
        x='Age',
        y='Total_Spent',
        color='Cluster',
        hover_data=['Gender'],
        title="Customer Clusters"
    )
    st.plotly_chart(fig, use_container_width=True)
