import streamlit as st
from app.data.db import init_db
from app.services.auth import register_user, login_user


st.set_page_config(page_title="Login", layout="wide")


# initialize DB (creates tables if missing)
init_db()


if "db_init_done" not in st.session_state:
    st.session_state.db_init_done = True


# Session state defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = "user"


tab_login, tab_register = st.tabs(["Login", "Register"])


with tab_login:
    st.header("Login")
    user = st.text_input("Username", key="login_user")
    pw = st.text_input("Password", type="password", key="login_pw")
    if st.button("Log in"):
        ok, role = login_user(user, pw)
        if ok:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_st
