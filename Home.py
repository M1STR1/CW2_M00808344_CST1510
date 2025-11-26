import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'Column A': [1, 2, 3, 4],
    'Column B': ['A', 'B', 'C', 'D']
})

st.set_page_config(
    page_title="My app",
    page_icon=":shark:",
    layout="wide"
)

st.title("📊 Sales Dashboard")
with st.sidebar:
    st.title("Controls")
    st.write("Choose")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Left")
    st.bar_chart(df['Column A'])

with col2:
    st.subheader("Right")
    st.line_chart(df['Column A'])

with st.expander("See details"):
    st.write("Hidden content")
    st.dataframe(df)
