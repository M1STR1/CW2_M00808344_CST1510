import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import altair as alt

# --- Page Guard ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access the dashboard.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(layout="wide", page_title="Dashboard")
st.title("📊 Dashboard")
st.success(f"Welcome, {st.session_state.get('username','')}!")

DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

@st.cache_data(ttl=30)
def load_table(table_name: str) -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

# Load available data (fallback to small synthetic datasets if DB absent)
incidents_df = load_table("cyber_incidents")
tickets_df = load_table("it_tickets")
datasets_df = load_table("datasets_metadata")

if incidents_df.empty:
    # synthetic sample incidents for charts
    dates = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="W")
    incidents_df = pd.DataFrame({
        "date": dates.astype(str),
        "incident_type": ["Phishing","Malware","Phishing","DDoS","Malware","Phishing","Insider","Phishing","Malware","DDoS","Phishing","SupplyChain"],
        "severity": ["High","Medium","High","Critical","Low","Medium","High","Low","Medium","High","Medium","High"],
        "status": ["Open","Closed","Investigating","Open","Resolved","Closed","Open","Closed","Investigating","Open","Resolved","Open"],
        "description": ["Sample incident"]*12,
        "reported_by": ["alice","bob","alice","carol","dave","alice","eve","bob","carol","alice","dave","eve"]
    })

# KPIs
total_threats = len(incidents_df)
open_tickets = int(tickets_df['status'].eq('Open').sum()) if not tickets_df.empty else 34
datasets_loaded = len(datasets_df) if not datasets_df.empty else 12

col1, col2, col3 = st.columns(3)
col1.metric("Threats Detected", total_threats, "+12")
col2.metric("Tickets Open", open_tickets, "-3")
col3.metric("Datasets Loaded", datasets_loaded, "+1")

st.markdown("---")

# Charts area
left, right = st.columns([2, 1])

with left:
    st.subheader("Incidents over time")
    # ensure date column exists and is datetime
    if "date" in incidents_df.columns:
        try:
            incidents_df["date_parsed"] = pd.to_datetime(incidents_df["date"], errors="coerce")
        except Exception:
            incidents_df["date_parsed"] = pd.to_datetime(incidents_df["date"].astype(str), errors="coerce")
        time_series = (incidents_df.dropna(subset=["date_parsed"])
                       .assign(week=lambda d: d["date_parsed"].dt.to_period("W").apply(lambda x: x.start_time))
                       .groupby("week")
                       .size()
                       .reset_index(name="count"))
        if not time_series.empty:
            line = alt.Chart(time_series).mark_area(opacity=0.4).encode(
                x=alt.X("week:T", title="Week"),
                y=alt.Y("count:Q", title="Incidents"),
                tooltip=["week:T","count:Q"]
            ).properties(height=300)
            st.altair_chart(line, use_container_width=True)
        else:
            st.info("Not enough date data to show trend.")
    else:
        st.info("No date column available in incidents data.")

    st.subheader("Incidents by severity")
    if "severity" in incidents_df.columns:
        sev_counts = incidents_df["severity"].fillna("Unknown").value_counts().reset_index()
        sev_counts.columns = ["severity", "count"]
        bar = alt.Chart(sev_counts).mark_bar().encode(
            x=alt.X("severity:N", sort='-y'),
            y="count:Q",
            color=alt.Color("severity:N", legend=None),
            tooltip=["severity","count"]
        ).properties(height=250)
        st.altair_chart(bar, use_container_width=True)
    else:
        st.info("No severity data available.")

    st.subheader("Recent incidents")
    st.dataframe(incidents_df.sort_values(by=incidents_df.columns[0], ascending=False).head(10), use_container_width=True)

with right:
    st.subheader("Tickets by status")
    if not tickets_df.empty and "status" in tickets_df.columns:
        status_counts = tickets_df["status"].fillna("Unknown").value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        pie = alt.Chart(status_counts).mark_arc().encode(
            theta=alt.Theta("count:Q"),
            color=alt.Color("status:N"),
            tooltip=["status","count"]
        ).properties(height=300)
        st.altair_chart(pie, use_container_width=True)
    else:
        # synthetic ticket breakdown
        sample = pd.DataFrame({"status":["Open","Investigating","Resolved","Closed"], "count":[34,10,20,15]})
        pie = alt.Chart(sample).mark_arc().encode(theta="count:Q", color="status:N", tooltip=["status","count"]).properties(height=300)
        st.altair_chart(pie, use_container_width=True)

    st.subheader("Datasets summary")
    if not datasets_df.empty and "dataset_name" in datasets_df.columns:
        ds = datasets_df.head(10)
        st.table(ds[["dataset_name","record_count","last_updated"]].fillna("-"))
    else:
        st.info("No datasets metadata found. Example:")
        st.table(pd.DataFrame({
            "dataset_name":["cyber_incidents","it_tickets","datasets_metadata"],
            "record_count":[total_threats, open_tickets, datasets_loaded]
        }))

st.markdown("---")
if st.button("Refresh"):
    st.experimental_rerun()

# Logout section
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("Home.py")
