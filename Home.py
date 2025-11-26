import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3

DATA_DIR = Path("DATA")             # put CSV/DB here
DATA_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="My app", page_icon=":shark:", layout="wide")
st.title("📊 Sales Dashboard")

# Cached data loader (use st.cache_data; older streamlit use st.cache)
@st.cache_data(ttl=300)
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

@st.cache_data(ttl=300)
def load_db_table(db_path: str, table: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

with st.sidebar:
    st.title("Controls")
    # Option 1: select a CSV from DATA folder
    csv_files = ["--"] + [str(p.name) for p in DATA_DIR.glob("*.csv")]
    chosen_csv = st.selectbox("Choose CSV (DATA folder)", csv_files)

    # Option 2: upload a file (one-time)
    uploaded = st.file_uploader("Upload CSV", type=["csv"])

    # Option 3: load from sqlite table if exists
    db_path = str(DATA_DIR / "intelligence_platform.db")
    use_db = st.checkbox("Load from DB (cyber_incidents)", value=False)

    # Refresh button
    if st.button("Refresh"):
        st.experimental_rerun()

# Decide which source to use
df = pd.DataFrame()
if uploaded is not None:
    df = pd.read_csv(uploaded)
elif chosen_csv != "--":
    df = load_csv(str(DATA_DIR / chosen_csv))
elif use_db and Path(db_path).exists():
    df = load_db_table(db_path, "cyber_incidents")
else:
    # fallback: sample dataframe
    df = pd.DataFrame({'Column A': [1, 2, 3, 4], 'Column B': ['A', 'B', 'C', 'D']})

# show dataframe and simple filters
st.subheader("Data Table")
st.dataframe(df)

# Provide quick filters based on available columns
if not df.empty:
    st.subheader("Filters")
    cols = df.columns.tolist()
    col_filter = st.selectbox("Filter column", ["--"] + cols)
    if col_filter != "--":
        unique = list(df[col_filter].dropna().unique()[:50])
        selected = st.multiselect(f"Select values from {col_filter}", unique, default=unique[:5])
        if selected:
            df = df[df[col_filter].isin(selected)]
        st.dataframe(df)

# charts
col1, col2 = st.columns(2)
with col1:
    st.subheader("Bar Chart (numeric)")
    # pick first numeric column for simple chart
    numeric_cols = df.select_dtypes("number").columns.tolist()
    if numeric_cols:
        st.bar_chart(df[numeric_cols[0]])
    else:
        st.info("No numeric columns for bar chart")

with col2:
    st.subheader("Line Chart")
    if numeric_cols:
        st.line_chart(df[numeric_cols[0]])
    else:
        st.info("No numeric columns for line chart")

with st.expander("See details"):
    st.write("Hidden content")
    st.dataframe(df)
