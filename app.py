import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURATION ---
FIRM_NAME = "Sterling & Stone CPA"
PRIMARY_COLOR = "#0F172A" # Deep Navy
ACCENT_COLOR = "#F59E0B"  # Gold

# --- PAGE SETUP ---
st.set_page_config(page_title=FIRM_NAME, page_icon="🛡️", layout="wide")

# --- AUTHENTICATION DATABASE ---
# This is where you control access.
CLIENT_DB = {
    "admin@sterling.cpa": "Admin@123",   # <--- THIS IS YOUR ADMIN LOGIN
    "client@vip.com": "Client@123"       # <--- THIS IS A CLIENT LOGIN
}

# --- SESSION STATE INITIALIZATION ---
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# --- CUSTOM CSS (PREMIUM LOOK) ---
st.markdown(f"""
    <style>
    .main {{ background-color: #f8fafc; }}
    .stButton > button {{
        background-color: {ACCENT_COLOR}; color: white; border: none;
        font-weight: bold; width: 100%; padding: 0.5rem;
    }}
    .auth-container {{
        background-color: white; padding: 3rem; border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        max-width: 400px; margin: auto; border-top: 5px solid {ACCENT_COLOR};
    }}
    .header-text {{ color: {PRIMARY_COLOR}; text-align: center; font-family: serif; }}
    </style>
""", unsafe_allow_html=True)

# --- FUNCTIONS ---

def login_user():
    st.markdown(f"""
        <div class="auth-container">
            <h1 class="header-text">🛡️</h1>
            <h2 class="header-text">{FIRM_NAME.upper()}</h2>
            <p style="text-align:center; color:gray;">SECURE CLIENT PORTAL</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Access Secure Vault")
            
            if submit:
                if email in CLIENT_DB and CLIENT_DB[email] == password:
                    st.session_state.user_email = email
                    if email == "admin@sterling.cpa":
                        st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid credentials.")
        
        # Demo Hint
        st.info("Try: admin@sterling.cpa / Admin@123")

def main_app():
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_email}")
        if st.session_state.is_admin:
            st.success("🔑 ADMIN MODE ACTIVE")
        
        if st.button("Log Out"):
            st.session_state.user_email = None
            st.session_state.is_admin = False
            st.rerun()
            
    # --- ADMIN VIEW ---
    if st.session_state.is_admin:
        st.title("🔐 Principal Dashboard")
        
        tab1, tab2 = st.tabs(["Client Files", "Manage Access"])
        
        with tab1:
            st.subheader("Incoming Client Documents")
            # This is where you would list files from OneDrive later
            st.info("No new documents pending review.")
            
            # Example of your Python Automation Trigger
            if st.button("Run Auto-Renaming Script"):
                with st.spinner("Scanning OneDrive..."):
                    time.sleep(2)
                    st.success("✅ 3 Files Renamed according to [Date]_[Client] format.")

        with tab2:
            st.subheader("Authorized Clients")
            st.json(CLIENT_DB)

    # --- CLIENT VIEW ---
    else:
        st.title(f"📂 Secure Vault")
        st.markdown("Upload your tax documents below. They will be automatically encrypted and synced to the firm's secure storage.")
        
        uploaded_files = st.file_uploader("Drag and drop files here", accept_multiple_files=True)
        
        if uploaded_files:
            for file in uploaded_files:
                # --- YOUR FUTURE PYTHON AUTOMATION GOES HERE ---
                with st.spinner(f"Encrypting {file.name}..."):
                    time.sleep(1)
                    st.success(f"✅ Sent to Firm Secure Storage: {file.name}")

# --- APP ROUTER ---
if st.session_state.user_email:
    main_app()
else:
    login_user()
