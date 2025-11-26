import streamlit as st
import pandas as pd

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access analytics.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

st.title("📈 Domain Analytics")

domain = st.selectbox("Choose domain", ["Cybersecurity", "Data Science", "IT Operations"])

st.divider()

# --- CYBERSECURITY ---
if domain == "Cybersecurity":
    st.subheader("Cybersecurity Threat Trends")
    threats = {"Malware": 89, "Phishing": 67, "DDoS": 45, "Intrusion": 46}
    df = pd.DataFrame(threats, index=[0])
    st.bar_chart(df)

# --- DATA SCIENCE ---
elif domain == "Data Science":
    st.subheader("Model Training Metrics")
    history = pd.DataFrame({
        "epoch": [1, 2, 3, 4, 5],
        "loss": [0.45, 0.32, 0.24, 0.18, 0.15],
        "accuracy": [0.78, 0.85, 0.89, 0.92, 0.94]
    })
    st.line_chart(history, x="epoch", y=["loss", "accuracy"])

# --- IT OPERATIONS ---
else:
    st.subheader("CPU & Memory Usage")
    usage = pd.DataFrame({
        "time": ["00:00", "06:00", "12:00", "18:00", "23:59"],
        "CPU": [45, 52, 78, 82, 67],
        "Memory": [6.2, 6.8, 8.5, 9.1, 8.2]
    })
    st.line_chart(usage, x="time")
