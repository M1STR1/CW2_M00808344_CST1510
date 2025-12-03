import streamlit as st
from app.data.db import init_db
from app.services.auth import register_user, login_user

st.set_page_config(page_title="Login", layout="wide")

# --------------------------
# INITIALISE DATABASE
# --------------------------
init_db()

if "db_init_done" not in st.session_state:
    st.session_state.db_init_done = True

# --------------------------
# SESSION STATE DEFAULTS
# --------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = "user"

# --------------------------
# LOGIN / REGISTER TABS
# --------------------------
tab_login, tab_register = st.tabs(["Login", "Register"])


# ==========================================
#                LOGIN TAB
# ==========================================
with tab_login:
    st.header("Login")

    user = st.text_input("Username", key="login_user")
    pw = st.text_input("Password", type="password", key="login_pw")

    if st.button("Log in"):
        ok, role = login_user(user, pw)

        if ok:
            st.success("Login successful!")
            st.balloons()  # SHOW BALLOONS FIRST

            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.role = role

            st.switch_page("pages/1_Dashboard.py")

        else:
            st.error("Invalid username or password.")

# ==========================================
#             REGISTER TAB
# ==========================================
with tab_register:
    st.header("Create Account")

    new_user = st.text_input("New Username", key="reg_user")
    new_pw = st.text_input("New Password", type="password", key="reg_pw")
    confirm_pw = st.text_input("Confirm Password", type="password", key="reg_confirm")

    role_choice = st.selectbox(
        "Select Role",
        ["user", "admin"],
        key="reg_role"
    )

    if st.button("Register"):
        if not new_user or not new_pw:
            st.warning("Please enter a username and password.")
        elif new_pw != confirm_pw:
            st.error("Passwords do not match.")
        else:
            created = register_user(new_user, new_pw, role_choice)

            if created:
                st.success("Account created! You can now log in.")
            else:
                st.error("Username already exists.")
