import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Create a sample DataFrame with timestamps in minutes
data = {'Timestamp': pd.date_range('2022-01-01', periods=100, freq='T'),  # 'T' stands for minutes
        'Value': np.random.randn(100).cumsum()}
df = pd.DataFrame(data)

# Define a constant y-axis range
constant_y_range = (-10, 10)

# Create a line chart using plotly express
fig = px.line(df, x='Timestamp', y='Value', title='Line Chart with Constant Y-Axis Range', labels={'Value': 'Y-Axis Label'})

# Customize y-axis range
fig.update_yaxes(range=constant_y_range)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
