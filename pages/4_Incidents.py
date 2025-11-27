# incidents.py
import streamlit as st
import pandas as pd

# Page title
st.title("Incidents Viewer")

# Load incidents from CSV
incidents_file = "DATA\cyber_incidents.csv"

try:
    df = pd.read_csv(incidents_file)
    
    # Display the dataframe
    st.dataframe(df)
    
    # Optional: filter by a column, e.g., "severity"
    if "severity" in df.columns:
        severity_filter = st.selectbox("Filter by severity:", ["All"] + df["severity"].unique().tolist())
        if severity_filter != "All":
            filtered_df = df[df["severity"] == severity_filter]
            st.dataframe(filtered_df)
except FileNotFoundError:
    st.error(f"File {incidents_file} not found.")
