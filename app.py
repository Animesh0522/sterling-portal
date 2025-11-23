import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURATION ---
FIRM_NAME = "Sterling & Stone CPA"
FIRM_TAGLINE = "Global Wealth Preservation & Strategic Tax Compliance"
PRIMARY_COLOR = "#0F172A" # Deep Navy (Slate 900)
ACCENT_COLOR = "#F59E0B"  # Amber/Gold

# --- PAGE SETUP ---
st.set_page_config(
    page_title=FIRM_NAME,
    page_icon="🛡️",
    layout="centered"
)

# --- CUSTOM CSS (THE "MILLION DOLLAR" LOOK) ---
# This injects CSS to override Streamlit's default look to match your premium brand
st.markdown(f"""
    <style>
    /* Main Background */
    .stApp {{
        background-color: #f8fafc;
    }}
    
    /* Header Styling */
    .main-header {{
        background-color: {PRIMARY_COLOR};
        padding: 2rem;
        border-bottom: 4px solid {ACCENT_COLOR};
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    /* Headings */
    h1, h2, h3 {{
        font-family: 'Source Serif Pro', serif;
        color: {PRIMARY_COLOR};
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {ACCENT_COLOR};
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        letter-spacing: 1px;
        border-radius: 2px;
    }}
    .stButton > button:hover {{
        background-color: #d97706; /* Darker Gold */
        color: white;
    }}

    /* Success Messages */
    .stSuccess {{
        background-color: #ecfdf5;
        color: #065f46;
        border-left: 5px solid #10b981;
    }}
    
    /* File Uploader */
    .stFileUploader section {{
        background-color: white;
        border: 1px dashed {PRIMARY_COLOR};
        padding: 2rem;
    }}
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION (SIMPLE SECURE LIST) ---
# In production, you would hide these in "Streamlit Secrets"
# Format: 'email': 'password'
CLIENT_DB = {
    "admin@sterling.cpa": "Admin@123",
    "client@vip.com": "Client@123"
}

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in CLIENT_DB and \
           st.session_state["password"] == CLIENT_DB[st.session_state["username"]]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs
        st.markdown(f"""
            <div style='text-align: center; margin-top: 50px;'>
                <h1 style='font-size: 3rem;'>🛡️</h1>
                <h2>{FIRM_NAME.upper()}</h2>
                <p>SECURE CLIENT ACCESS</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("Credentials"):
            st.text_input("Username (Email)", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Access Secure Vault", on_click=password_entered)
        
        # Demo Hint (Remove in production)
        st.info("Demo Login: client@vip.com / Client@123")
        return False
        
    elif not st.session_state["password_correct"]:
        # Password incorrect, show inputs + error
        st.markdown(f"<h2 style='text-align: center;'>{FIRM_NAME}</h2>", unsafe_allow_html=True)
        with st.form("Credentials"):
            st.text_input("Username (Email)", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Access Secure Vault", on_click=password_entered)
        st.error("😕 Credentials not recognized.")
        return False
        
    else:
        # Password correct
        return True

# --- MAIN APP LOGIC ---

if check_password():
    user_email = st.session_state["username"]
    
    # HEADER
    st.markdown(f"""
        <div class="main-header">
            <h1>{FIRM_NAME}</h1>
            <p>{FIRM_TAGLINE}</p>
            <small>Logged in as: {user_email}</small>
        </div>
    """, unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to", ["My Vault", "Firm Services", "Contact Principal"])
        
        st.markdown("---")
        if st.button("Log Out"):
            st.session_state["password_correct"] = False
            st.rerun()

    # PAGE: MY VAULT
    if page == "My Vault":
        st.subheader(f"📂 Secure Document Vault: {user_email}")
        st.warning("🔒 This connection is encrypted (TLS 1.3). Files are processed in memory.")

        uploaded_files = st.file_uploader(
            "Upload Tax Documents (PDF, XLSX, DOCX)", 
            accept_multiple_files=True
        )

        if uploaded_files:
            # --- YOUR FUTURE PYTHON AUTOMATION GOES HERE ---
            # This is where the magic happens. Because we are in Python,
            # you can run your scripts immediately.
            
            for uploaded_file in uploaded_files:
                # 1. LOGIC: File Renaming
                timestamp = datetime.now().strftime("%Y%m%d")
                clean_name = uploaded_file.name.replace(" ", "_")
                new_filename = f"{timestamp}_{user_email}_{clean_name}"
                
                # 2. LOGIC: Content Reading (Example Placeholder)
                # file_contents = uploaded_file.read() 
                # pdf_text = your_pdf_reader_function(file_contents)
                
                # 3. LOGIC: Save to OneDrive (Simulation)
                with st.spinner(f"Encrypting & Processing {uploaded_file.name}..."):
                    time.sleep(1.5) # Simulate processing time
                    
                    # In reality, here you would use the Microsoft Graph API to push `file_contents`
                    # directly to your OneDrive folder.
                    
                    st.success(f"✅ Successfully Processed & Saved as: **{new_filename}**")
                    
                    # Display "Simulated" Metadata that you would save to Excel
                    st.json({
                        "Original Name": uploaded_file.name,
                        "New System Name": new_filename,
                        "Size": f"{uploaded_file.size / 1024:.2f} KB",
                        "Status": "Sent to OneDrive Business"
                    })

    # PAGE: SERVICES
    elif page == "Firm Services":
        st.subheader("Our Expertise")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 🌐 International Tax
            Specialized reporting for FBAR, FATCA, and cross-border income streams.
            """)
            st.markdown("""
            ### ⚖️ IRS Representation
            Aggressive defense and negotiation for audits and dispute resolution.
            """)
        with col2:
            st.markdown("""
            ### 📈 Strategic Planning
            Proactive liability minimization strategies for corporations.
            """)
            st.markdown("""
            ### 🏛️ Trust & Estate
            Preserving family legacy through tax-efficient wealth transfer.
            """)

    # PAGE: CONTACT
    elif page == "Contact Principal":
        st.subheader("Direct Communication")
        with st.form("contact_form"):
            st.selectbox("Topic", ["Tax Question", "Appointment Request", "Urgent Notice"])
            st.text_area("Message (End-to-End Encrypted)")
            submitted = st.form_submit_button("Send Secure Message")
            if submitted:
                st.success("Message sent directly to Alexander Sterling's secure inbox.")
