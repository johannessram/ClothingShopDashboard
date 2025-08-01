import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    customers = pd.read_csv('data/new_customers_data.csv')
    products = pd.read_csv('data/products_data.csv')
    sales = pd.read_csv('data/sales_data.csv')
    campaigns = pd.read_csv('data/marketing_data.csv')
    segments_summary = pd.read_csv('data/cluster_summary.csv')
    cross_segmentation = pd.read_csv('data/age_category_matrix.csv')
    kpi_summary = pd.read_csv('data/kpi_summary.csv')  # <-- new line
    return customers, products, sales, campaigns, segments_summary, cross_segmentation, kpi_summary
