import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import matplotlib.pyplot as plt



def dividends(num=6 ,stock_symbol="AAPL" ):
  # Replace 'AAPL' with the stock symbol you're interested in
  stock_symbol = stock_symbol

  # Create Ticker object
  ticker = yf.Ticker(stock_symbol)

  # Fetch historical data including dividends
  data = ticker.history(period='3y', actions=True)

  # Resample data to hourly intervals
  data_hourly = data.resample('1h').ffill()

  data_hourly=data_hourly.reset_index()
  # Extract relevant data (closing prices and dividends)
  closing_prices = data_hourly['Close']
  dividends = data_hourly['Dividends']

  # Calculate market deviance
  market_deviance = closing_prices - dividends
  dividends=data_hourly[data_hourly['Dividends']!=0]

  dividends['date_column'] = dividends['Date'].apply(lambda x: x.date())

  dividends=dividends.drop_duplicates(subset=['date_column'], keep='first')
  ticker = yf.Ticker(stock_symbol)

      # Get dividends data
  dividends_data = ticker.dividends
  dividends_date_list=dividends_data.reset_index()['Date'].tolist()
  if (len(dividends_date_list))>=num:
    length=len(dividends_date_list)
    last_dividends_date_list=dividends_date_list[length-num:]
  else:
    last_dividends_date_list=dividends_date_list
  last_dividends_date_list

  data_list=[]
  length=data_hourly.shape[0]
  for i in last_dividends_date_list:
  # Assuming df is your dataframe
    condition = data_hourly['Date'] ==i
    # Get the index of the first row that satisfies the condition
    row_number = data_hourly.index[condition].tolist()[0]
    new_start_index=-100
    d=data_hourly.iloc[ row_number-100:row_number+100].set_index(pd.Index(range(new_start_index, new_start_index +200)))
    d=d[['Date',	'Open' ,	'High', 	'Low', 	'Close'	, 'Volume']]
    data_list.append(d)
  return data_list
