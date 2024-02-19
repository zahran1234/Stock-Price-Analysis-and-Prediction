import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import matplotlib.pyplot as plt
#from devidents import dividends

##################################### dividends #############################
def dividends(stock_symbol ,num=6 ):
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
######################################## get_short_interest ###########################

def get_short_interest(stock_symbol):
    try:
        # Create a Ticker object
        ticker = yf.Ticker(stock_symbol)

        # Fetch summary information
        info = ticker.info

        # Extract relevant short interest information
        short_interest_data = {
            'Short Shares': info.get('sharesShort', 'N/A'),
            'Short Interest': info.get('shortInterest', 'N/A'),
            'Short Float': info.get('shortPercentOfFloat', 'N/A'),
            'Reporting Date': info.get('lastShortInterestDate', 'N/A')
        }

        return short_interest_data

    except Exception as e:
        print(f"Error fetching short interest data for {stock_symbol}: {e}")
        return None
    
    ##################################### GUI ################################

st.title("Stock Data App")
# Sidebar with user input
st.sidebar.header("User Input")

# Allow user to input stock symbol
stock_symbol = st.sidebar.text_input("Enter Stock Symbol", "AAPL")

# Allow user to input date and time range
from datetime import datetime, timedelta

end_date = datetime.now().date()

start_date = end_date - timedelta(days=7)
start_date = st.sidebar.date_input("Start Date",start_date)
end_date = st.sidebar.date_input("End Date", end_date)
start_time = st.sidebar.time_input("Start Time", pd.to_datetime('4:00:00'))    
end_time = st.sidebar.time_input("End Time", pd.to_datetime('17:59:00'))
submit= st.sidebar.button('submit')
#stock_symbol =stock_symbol # Replace with the stock symbol of your choice
short_interest_data = get_short_interest(stock_symbol)

if short_interest_data:
    print(f"Short Shares: {short_interest_data['Short Shares']}")
    print(f"Short Interest: {short_interest_data['Short Interest']}")
    print(f"Short Float: {short_interest_data['Short Float']}")
    print(f"Reporting Date: {short_interest_data['Reporting Date']}")
if submit:
# Fetch historical stock data
    # Fetch historical stock data and data prepressing 
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date ,  interval="1m" ,prepost=True )
    stock_data=stock_data.asfreq('1T')
    stock_data=stock_data.fillna(method='ffill')
    stock_data=stock_data.between_time(start_time, end_time)

    # Display raw data
    st.subheader("Raw Stock Data")
    st.write(stock_data)

     #Display line chart
    st.subheader("Stock Price Chart")
    st.line_chart(stock_data[['Open' , 'Close']])

    # Line Chart with Y-Axis Limit
    #st.subheader("Line Chart with Y-Axis Limit:")
    #fig, ax = plt.subplots()
    #ax.plot(stock_data['Close'], label='close')
    #ax.plot(stock_data['Open'], label='open')
    # Set Y-Axis Limit
    #y_axis_limit = st.slider("Set Y-Axis Limit", min_value=0, max_value=100, value=(0, 100))
    #ax.set_ylim(y_axis_limit)

    # Display the chart in Streamlit
    #st.pyplot(fig)



    # Display summary statistics
    st.subheader("Summary Statistics for last weak ")
    st.write(stock_data.describe())
    short_interest_data = get_short_interest(stock_symbol)
    if short_interest_data:
        st.table(short_interest_data)
    # Create Ticker object
    ticker = yf.Ticker(stock_symbol)

    # Get dividends data
    dividends_data =dividends(stock_symbol=stock_symbol ,num=6) 

    # Streamlit app title
    st.title(f"Dividends and Earnings for {stock_symbol}")
    # Display dividends data as a table
    st.subheader("Dividends Data:")
    for i in range (len(dividends_data)):
        st.subheader("Dividend : " +str(i+1))
        st.write(dividends_data[len(dividends_data)-i-1])
        st.subheader("statistical analysis for this data before Dividend: " +str(i+1))
        st.write( dividends_data[len(dividends_data)-i-1].iloc[ :100].describe())
        st.subheader("statistical analysis for this data after Dividend: " +str(i+1))
        st.write( dividends_data[len(dividends_data)-i-1].iloc[ 100:].describe())


# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
    api_key = 'CD82V0YRBKXOVLXZ'
    


# Endpoint for quarterly earnings
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={stock_symbol}&apikey={api_key}'

# Make API request
    response = requests.get(url)
    earnings_data = response.json()

# Display earnings data
    #st.write("Earnings Data:")
    #st.write(earnings_data)

    
    

    
