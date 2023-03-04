import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define a function to retrieve the stock data for a given symbol
@st.cache
def load_data(symbol):
    data = yf.download(symbol)
    return data

# Define a function to clean and process the stock data
def clean_data(data):
    data = data.dropna()
    data['Daily Return'] = data['Adj Close'].pct_change()
    data['Cumulative Return'] = (1 + data['Daily Return']).cumprod()
    return data

# Define a function to display the stock data and charts
def display_data(stock1, stock2, metric):
    st.write(f"### {metric} for {stock1} and {stock2}")

    # Retrieve the stock data and clean it
    data1 = load_data(stock1)
    data2 = load_data(stock2)
    data1 = clean_data(data1)
    data2 = clean_data(data2)

    # Display the stock data and charts
    if metric == 'Stock Price':
        fig, ax = plt.subplots()
        ax.plot(data1['Adj Close'], label=stock1)
        ax.plot(data2['Adj Close'], label=stock2)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        st.pyplot(fig)

    elif metric == 'Daily Returns':
        fig, ax = plt.subplots()
        ax.hist(data1['Daily Return'], alpha=0.5, label=stock1, density=True)
        ax.hist(data2['Daily Return'], alpha=0.5, label=stock2, density=True)
        ax.set_xlabel('Daily Return')
        ax.set_ylabel('Density')
        ax.legend()
        st.pyplot(fig)

    elif metric == 'Cumulative Returns':
        fig, ax = plt.subplots()
        ax.plot(data1['Cumulative Return'], label=stock1)
        ax.plot(data2['Cumulative Return'], label=stock2)
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Return')
        ax.legend()
        st.pyplot(fig)

# Define the main function to run the app
def main():
    st.title("Stock Comparison App")

    # Ask the user to enter the stock symbols
    stock1 = st.text_input("Enter the symbol for stock 1")
    stock2 = st.text_input("Enter the symbol for stock 2")

    # Ask the user to choose a metric to display
    metric = st.selectbox("Choose a metric to compare", ['Stock Price', 'Daily Returns', 'Cumulative Returns'])

    # Display the stock data and charts
    if stock1 and stock2:
        display_data(stock1, stock2, metric)

if __name__ == '__main__':
    main()
