import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

# Database connection
def get_connection():
    return psycopg2.connect(
        dbname="dq_db", user="dq_user",
        password="dq_pass", host="postgres"
    )

# Dashboard layout
st.set_page_config(layout="wide")
st.title("Data Quality Monitoring Dashboard")

# Raw Data Section
conn = get_connection()

col1, col2 = st.columns(2)

with col1:
    st.header("Raw Data Metrics")
    raw_stats = pd.read_sql("""
        SELECT 
            COUNT(*) AS total_records,
            SUM(CASE WHEN sale_amount IS NULL THEN 1 ELSE 0 END) AS null_sales,
            COUNT(DISTINCT transaction_id) AS unique_transactions
        FROM raw_sales
    """, conn)
    
    st.metric("Total Records", raw_stats['total_records'][0])
    st.metric("Null Sales Amounts", raw_stats['null_sales'][0])
    st.metric("Unique Transactions", raw_stats['unique_transactions'][0])

with col2:
    st.header("Data Distribution")
    df = pd.read_sql("SELECT region, SUM(sale_amount) AS total FROM raw_sales GROUP BY region", conn)
    fig = px.pie(df, values='total', names='region', title='Sales by Region')
    st.plotly_chart(fig)

# Clean Data Section
st.header("Clean Data Overview")
clean_data = pd.read_sql("SELECT * FROM clean_sales", conn)
st.dataframe(clean_data)

# Data Quality Issues
st.header("Quality Issues Breakdown")
issues = pd.read_sql("""
    SELECT 
        'Duplicate Transactions' AS issue_type,
        COUNT(*) - COUNT(DISTINCT transaction_id) AS count
    FROM raw_sales
    
    UNION ALL
    
    SELECT 
        'Negative Sales' AS issue_type,
        COUNT(*) 
    FROM raw_sales 
    WHERE sale_amount < 0
    
    UNION ALL
    
    SELECT 
        'Missing Sales Amount' AS issue_type,
        COUNT(*) 
    FROM raw_sales 
    WHERE sale_amount IS NULL
""", conn)

fig = px.bar(issues, x='issue_type', y='count', title='Data Quality Issues')
st.plotly_chart(fig)

conn.close()