import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns 
import plotly.graph_objects as go
from datetime import datetime, timedelta


pd.options.mode.copy_on_write = True

import requests


def get_range(earnings_history):
  # Your timestamp
  timestamp_str = earnings_history
  timestamp = pd.Timestamp(timestamp_str)
  # Define the time range
  minutes_before = 100
  minutes_after = 100
  # Generate the list of timestamps
  time_range = [timestamp - pd.Timedelta(hours=i) for i in range(0, minutes_before + 1)]
  time_range += [timestamp + pd.Timedelta(hours=i) for i in range(1, minutes_after + 1)]
  # Print the results
  li=[]
  for ts in time_range:
      li.append(ts)
  return li

def earning_show(stock_symbol):

    # Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
    api_key = 'CD82V0YRBKXOVLXZ'
    symbol = 'AAPL'
    # Endpoint for quarterly earnings
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={api_key}'

    # Make API request
    #response = requests.get(url)

    # Create a Ticker object
    ticker = yf.Ticker(stock_symbol)
    st.write(ticker.earnings_dates.reset_index())

    earnings_history = ticker.earnings_dates.index[1:]
    eraning_dates= earnings_history

    #earnings_data = response.json()

    # Display earnings data

    #datetime.strptime(eraning_dates[0], '%Y-%m-%d').date()
    all_earning_date=[]
    for i in eraning_dates:
        all_earning_date.append(get_range(i))
        #all_earning_date.append([ i ])
    # Replace 'AAPL' with the stock symbol you're interested in
        
    pd.options.mode.copy_on_write = True
    

    # Create Ticker object
    ticker = yf.Ticker(stock_symbol)

    # Fetch historical data including dividends
    data = ticker.history(period='3y', actions=True)

    # Resample data to hourly intervals

    data_hourly = data.resample('1min').ffill()

    data_min=data_hourly.reset_index()
    data_min['date_column'] = data_min['Date'].apply(lambda x: x.date())
    list_earning_data=[]

    for i in all_earning_date:
        df=data_min[data_min['Date'].isin(i)]
        if df.shape[0]>0:
            list_earning_data.append(df[['Date',	'Open' ,	'High', 	'Low', 	'Close'	, 'Volume']])
    if len(list_earning_data)>4:
        dividends_data=list_earning_data[:4]
    else:
        dividends_data=list_earning_data

    dividends_data.reverse()
    for i in range (len(dividends_data)):
        st.subheader("earnings : " +str(i+1))
        st.write(dividends_data[len(dividends_data)-i-1])
        
        constant_y_range = ( dividends_data[len(dividends_data)-i-1]['Low'].min(),dividends_data[len(dividends_data)-i-1]['High'].max())

        # Create Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(x=dividends_data[len(dividends_data)-i-1].Date,
                                            open=dividends_data[len(dividends_data)-i-1]['Open'],
                                            high=dividends_data[len(dividends_data)-i-1]['High'],
                                            low=dividends_data[len(dividends_data)-i-1]['Low'],
                                            close=dividends_data[len(dividends_data)-i-1]['Close'])])

        # Set chart title and labels
        fig.update_layout(title=f" Candlestick Chart  earnings",
                        xaxis_title="Date",
                        yaxis_title="Stock Price")
        
        # Display the chart in Streamlit
        #st.plotly_chart(fig)

        fig = px.line(dividends_data[len(dividends_data)-i-1].reset_index(), x='Date', y=['Open' , 'Close' , 'Low' , 'High'], title='Line Chart earning date: ' +str(eraning_dates[i]), labels={'Value': 'Y-Axis Label'})
    
        fig.update_yaxes(range=constant_y_range )
        #fig.update_layout(height=600, width=800)
        st.plotly_chart(fig, use_container_width=True )
        st.subheader("statistical analysis for earnings : " +str(eraning_dates[i]))
        st.write( dividends_data[len(dividends_data)-i-1].describe())