# tickets.py
import streamlit as st
import pandas as pd

# Page title
st.title("IT Tickets")

# Load tickets from CSV
# Make sure the path is correct relative to your main app
tickets_file = "DATA\it_tickets.csv"
try:
    df = pd.read_csv(tickets_file)
    
    # Display the dataframe
    st.dataframe(df)
except FileNotFoundError:
    st.error(f"File {tickets_file} not found.")
