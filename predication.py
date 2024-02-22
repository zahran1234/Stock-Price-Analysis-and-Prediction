import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM , Dropout
import streamlit as st

def train_and_predication(stock_symbol):
    time_steps=100
    # Get the number of historical data days
    ticker = yf.Ticker(stock_symbol)
    num_historical_days = len(ticker.history(period='max'))
    
    if 3000> num_historical_days:
        data = ticker.history(period=str(num_historical_days)+"d", actions=True)
    else:
        data = ticker.history(period='7000d', actions=True)
    # Select the specified features for prediction
    features=[ 'Close']
    dataset = data[features].values
    from sklearn.preprocessing import MinMaxScaler

    x_train=[]
    y_train = []
    for i in  range(0 ,len(dataset)-(time_steps+1)):
        x_train.append(dataset[i:i+time_steps])
        y_train.append(dataset[i+time_steps][0])
    x_train=np.array(x_train)
    y_train=np.array(y_train)
        # Build LSTM model
    model=Sequential()
    model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
    model.add(LSTM(50,return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error',optimizer='adam')
    # Train the model
    st.write(" waiting for model traing ")
    model.fit(x_train, y_train, batch_size=64, epochs=100)
    ticker = yf.Ticker(stock_symbol)
    last_days=data = ticker.history(period='100d', actions=True)
    last_days=last_days[features].values
    last_days=last_days.reshape(1, 100, -1)
    return model.predict(last_days)[0]