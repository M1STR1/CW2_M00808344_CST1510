# datasets.py
import streamlit as st
import pandas as pd

# Page title
st.title("Datasets Metadata Viewer")

# Load datasets metadata from CSV
datasets_file = "DATA\datasets_metadata.csv"

try:
    df = pd.read_csv(datasets_file)
    
    # Display the dataframe
    st.dataframe(df)
    
    # Optional: allow filtering by a column, e.g., "category"
    if "category" in df.columns:
        category_filter = st.selectbox("Filter by category:", ["All"] + df["category"].unique().tolist())
        if category_filter != "All":
            filtered_df = df[df["category"] == category_filter]
            st.dataframe(filtered_df)
except FileNotFoundError:
    st.error(f"File {datasets_file} not found.")
