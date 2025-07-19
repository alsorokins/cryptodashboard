# crypto_dashboard.py

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("📊 Crypto Strategy Dashboard")

# Sidebar: Choose tokens
default_tokens = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'APT-USD']
tokens = st.sidebar.multiselect("Select tokens", default_tokens, default=default_tokens)

# Date range
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# Load data
@st.cache_data
def load_data(tickers, start, end):
    df = yf.download(tickers, start=start, end=end)['Close']
    return df.ffill()

data = load_data(tokens, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

# Normalize prices
normalized = data / data.iloc[0]

# Daily returns
returns = data.pct_change().dropna()
cumulative_returns = (1 + returns).cumprod() * 100

# Layout
col1, col2 = st.columns(2)

# Price Chart
with col1:
    st.subheader("Normalized Prices (Start = 1)")
    st.line_chart(normalized)

# Cumulative Returns
with col2:
    st.subheader("Cumulative Returns (Start = $100)")
    st.line_chart(cumulative_returns)

# Show raw data
with st.expander("Show raw price data"):
    st.write(data.tail())

