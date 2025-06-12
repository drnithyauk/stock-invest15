
import streamlit as st
import yfinance as yf
import pandas as pd

def ai_signal(df):
    if 'Close' not in df.columns:
        st.warning("No 'Close' column found in data.")
        return df

    if df['Close'].isna().all() is True:
        st.warning("No valid 'Close' price data available.")
        return df

    df = df.copy()
    df['Signal'] = 'Hold'
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df.dropna(subset=['MA5'], inplace=True)
    df.loc[df['Close'] > df['MA5'], 'Signal'] = 'Buy'
    df.loc[df['Close'] < df['MA5'], 'Signal'] = 'Sell'
    return df

def main():
    st.set_page_config(page_title="Stock AI Insights", layout="centered")
    st.title("📈 Stock Trading Insights")

    ticker_input = st.text_input("Enter stock ticker (e.g., AAPL for Apple Inc.)", "AAPL")

    try:
        df = yf.download(ticker_input, period="6mo", interval="1d")
        if df.empty:
            st.error("No data available for the selected company.")
            return
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return

    df = ai_signal(df)

    if 'Signal' in df.columns:
        st.subheader(f"{ticker_input} - Last 6 Months")
        st.line_chart(df['Close'])

        st.subheader("Trading Signals")
        st.dataframe(df[['Close', 'MA5', 'Signal']].dropna())
    else:
        st.warning("Signal data not available.")

    st.markdown("🛠️ *Next steps: Add real-time news sentiment analysis and portfolio tracking.*")

if __name__ == "__main__":
    main()
