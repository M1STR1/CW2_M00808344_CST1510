import streamlit as st

st.set_page_config(page_title="Login", layout="wide")

# --- Session state setup ---
if "users" not in st.session_state:
    st.session_state.users = {}  # For coursework demo only

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# --- Tabs for login/register ---
tab_login, tab_register = st.tabs(["Login", "Register"])

# =====================
# LOGIN TAB
# =====================
with tab_login:
    st.header("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        users = st.session_state.users
        if login_username in users and users[login_username] == login_password:
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success("Login successful!")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Invalid username or password")


# =====================
# REGISTER TAB
# =====================
with tab_register:
    st.header("Create Account")

    new_username = st.text_input("Create username", key="new_user")
    new_password = st.text_input("Create password", type="password", key="new_pass")
    confirm_password = st.text_input("Confirm password", type="password", key="confirm_pass")

    if st.button("Register"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in st.session_state.users:
            st.error("Username already taken.")
        else:
            st.session_state.users[new_username] = new_password
            st.success("Account created! Go to Login tab.")
