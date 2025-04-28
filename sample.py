import streamlit as st
from web_functions import load_data
from Tabs import home, data, detect

# --- User Authentication Info ---
VALID_USERS = {
    "admin": "123",
    "user1": "pass1",
    
}

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title='Human Stress Detector',
    page_icon=':worried:',
    layout='wide',
    initial_sidebar_state='auto'
)

# --- Initialize Session States ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# --- Login Screen ---
if not st.session_state.logged_in:
    st.title("🔐 Login to Continue")

    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Login"):
        if username_input in VALID_USERS and VALID_USERS[username_input] == password_input:
            st.session_state.logged_in = True
            st.session_state.username = username_input
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.stop()

# --- Sidebar (Post-login) ---
st.sidebar.markdown(f"👤`{st.session_state.username}`")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Pages", ["Home", "Data Info", "Detection"])

# --- User Info + Logout ---
# st.sidebar.markdown(f"👤 **Logged in as:** `{st.session_state.username}`")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# --- Top-right Logo ---
col1, col2 = st.columns([10, 1])
with col2:
    st.image("data:image/jpeg;base64,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", width=50)

# --- Load Dataset ---
df, x, y = load_data()

# --- Page Routing ---
Tabs = {
    "Home": home,
    "Data Info": data,
    "Detection": detect,
}

if page == "Detection":
    Tabs[page].app(df, x, y)
elif page == "Data Info":
    Tabs[page].app(df)
else:
    Tabs[page].app()
