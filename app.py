import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns 
import plotly.graph_objects as go

from dividends import dividends

##################################### dividends #############################

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
        if short_interest_data['Short Shares'] !="N/A":
           short_interest_data['Short Shares']= "{:,}".format(short_interest_data['Short Shares']) 
        if short_interest_data ['Short Float'] != "N/A":
           short_interest_data ['Short Float']=str(short_interest_data ['Short Float']*100)+"%"
           
           


        return short_interest_data

    except Exception as e:
        print(f"Error fetching short interest data for {stock_symbol}: {e}")
        return None
    


def calculate_average_changes(stock_data):
    # Calculate the percentage change in closing prices
    stock_data['Price Change'] = stock_data['Close'].pct_change() * 100

    # Filter positive and negative percentage changes
    positive_changes = stock_data[stock_data['Price Change'] > 0]['Price Change']
    negative_changes = stock_data[stock_data['Price Change'] < 0]['Price Change']

    # Calculate the Average Price Up% and Average Price Down%
    average_price_up = positive_changes.mean()
    average_price_down = abs(negative_changes.mean())
    with right_column:
        st.write (f"Average Price Up%: {average_price_up:.2f}%"), 
        st.write (f"Average Price Down%: {average_price_down:.2f}%")
 

def display_stock_information(stock_symbol):
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
        st.sidebar.write(f"Market Cap: {info.get('marketCap', 'N/A')}")
        st.sidebar.write(f"Current Price: {info.get('regularMarketPrice', 'N/A')}")
        st.sidebar.write(f"52-Week High: {info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.sidebar.write(f"52-Week Low: {info.get('fiftyTwoWeekLow', 'N/A')}")
        st.sidebar.write(f"Dividend Rate: {info.get('dividendRate', 'N/A')}")
        st.sidebar.write(f"Dividend Yield: {info.get('dividendYield', 'N/A')}")
        st.sidebar.write(f"EPS (Earnings Per Share): {info.get('trailingEps', 'N/A')}")
        st.sidebar.write(f"Short Ratio: {info.get('shortRatio', 'N/A')}")
        st.sidebar.write(f"Short Shares: {info.get('sharesShort', 'N/A')}")
        st.sidebar.write(f"Short Percent: {info.get('shortPercentOfFloat', 'N/A')}")
    except Exception as e:
        print(f"Error fetching stock information for {stock_symbol}: {e}")
        st.sidebar.write("Error fetching stock information. Please check the stock symbol.")
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
    left_column, right_column = st.columns(2)
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date ,  interval="1m" ,prepost=True )
    stock_data=stock_data.asfreq('1T')
    stock_data=stock_data.fillna(method='ffill')
    stock_data=stock_data.between_time(start_time, end_time)
    display_stock_information(stock_symbol)
    
    
    with left_column:
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
       
    api_key = 'CD82V0YRBKXOVLXZ'
    


# Endpoint for quarterly earnings
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={stock_symbol}&apikey={api_key}'

# Make API request
    response = requests.get(url)
    earnings_data = response.json()

# Display earnings data
    st.write("Earnings Data:")
    st.write(earnings_data)

    
    

    
