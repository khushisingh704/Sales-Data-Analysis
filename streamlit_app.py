import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# ---------- LOAD DATA ----------
df = pd.read_excel("data/sales.xlsx")
df['Order Date'] = pd.to_datetime(df['Order Date'])

# ---------- SIDEBAR ----------
st.sidebar.title("🔍 Filters")

date_range = st.sidebar.date_input(
    "Order Date",
    [df['Order Date'].min(), df['Order Date'].max()]
)

if len(date_range) == 2:
    df = df[(df['Order Date'] >= pd.to_datetime(date_range[0])) &
            (df['Order Date'] <= pd.to_datetime(date_range[1]))]

# ---------- KPI CARDS ----------
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
growth_rate = (total_profit / total_sales) * 100

st.markdown("## 📊 Sales Dashboard")

k1, k2, k3 = st.columns(3)

k1.markdown(f"""
### 💰 Total Sales  
### {total_sales:,.0f}
""")

k2.markdown(f"""
### 📈 Total Profit  
### {total_profit:,.0f}
""")

k3.markdown(f"""
### 📊 Growth Rate  
### {growth_rate:.2f}%
""")

# ---------- ROW 1 ----------
c1, c2, c3 = st.columns([2,1,1])

# Profit Margin style (positive & negative)
subcat = df.groupby('Product Sub-Category')['Profit'].sum().sort_values()

fig1 = px.bar(
    subcat,
    orientation='h',
    color=subcat,
    color_continuous_scale=['red','blue'],
    title="Profit by Product Sub-Category"
)
c1.plotly_chart(fig1, use_container_width=True)

# Ship Mode
ship = df.groupby('Ship Mode')['Sales'].sum().reset_index()
fig2 = px.line(ship, x='Ship Mode', y='Sales', markers=True,
               title="Ship Mode Analysis")
c2.plotly_chart(fig2, use_container_width=True)

# Returns (approx)
returns = df.groupby('Product Category')['Sales'].sum().reset_index()
fig3 = px.area(returns, x='Product Category', y='Sales',
               title="Returns by Category")
c3.plotly_chart(fig3, use_container_width=True)

# ---------- ROW 2 ----------
c1, c2, c3 = st.columns(3)

# Pie
pie = df.groupby('Product Sub-Category')['Sales'].sum().reset_index()
fig4 = px.pie(pie, values='Sales', names='Product Sub-Category',
              title="Sales Distribution")
c1.plotly_chart(fig4, use_container_width=True)

# Top products
top = df.groupby('Product Name')['Profit'].sum().nlargest(10).reset_index()
fig5 = px.bar(top, x='Profit', y='Product Name',
              orientation='h',
              title="Top Products by Profit")
c2.plotly_chart(fig5, use_container_width=True)

# Table
segment = df.groupby('Customer Segment')['Order Quantity'].sum().reset_index()
segment.columns = ['Customer Segment', 'Order Quantity']
c3.dataframe(segment, use_container_width=True)
