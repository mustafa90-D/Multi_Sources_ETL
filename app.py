import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Connect to SQLite
conn = sqlite3.connect("../db/retail_sales.db")

# Load retail and product data
df = pd.read_sql("SELECT * FROM retail_analytics", conn)
products_df = pd.read_sql("SELECT * FROM dummyjson_products", conn)

s3_df = pd.read_sql("SELECT * FROM redmi6_specs", conn)
st.header("📦 Redmi Products from S3")
st.dataframe(s3_df.head())

st.title("💼 Retail Dashboard with Live Products")

# Refresh every 10 seconds (10,000 milliseconds)
st_autorefresh(interval=10_000, key="auto-refresh")

# ===================== 📊 RETAIL ANALYTICS =====================
st.header("📊 Retail Sales Overview")
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Year", sorted(df["year"].unique()), index=0)
filtered_df = df[df["year"] == year]

# Sales Over Time
st.subheader("📈 Sales Over Time")
sales_by_day = filtered_df.groupby("sale_date")["total_sales"].sum().reset_index()
fig = px.line(sales_by_day, x="sale_date", y="total_sales", title="Total Sales per Day")
st.plotly_chart(fig)

# Peak day
max_sales_row = sales_by_day.sort_values(by="total_sales", ascending=False).iloc[0]
st.info(f"📌 Highest sales on **{max_sales_row['sale_date']}**: **{max_sales_row['total_sales']:,}**")

# Top Products
st.subheader("🏆 Top 5 Products by Revenue")
top_products = (
    filtered_df.groupby("product")["total_sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)
fig_top = px.bar(top_products, x="product", y="total_sales", title="Top Products")
st.plotly_chart(fig_top)

# Gender Sales
st.subheader("👫 Sales by Gender")
gender_sales = filtered_df.groupby("gender")["total_sales"].sum().reset_index()
fig_gender = px.bar(gender_sales, x="gender", y="total_sales", title="Sales by Gender")
st.plotly_chart(fig_gender)

# Category Sales
st.subheader("📦 Sales by Category")
category_sales = (
    filtered_df.groupby("category")["total_sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
fig_cat = px.bar(category_sales, x="category", y="total_sales", title="Sales by Category")
st.plotly_chart(fig_cat)

fig_price = px.histogram(s3_df, x="rating", nbins=20, title="Rating Distribution (S3)")
st.plotly_chart(fig_price)



# ===================== 🌍 LIVE PRODUCT DATA (DummyJSON) =====================
st.header("🌍 Live Product Prices from DummyJSON")

st.subheader("All Products")
st.dataframe(products_df)

#  Top 5 Most Expensive Products - Pie Chart
st.subheader(" Top 5 Most Expensive Products (Pie Chart)")

top_prices = products_df.sort_values(by="price", ascending=False).head(5)

fig_pie = px.pie(
    top_prices,
    names="title",
    values="price",
    title="Top 5 Products by Price",
    hole=0.3  # for a donut chart look (optional)
)

st.plotly_chart(fig_pie)


# ===================== 🤖 AI Assistant =====================
st.header("🤖 Ask the AI About Your Sales Data")
question = st.text_input("Ask a question like:")
st.caption("e.g. 'What were the top products in Q2?' or 'Compare sales by gender'")

if question:
    with st.spinner("Thinking..."):
        try:
            from langchain_ollama import OllamaLLM
            from langchain_experimental.agents import create_pandas_dataframe_agent
            from langchain.agents import AgentExecutor
            from langchain.agents.agent_types import AgentType

            llm = OllamaLLM(model="llama3")
            base_agent = create_pandas_dataframe_agent(
                llm=llm,
                df=filtered_df,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                allow_dangerous_code=True,
                max_iterations=3,
                verbose=False
            )

            agent = AgentExecutor.from_agent_and_tools(
                agent=base_agent.agent,
                tools=base_agent.tools,
                verbose=True,
                handle_parsing_errors=True
            )

            response = agent.invoke({"input": question})

            if isinstance(response, dict) and "output" in response:
                st.success(response["output"])
            else:
                st.success(response)

        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")

# Close connection
conn.close()
