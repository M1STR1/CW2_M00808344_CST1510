import streamlit as st

# --- Page Guard ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access the dashboard.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(layout="wide")
st.title("📊 Dashboard")
st.success(f"Welcome, {st.session_state.username}!")

# Example dashboard metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Threats Detected", 247, "+12")

with col2:
    st.metric("Tickets Open", 34, "-3")

with col3:
    st.metric("Datasets Loaded", 12, "+1")

# Logout section
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("Home.py")
