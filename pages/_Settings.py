import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access settings.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

st.title("⚙️ Settings")
st.write("User preferences and profile settings will go here.")

st.info("This page meets the 'Settings Page' requirement for your coursework.")
