import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = pd.read_excel("data/sales.xlsx")
df["Order Date"] = pd.to_datetime(df["Order Date"])

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------
st.sidebar.title("🔍 Filters")

date_range = st.sidebar.date_input(
    "Choose Date Range",
    [df["Order Date"].min(), df["Order Date"].max()]
)

if len(date_range) == 2:
    df = df[
        (df["Order Date"] >= pd.to_datetime(date_range[0])) &
        (df["Order Date"] <= pd.to_datetime(date_range[1]))
    ]

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
growth_rate = (total_profit / total_sales) * 100

st.markdown("## 📊 Sales Dashboard")

k1, k2, k3 = st.columns(3)

with k1:
    st.metric("💰 Total Sales", f"{total_sales:,.0f}")

with k2:
    st.metric("📈 Total Profit", f"{total_profit:,.0f}")

with k3:
    st.metric("📊 Growth Rate", f"{growth_rate:.2f}%")

# -------------------------------------------------
# ROW 1
# -------------------------------------------------
c1, c2, c3 = st.columns([2, 1, 1], gap="medium")

# Profit by Product Sub-Category
with c1:
    subcat = (
        df.groupby("Product Sub-Category")["Profit"]
        .sum()
        .sort_values()
        .reset_index()
    )

    fig1 = px.bar(
        subcat,
        x="Profit",
        y="Product Sub-Category",
        orientation="h",
        color="Profit",
        color_continuous_scale="Blues",
        title="Profit by Product Sub-Category"
    )

    fig1.update_layout(height=420)

    st.plotly_chart(fig1, use_container_width=True)

# Ship Mode
with c2:
    ship = (
        df.groupby("Ship Mode")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        ship,
        x="Ship Mode",
        y="Sales",
        markers=True,
        title="Ship Mode Analysis"
    )

    fig2.update_layout(height=420)

    st.plotly_chart(fig2, use_container_width=True)

# Returns by Category
with c3:
    returns = (
        df.groupby("Product Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.area(
        returns,
        x="Product Category",
        y="Sales",
        title="Returns by Category"
    )

    fig3.update_layout(height=420)

    st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------
# SEPARATOR
# -------------------------------------------------
st.markdown("---")

# -------------------------------------------------
# ROW 2 FINAL FIXED
# -------------------------------------------------
c1, c2, c3 = st.columns([1.2, 1, 1], gap="large")

# PIE CHART
with c1:
    pie = (
        df.groupby("Product Sub-Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(8)
        .reset_index()
    )

    fig4 = px.pie(
        pie,
        values="Sales",
        names="Product Sub-Category",
        title="Sales Distribution",
        hole=0.35
    )

    fig4.update_layout(
        height=460,
        legend=dict(
            orientation="h",
            y=-0.25,
            x=0
        ),
        margin=dict(l=20, r=20, t=50, b=80)
    )

    st.plotly_chart(fig4, use_container_width=True)

# TOP PRODUCTS
with c2:
    top = (
        df.groupby("Product Name")["Profit"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

    fig5 = px.bar(
        top,
        x="Profit",
        y="Product Name",
        orientation="h",
        title="Top Products by Profit"
    )

    fig5.update_layout(
        height=460,
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=5, r=5, t=50, b=20)
    )

    st.plotly_chart(fig5, use_container_width=True)

# TABLE
with c3:
    st.markdown("### Customer Segment by Region")

    segment = (
        df.groupby("Customer Segment")["Order Quantity"]
        .sum()
        .reset_index()
    )

    segment.columns = ["Customer Segment", "Order Quantity"]

    st.dataframe(
        segment,
        use_container_width=True,
        height=460,
        hide_index=True
    )

    #python -m streamlit run streamlit_app.py