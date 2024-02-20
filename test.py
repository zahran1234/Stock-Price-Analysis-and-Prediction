import streamlit as st

# Streamlit app title
st.title("Right Side Content Example")

# Create a layout with two columns
left_column, right_column = st.columns(2)

# Write content in the right column
with right_column:
    st.header("Right Side Header")
    st.write("This is content on the right side of the app.")

# Write content in the left column
with left_column:
    st.header("Left Side Header")
    st.write("This is content on the left side of the app.")

# You can add more content in each column as needed
