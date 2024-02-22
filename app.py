import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns 
import plotly.graph_objects as go
from datetime import datetime, timedelta
from predication import train_and_predication
from earnings import earning_show
pd.options.mode.copy_on_write = True

import os

os.system('echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p')

from dividends import dividends , calculate_average_changes ,get_short_interest , display_stock_information ,analysis_last_week

st.title("Stock Data App")
# Sidebar with user input
st.sidebar.header("User Input")
# Allow user to input stock symbol
stock_symbol = st.sidebar.text_input("Enter Stock Symbol", "GOOG")

# Allow user to input date and time range
end_date = datetime.now().date()
start_date = end_date - timedelta(days=7)
start_date = st.sidebar.date_input("Start Date",start_date)
end_date = st.sidebar.date_input("End Date", end_date)
start_time = st.sidebar.time_input("Start Time", pd.to_datetime('4:00:00'))    
end_time = st.sidebar.time_input("End Time", pd.to_datetime('17:59:00'))
submit= st.sidebar.button('submit')
submit_with_ai= st.sidebar.button('submit with ai ')

#stock_symbol =stock_symbol # Replace with the stock symbol of your choice
short_interest_data = get_short_interest(stock_symbol)

if short_interest_data:
    print(f"Short Shares: {short_interest_data['Short Shares']}")
    print(f"Short Interest: {short_interest_data['Short Interest']}")
    print(f"Short Float: {short_interest_data['Short Float']}")
    print(f"Reporting Date: {short_interest_data['Reporting Date']}")

if submit:
    
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date ,  interval="1m" ,prepost=True )
    stock_data=stock_data.asfreq('1T')
    stock_data=stock_data.fillna(method='ffill')
    stock_data=stock_data.between_time(start_time, end_time)
    
    display_stock_information(stock_symbol, stock_data['Close'][len(stock_data['Close'].tolist())-1])
    analysis_last_week(stock_data,stock_symbol)
    dividends(stock_symbol=stock_symbol ,num=6) 
    earning_show(stock_symbol)
    #api_key = 'AMNYBKHTP0TTTE1Y'
    
    #url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={stock_symbol}&apikey={api_key}'

    #response = requests.get(url)
    #earnings_data = response.json()

    #st.write("Earnings Data:")
    #st.write(earnings_data)
elif submit_with_ai:
    st.subheader("the next day predication : " +str(train_and_predication(stock_symbol)))
    
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date ,  interval="1m" ,prepost=True )
    stock_data=stock_data.asfreq('1T')
    stock_data=stock_data.fillna(method='ffill')
    stock_data=stock_data.between_time(start_time, end_time)
    display_stock_information(stock_symbol, stock_data['Close'][len(stock_data['Close'].tolist())-1])
    analysis_last_week(stock_data,stock_symbol)
    
    dividends(stock_symbol=stock_symbol ,num=6) 
    


    
    

    
