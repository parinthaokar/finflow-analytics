import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector
import os

st.set_page_config(page_title="FinFlow Fraud Dashboard", layout="wide")

st.title(" FinFlow — Fraud Intelligence Dashboard")
st.markdown("Real-time fraud detection powered by Kafka → Snowflake → dbt")

conn = snowflake.connector.connect(
    user=os.environ.get('SNOWFLAKE_USER'),
    password=os.environ.get('SNOWFLAKE_PASSWORD'),
    account=os.environ.get('SNOWFLAKE_ACCOUNT'),
    warehouse='COMPUTE_WH',
    database='FINFLOW',
    schema='SILVER_GOLD'
)
cursor = conn.cursor()
df = cursor.execute("SELECT * FROM FRAUD_SCORES").fetch_pandas_all()
cursor.close()
conn.close()

# KPI Cards
count = (df['IS_FRAUD'] == True).sum()
col1, col2 = st.columns(2)
col1.metric("Total Transactions", df['TRANSACTION_ID'].count(), border=True)
col2.metric("Total Fraud Transactions", count, border=True)

st.markdown("---")

# Charts side by side
col3, col4 = st.columns(2)

with col3:
    top_5_df = df.sort_values(by="FRAUD_RATE", ascending=False).head(5)
    fig = px.bar(top_5_df, x="MERCHANT_ID", y="FRAUD_RATE", title="Top 5 Merchants by Fraud Rate")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    risk_counts = df['RISK_LABEL'].value_counts().reset_index()
    risk_counts.columns = ['RISK_LABEL', 'COUNT']
    fig2 = px.pie(
        risk_counts,
        names='RISK_LABEL',
        values='COUNT',
        title='Risk Label Distribution',
        color='RISK_LABEL',
        color_discrete_map={'HIGH': '#FF4444', 'MEDIUM': '#FFA500', 'LOW': '#00CC44'}
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# High Risk Transactions Table
st.subheader(" High Risk Transactions")
high_risk = df[df['RISK_LABEL'] == 'HIGH'][
    ['TRANSACTION_ID', 'USER_ID', 'MERCHANT_ID', 'AMOUNT', 'RISK_SCORE']
].sort_values('RISK_SCORE', ascending=False).head(10)
st.dataframe(high_risk, use_container_width=True)