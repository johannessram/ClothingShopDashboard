# tabs/campaign_performance.py

import streamlit as st
import pandas as pd
import plotly.express as px


def show(campaigns, selected_channels, start_date, end_date):
    st.header("Marketing Campaign Performance")

    # Calculate Conversion Rate if not already present
    if 'Conversion_Rate' not in campaigns.columns:
        # Avoid division by zero
        campaigns['Conversion_Rate'] = campaigns.apply(
            lambda row: (row['Conversions'] / row['Sondage']) if row['Sondage'] > 0 else 0,
            axis=1
        )

    # Now find best channel by Conversion Rate
    best_channel = campaigns.sort_values('Conversion_Rate', ascending=False).iloc[0]
    st.info(f"📈 The most effective channel is **{best_channel['Channel']}** with a conversion rate of {best_channel['Conversion_Rate']:.2%}.")

    # Convert dates
    campaigns["Start_Date"] = pd.to_datetime(campaigns["Start_Date"])
    campaigns["End_Date"] = pd.to_datetime(campaigns["End_Date"])

    # Filter campaigns by selected channels and date range
    filtered = campaigns[
        (campaigns["Channel"].isin(selected_channels)) &
        (campaigns["Start_Date"] <= pd.to_datetime(end_date)) &
        (campaigns["End_Date"] >= pd.to_datetime(start_date))
    ].copy()


    if filtered.empty:
        st.warning("No campaigns match the selected filters.")
        return

    # --- KPI Summary Cards ---
    st.subheader("Key Performance Indicators (KPI)")

    total_impressions = int(filtered["Impressions"].sum())
    total_conversions = int(filtered["Conversions"].sum())
    total_budget = filtered["Budget"].sum()
    total_ctr = (filtered["Sondage"].sum() / filtered["Impressions"].sum()) * 100 if filtered["Impressions"].sum() > 0 else 0
    conv_rate = (filtered["Conversions"].sum() / filtered["Sondage"].sum()) * 100 if filtered["Sondage"].sum() > 0 else 0
    cpa = total_budget / filtered["Conversions"].sum() if filtered["Conversions"].sum() > 0 else 0
    cpc = total_budget / filtered["Sondage"].sum() if filtered["Sondage"].sum() > 0 else 0
    roi = ((filtered["Conversions"].sum() * 50) - total_budget) / total_budget * 100 if total_budget > 0 else 0  # assume revenue per conversion = 50€

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("CTR (%)", f"{total_ctr:.2f}")
    kpi2.metric("Conversion Rate (%)", f"{conv_rate:.2f}")
    kpi3.metric("ROI (%)", f"{roi:.2f}")

    kpi4, kpi5, kpi6 = st.columns(3)
    kpi4.metric("CPC (€)", f"{cpc:.2f}")
    kpi5.metric("CPA (€)", f"{cpa:.2f}")
    kpi6.metric("Conversions", f"{total_conversions}")

    # --- Bar Chart: KPI by Channel ---
    st.subheader("Campaign CTR by Channel")
    filtered["CTR"] = filtered["Sondage"] / filtered["Impressions"]
    ctr_by_channel = filtered.groupby("Channel")["CTR"].mean().reset_index()
    fig_ctr = px.bar(ctr_by_channel, x="Channel", y="CTR", title="Average CTR by Channel")
    st.plotly_chart(fig_ctr, use_container_width=True)

    # --- Time Series: Campaigns Over Time ---
    st.subheader("Campaign Volume Over Time")
    filtered["Month"] = filtered["Start_Date"].dt.to_period("M").astype(str)
    monthly = filtered.groupby(["Month", "Channel"])[["Impressions", "Sondage", "Conversions"]].sum().reset_index()
    fig_time = px.line(
        monthly,
        x="Month",
        y="Conversions",
        color="Channel",
        markers=True,
        title="Conversions Over Time by Channel"
    )
    st.plotly_chart(fig_time, use_container_width=True)
