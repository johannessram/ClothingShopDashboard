import tabs.customer_segmentation as customer_tab
import tabs.product_analysis as product_tab
import tabs.campaign_performance as campaign_tab
import tabs.dashboard_home as home_tab
import tabs.kpi_insights as kpi_tab

import streamlit as st
import pandas as pd
import datetime
from load_data import load_data


customers, products, sales, campaigns, segments_summary, cross_segmentation, kpi_summary = load_data()

# Sidebar filters

# 1. Date range filter for Sales data
min_date = pd.to_datetime(sales['Date']).min()
max_date = pd.to_datetime(sales['Date']).max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if len(date_range) != 2:
    st.sidebar.error("Please select a start and end date.")

start_date, end_date = date_range

# 2. Customer Segment filter
segment_options = segments_summary['Cluster'].unique()
selected_segments = st.sidebar.multiselect(
    "Select Customer Segment(s)",
    options=segment_options,
    default=list(segment_options)
)

# 3. Product Category filter
category_options = products['Category'].unique()
selected_categories = st.sidebar.multiselect(
    "Select Product Category(ies)",
    options=category_options,
    default=list(category_options)
)

# 4. Marketing Campaign Channel filter
campaign_channels = campaigns['Channel'].unique()
selected_channels = st.sidebar.multiselect(
    "Select Campaign Channel(s)",
    options=campaign_channels,
    default=list(campaign_channels)
)

# Filter datasets based on sidebar inputs

# Filter sales by date range
filtered_sales = sales[
    (pd.to_datetime(sales['Date']) >= pd.to_datetime(start_date)) &
    (pd.to_datetime(sales['Date']) <= pd.to_datetime(end_date))
]

# Filter products by category
filtered_products = products[products['Category'].isin(selected_categories)]

# Filter campaigns by channel and date range (assuming Start_Date and End_Date in campaigns)
filtered_campaigns = campaigns[
    (campaigns['Channel'].isin(selected_channels)) &
    (pd.to_datetime(campaigns['Start_Date']) <= pd.to_datetime(end_date)) &
    (pd.to_datetime(campaigns['End_Date']) >= pd.to_datetime(start_date))
]

# Display filters summary (optional)
st.sidebar.markdown("### Current Filters")
st.sidebar.write(f"Date Range: {start_date} to {end_date}")
st.sidebar.write(f"Segments: {selected_segments}")
st.sidebar.write(f"Categories: {selected_categories}")
st.sidebar.write(f"Campaign Channels: {selected_channels}")




######### Navigation
selected_tab = st.sidebar.radio("Navigate", [
    "Dashboard Home",
    "KPI Insights",
    "Customer Segmentation",
    "Product Analysis",
    "Campaign Performance"
])
if selected_tab == "Dashboard Home":
    home_tab.show(customers, sales)

elif selected_tab == "KPI Insights":
    kpi_tab.show(kpi_summary, segments_summary)  # pass kpi_summary here

elif selected_tab == "Customer Segmentation":
    customer_tab.show(customers, segments_summary, selected_segments)

elif selected_tab == "Product Analysis":
    product_tab.show(filtered_sales, filtered_products, cross_segmentation, selected_categories)

elif selected_tab == "Campaign Performance":
    campaign_tab.show(filtered_campaigns, selected_channels, start_date, end_date)  # pass campaigns filtered
