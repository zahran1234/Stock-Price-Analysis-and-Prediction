
import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns 
import plotly.graph_objects as go


left_column, right_column = st.columns(2)

def dividends(stock_symbol ,num=6 ):
  # Replace 'AAPL' with the stock symbol you're interested in
  stock_symbol = stock_symbol
  # Create Ticker object
  ticker = yf.Ticker(stock_symbol)

  # Fetch historical data including dividends
  data = ticker.history(period='7y', actions=True)

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
    # Streamlit app title
  st.title(f"Dividends and Earnings for {stock_symbol}")
   # Display dividends data as a table
  st.subheader("Dividends Data:")
  dividends_data=data_list
  for i in range (len(dividends_data)):
        st.subheader("Dividend : " +str(i+1))
        st.write(dividends_data[len(dividends_data)-i-1])
        st.subheader("statistical analysis for this data before Dividend: " +str(i+1))
        st.write( dividends_data[len(dividends_data)-i-1].iloc[ :100].describe())
        st.subheader("statistical analysis for this data after Dividend: " +str(i+1))
        st.write( dividends_data[len(dividends_data)-i-1].iloc[ 100:].describe())
        constant_y_range = ( dividends_data[len(dividends_data)-i-1]['Low'].min(),dividends_data[len(dividends_data)-i-1]['High'].max())

        # Create Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(x=dividends_data[len(dividends_data)-i-1].index,
                                            open=dividends_data[len(dividends_data)-i-1]['Open'],
                                            high=dividends_data[len(dividends_data)-i-1]['High'],
                                            low=dividends_data[len(dividends_data)-i-1]['Low'],
                                            close=dividends_data[len(dividends_data)-i-1]['Close'])])

        # Set chart title and labels
        fig.update_layout(title=f" Candlestick Chart  before and after Dividend , Dividend represented by 0 in x-axis",
                        xaxis_title="Date",
                        yaxis_title="Stock Price")

        # Display the chart in Streamlit
        st.plotly_chart(fig)

        fig = px.line(dividends_data[len(dividends_data)-i-1].reset_index(), x='index', y=['Open' , 'Close' , 'Low' , 'High'], title='Line Chart before and after Dividend , Dividend represented by 0 in x-axis ', labels={'Value': 'Y-Axis Label'})

        fig.update_yaxes(range=constant_y_range)

        st.plotly_chart(fig, use_container_width=True)
  



def calculate_average_changes(stock_data):
    # Calculate daily percentage change
    stock_data['Price Change'] = (stock_data['Close'] - stock_data['Open']) / stock_data['Open'] * 100

    # Separate data into days with positive and negative price changes
    positive_price_change = stock_data[stock_data['Close'] > stock_data['Open']]
    negative_price_change = stock_data[stock_data['Close'] < stock_data['Open']]

    # Calculate Average Price Up%
    average_price_up_percent = positive_price_change['Price Change'].mean()

    # Calculate Average Price Down%
    average_price_down_percent = negative_price_change['Price Change'].mean()

    st.write (f"Average Price Up%: {average_price_up_percent:.2f}%"), 
    st.write (f"Average Price Down%: {average_price_down_percent:.2f}%")

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
        if short_interest_data['Short Shares'] !="N/A":
           short_interest_data['Short Shares']= "{:,}".format(short_interest_data['Short Shares']) 
        if short_interest_data ['Short Float'] != "N/A":
           short_interest_data ['Short Float']=str(short_interest_data ['Short Float']*100)+"%"
           
        return short_interest_data

    except Exception as e:
        print(f"Error fetching short interest data for {stock_symbol}: {e}")
        return None
def format_large_number(number, percentage=False):
    """
    Format a large number into million (M) or billion (B) format,
    or format a decimal into percentage format.

    Args:
        number (int, float): The number to be formatted.
        percentage (bool): If True, format as a percentage.

    Returns:
        str: Formatted string.
    """
    if number =="N/A":
        return "N/A"
    if percentage:
        return f"{number * 100:.2f}%"
    elif abs(number) >= 1e9:
        return f"{number / 1e9:.2f}B"
    elif abs(number) >= 1e6:
        return f"{number / 1e6:.2f}M"
    else:
        return str(number) 
    


def display_stock_information(stock_symbol , current):
    try:
        # Create a Ticker object
        ticker = yf.Ticker(stock_symbol)
        # Fetch summary information
        info = ticker.info
        # Display the information in the sidebar
        st.sidebar.header("Stock Information")
        st.sidebar.write(f"Company Name: {info.get('longName', 'N/A')}")
        st.sidebar.write(f"Symbol: {info.get('symbol', 'N/A')}")
        st.sidebar.write(f"Sector: {info.get('sector', 'N/A')}")
        st.sidebar.write(f"Country: {info.get('country', 'N/A')}")
       
        st.sidebar.write(f"Market Cap: {format_large_number(info.get('marketCap', 'N/A'))}")
    
        st.sidebar.write(f"Current Price: {current}")
        st.sidebar.write(f"52-Week High: {info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.sidebar.write(f"52-Week Low: {info.get('fiftyTwoWeekLow', 'N/A')}")
        st.sidebar.write(f"Dividend Rate: {info.get('dividendRate', 'N/A')}")
        st.sidebar.write(f"Dividend Yield: {info.get('dividendYield', 'N/A')}")
        st.sidebar.write(f"EPS (Earnings Per Share): {info.get('trailingEps', 'N/A')}")
        st.sidebar.write(f"Short Ratio: {info.get('shortRatio', 'N/A')}")
        st.sidebar.write(f"Short Shares: {format_large_number(info.get('sharesShort', 'N/A'))}")
        st.sidebar.write(f"Short Percent: {format_large_number(info.get('shortPercentOfFloat', 'N/A'), percentage=True)}")
       
    except Exception as e:
        print(f"Error fetching stock information for {stock_symbol}: {e}")
        st.sidebar.write("Error fetching stock information. Please check the stock symbol.")
def analysis_last_week(stock_data,stock_symbol):
    st.write(stock_data )
    calculate_average_changes(stock_data)
   
    constant_y_range = ( stock_data['Low'].min(),stock_data['High'].max())
    # Create a line chart using plotly express
    fig = px.line(stock_data.reset_index(), x='Datetime', y=['Open', 'Close', 'High', 'Low'],
              title='last week stock prices ',
              labels={'Value': 'Y-Axis Label'},
              color_discrete_map={'Open': 'blue', 'Close': 'green', 'High': 'red', 'Low': 'orange'})
    
    fig.update_yaxes(range=constant_y_range)
    st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                            open=stock_data['Open'],
                                            high=stock_data['High'],
                                            low=stock_data['Low'],
                                            close=stock_data['Close'])])

        # Set chart title and labels
    fig.update_layout(title=f" Candlestick Chart last week",
                        xaxis_title="Date",
                        yaxis_title="Stock Price")
    st.plotly_chart(fig)

    stock_data_r=stock_data.reset_index()
   # Create subplots
    
    # Create scatter plot
    fig, axs = plt.subplots(1, 5, figsize=(20, 5))
    # High VS Low
    sns.scatterplot(x='High', y='Low', data=stock_data, ax=axs[0])
    axs[0].set_title("High VS Low")
    axs[0].set_xlabel("High")
    axs[0].set_ylabel("Low")

    # Open VS Close
    sns.scatterplot(x='Open', y='Close', data=stock_data, ax=axs[1])
    axs[1].set_title("Open VS Close")
    axs[1].set_xlabel("Open")
    axs[1].set_ylabel("Close")
    # High VS Close
    sns.scatterplot(x='High', y='Close', data=stock_data, ax=axs[2])
    axs[2].set_title("High VS Close")
    axs[2].set_xlabel("High")
    axs[2].set_ylabel("Close")

    # High VS Open
    sns.scatterplot(x='High', y='Open', data=stock_data, ax=axs[3])
    axs[3].set_title("High VS Open")
    axs[3].set_xlabel("High")
    axs[3].set_ylabel("Open")

    # Low VS Open
    sns.scatterplot(x='Low', y='Open', data=stock_data, ax=axs[4])
    axs[4].set_title("Low VS Open")
    axs[4].set_xlabel("Low")
    axs[4].set_ylabel("Open")

    # Display the plot in Streamlit
    st.pyplot(fig)

    fig, axs = plt.subplots(1, 5, figsize=(20, 5))

    # Plot histogram of Close Price
    axs[0].hist(stock_data['Close'], bins=20, color='skyblue', edgecolor='black')
    axs[0].set_title("Distribution of Close Price")
    axs[0].set_xlabel("Close Price")
    axs[0].set_ylabel("Frequency")

    # Plot histogram of Volume
    axs[1].hist(stock_data['Volume'], bins=20, color='salmon', edgecolor='black')
    axs[1].set_title("Distribution of Volume")
    axs[1].set_xlabel("Volume")
    axs[1].set_ylabel("Frequency")

    # Plot histogram of High Price
    axs[2].hist(stock_data['High'], bins=20, color='lightgreen', edgecolor='black')
    axs[2].set_title("Distribution of High Price")
    axs[2].set_xlabel("High Price")
    axs[2].set_ylabel("Frequency")
    
    # Plot histogram of low 
    axs[3].hist(stock_data['Low'], bins=20, color='lightgreen', edgecolor='black')
    axs[3].set_title("Plot histogram of low ")
    axs[3].set_xlabel("low  Price")
    axs[3].set_ylabel("Frequency")

    axs[4].hist(stock_data['Open'], bins=20, color='lightgreen', edgecolor='black')
    axs[4].set_title("Plot histogram of Open ")
    axs[4].set_xlabel("open  Price")
    axs[4].set_ylabel("Frequency")


    # Display the plot in Streamlit
    st.pyplot(fig)

    # Display summary statistics
    st.subheader("Summary Statistics for last weak ")
    st.write(stock_data.describe())
    short_interest_data = get_short_interest(stock_symbol)
    st.header("short interest data")
    if short_interest_data:
        st.table(short_interest_data)
    # Create Ticker object
    ticker = yf.Ticker(stock_symbol)
