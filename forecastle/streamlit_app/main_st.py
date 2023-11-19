from datetime import date

import streamlit as st
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

import yfinance as yf

START = "2018-01-01"
TODAY = date.today().strftime("%Y-%m-%d")


@st.cache
def load_data(ticker):
    ticker_data = yf.download(ticker, START, TODAY)

    # put date in 1st column
    ticker_data.reset_index(inplace=True)

    return ticker_data


def plot_raw_data(ticker_data):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=ticker_data["Date"], y=ticker_data["Open"], name="stock_open")
    )
    fig.add_trace(
        go.Scatter(x=ticker_data["Date"], y=ticker_data["Close"], name="stock_close")
    )
    fig.layout.update(title_text="Time series data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


st.title("Stock Prediction App")

stocks = ("AAPL", "GOOG", "MSFT", "GME")

selected_stock = st.selectbox("Select dataset for prediction", stocks)

n_years = st.slider("Years of prediction:", 1, 4)
period = n_years * 365

data_load_state = st.text("Load data...")
data = load_data(selected_stock)
data_load_state.text("Loading data... Done!")

st.subheader("Raw data")
st.write(data.tail())

plot_raw_data(data)

# Forecasting
df_train = data[["Date", "Close"]]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

model = Prophet()
model.fit(df_train)

future = model.make_future_dataframe(periods=period)
forecast = model.predict(future)

st.subheader("Forecast data")
st.write(forecast.tail())

fig1 = plot_plotly(model, forecast)
fig1.write_image("images/fig1.png")
fig1.write_image("images/fig1.webp")
fig1.write_image("images/fig1.svg")

st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = model.plot_components(forecast)
st.write(fig2)
