
import streamlit as st
import yfinance as yf
import pandas as pd

def fetch_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")
    return df

def ai_signal(df):
    if 'Close' not in df.columns:
        st.warning("No 'Close' column found in data.")
        return df
    if df['Close'].isna().all():
        st.warning("No valid 'Close' price data available.")
        return df
    df = df.copy()
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df.dropna(subset=['MA5'], inplace=True)
    df['Signal'] = 'Hold'
    df.loc[df['Close'] > df['MA5'], 'Signal'] = 'Buy'
    df.loc[df['Close'] < df['MA5'], 'Signal'] = 'Sell'
    return df

def main():
    st.title("📈 Stock AI Insights")
    company = st.text_input("Enter Company Name (e.g., Apple)", "Apple")
    symbol_lookup = {
        "Apple": "AAPL",
        "Tesla": "TSLA",
        "Amazon": "AMZN",
        "Microsoft": "MSFT",
        "Google": "GOOGL",
        "Meta": "META",
    }
    ticker = symbol_lookup.get(company.title(), None)

    if not ticker:
        st.error("Company not found. Please enter a valid company name.")
        return

    df = fetch_data(ticker)
    if df.empty or 'Close' not in df.columns:
        st.error("No data available for the selected company.")
        return

    df = ai_signal(df)
    if 'Signal' in df.columns:
        st.subheader(f"{company} ({ticker}) - Last 6 Months")
        st.line_chart(df['Close'])
        st.dataframe(df.tail(10))
    st.markdown("🛠️ *Next steps: Add real-time news sentiment analysis and portfolio tracking.*")

if __name__ == "__main__":
    main()
