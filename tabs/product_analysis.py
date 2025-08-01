# tabs/product_analysis.py

import streamlit as st
import pandas as pd
import plotly.express as px

def show(sales, products, cross_segmentation, selected_categories):
    st.header("Product Analysis")
    top_category = sales.merge(products, on='Product_ID')['Category'].value_counts().idxmax()
    st.info(f"🛒 The best-selling product category is **{top_category}**.")


    # Filter products by selected categories
    filtered_products = products[products['Category'].isin(selected_categories)]

    # Join sales with product info
    merged = pd.merge(sales, filtered_products, on="Product_ID")

    # --- Top Products by Quantity ---
    st.subheader("Top Products by Quantity Sold")
    top_quantity = (
        merged.groupby("Product_Name")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig1 = px.bar(top_quantity, x="Quantity", y="Product_Name", orientation='h')
    st.plotly_chart(fig1, use_container_width=True)

    # --- Top Products by Revenue ---
    st.subheader("Top Products by Revenue")
    merged["Revenue"] = merged["Quantity"] * merged["Sale_Price"]
    top_revenue = (
        merged.groupby("Product_Name")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(top_revenue, x="Revenue", y="Product_Name", orientation='h')
    st.plotly_chart(fig2, use_container_width=True)

    # --- Cross-Segmentation Heatmap ---
    st.subheader("Product Category × Age Group")
    cross_df = cross_segmentation.set_index("Category").loc[selected_categories]
    st.dataframe(cross_df)

    fig3 = px.imshow(
        cross_df,
        labels=dict(x="Age Group", y="Category", color="Purchases"),
        aspect="auto",
        text_auto=True,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig3, use_container_width=True)
