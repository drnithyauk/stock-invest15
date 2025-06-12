
import streamlit as st
import pandas as pd
import yfinance as yf

COMPANY_TICKER_MAP = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Alphabet (Google)": "GOOGL",
    "Meta (Facebook)": "META"
}

def fetch_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")
    return df

def ai_signal(df):
    df = df.copy()

    if 'Close' not in df.columns:
        st.warning("No 'Close' column found in data.")
        return df

    if df['Close'].isna().all():
        st.warning("No valid 'Close' price data available.")
        return df

    df['Signal'] = 'Hold'
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df.dropna(subset=['MA5'], inplace=True)
    df.loc[df['Close'] > df['MA5'], 'Signal'] = 'Buy'
    df.loc[df['Close'] < df['MA5'], 'Signal'] = 'Sell'
    return df

def main():
    st.set_page_config(page_title="AI Stock Insights", layout="wide")
    st.markdown("<h1 style='text-align: center; color: white; background-color:#007BFF; padding: 10px;'>AI Stock Insights</h1>", unsafe_allow_html=True)
    company = st.selectbox("Select a company", list(COMPANY_TICKER_MAP.keys()))
    ticker = COMPANY_TICKER_MAP[company]

    df = fetch_data(ticker)

    if df.empty:
        st.error("No data available for the selected company.")
        return

    df = ai_signal(df)

    st.subheader(f"{company} ({ticker}) - Last 6 Months")
    st.line_chart(df['Close'])
    st.dataframe(df.tail(10))
    st.markdown("🛠️ *Next steps: Add real-time news sentiment analysis and portfolio tracking features here...*")

if __name__ == "__main__":
    main()
