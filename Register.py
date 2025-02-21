import streamlit as st
import sqlite3
import hashlib
import re
from datetime import datetime
import base64
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase (Add the path to your private key JSON)
if not firebase_admin._apps:
    cred = credentials.Certificate("C:\\Users\\keert\\Downloads\\nutrigen-3b09b-firebase-adminsdk-fbsvc-acb1f50bd0.json")
    firebase_admin.initialize_app(cred)
    
db = firestore.client()  # Initialize Firestore Database

# User Session State
if "user" not in st.session_state:
    st.session_state.user = None

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Username validation
def is_valid_username(username):
    pattern = r'^[a-zA-Z0-9_]{4,20}$'
    return re.match(pattern, username) is not None

# Check if username or email exists
def check_existing_user(username, email):
    conn = sqlite3.connect('nutrigen_users.db')
    c = conn.cursor()
    
    c.execute("SELECT username FROM users WHERE username = ?", (username,))
    existing_username = c.fetchone()
    
    c.execute("SELECT email FROM users WHERE email = ?", (email,))
    existing_email = c.fetchone()
    
    conn.close()
    
    return existing_username, existing_email

# Register user
def register_user(full_name, username, email, password):
    conn = sqlite3.connect('nutrigen_users.db')
    c = conn.cursor()
    
    try:
        c.execute("""
            INSERT INTO users (full_name, username, email, password)
            VALUES (?, ?, ?, ?)
        """, (full_name, username, email, hash_password(password)))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
    
    return success

def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: rgba(255, 255, 255, 0.85);
            background-blend-mode: overlay;
        }}
        
        [data-testid="stAppViewContainer"] {{
            background: transparent;
        }}
        
        [data-testid="stHeader"] {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
        }}
        
        [data-testid="stToolbar"] {{
            right: 2rem;
        }}
        
        .main {{
            background: transparent !important;
        }}
        
        .registration-container {{
            background-color: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(5px);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            margin: 2rem auto;
            max-width: 600px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .title-container {{
            text-align: center;
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.9), rgba(39, 174, 96, 0.9));
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .title-container h1 {{
            color: white;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .title-container p {{
            color: white;
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .stButton button {{
            background: linear-gradient(90deg, #2ecc71, #27ae60);
            border: none;
            color: white;
            font-weight: bold;
            padding: 0.75rem 1.5rem;
            border-radius: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 1rem;
        }}
        
        .stButton button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        
        .stTextInput input {{
            border-radius: 8px;
            border: 1px solid rgba(46, 204, 113, 0.3);
            padding: 0.75rem;
            transition: all 0.3s ease;
            background-color: rgba(255, 255, 255, 0.9);
        }}
        
        .stTextInput input:focus {{
            border-color: #2ecc71;
            box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.2);
        }}
        
        .nutrition-icon {{
            font-size: 48px;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .success-msg {{
            color: #2ecc71;
            padding: 1rem;
            border-radius: 8px;
            background-color: rgba(46, 204, 113, 0.1);
            margin: 1rem 0;
        }}
        
        .error-msg {{
            color: #e74c3c;
            padding: 1rem;
            border-radius: 8px;
            background-color: rgba(231, 76, 60, 0.1);
            margin: 1rem 0;
        }}
        
        .footer {{
            text-align: center;
            background: rgba(255, 255, 255, 0.92);
            padding: 1.5rem;
            border-radius: 15px;
            margin-top: 2rem;
            backdrop-filter: blur(5px);
        }}
        
        .footer a {{
            color: #2ecc71;
            text-decoration: none;
            font-weight: bold;
            transition: color 0.3s ease;
        }}
        
        .footer a:hover {{
            color: #27ae60;
            text-decoration: underline;
        }}
        
        /* Custom divider */
        .divider {{
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(46, 204, 113, 0.3), transparent);
            margin: 1.5rem 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(
        page_title="NutriGen Registration",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Add custom background and styling
    set_background()
    
    # Title section
    st.markdown("""
        <div class="title-container">
            <div class="nutrition-icon">🥗</div>
            <h1>Welcome to NutriGen</h1>
            <p>Your Personal Nutrition Assistant</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Registration Form Container
    st.markdown('<div class="registration-container">', unsafe_allow_html=True)
    
    with st.form("registration_form"):
        st.subheader("Create Your Account")
        
        full_name = st.text_input("Full Name")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        submit_button = st.form_submit_button("Join NutriGen")
        
        if submit_button:
            # Validation
            if not all([full_name, username, email, password, confirm_password]):
                st.markdown('<div class="error-msg">Please fill in all fields.</div>', unsafe_allow_html=True)
            elif not is_valid_username(username):
                st.markdown('<div class="error-msg">Username must be 4-20 characters long and contain only letters, numbers, and underscores.</div>', unsafe_allow_html=True)
            elif not is_valid_email(email):
                st.markdown('<div class="error-msg">Please enter a valid email address.</div>', unsafe_allow_html=True)
            elif len(password) < 8:
                st.markdown('<div class="error-msg">Password must be at least 8 characters long.</div>', unsafe_allow_html=True)
            elif password != confirm_password:
                st.markdown('<div class="error-msg">Passwords do not match.</div>', unsafe_allow_html=True)
            else:
                # Check for existing username/email
                existing_username, existing_email = check_existing_user(username, email)
                
                if existing_username:
                    st.markdown('<div class="error-msg">Username already exists. Please choose another one.</div>', unsafe_allow_html=True)
                elif existing_email:
                    st.markdown('<div class="error-msg">Email already registered. Please use another email address.</div>', unsafe_allow_html=True)
                else:
                    # Register the user
                    if register_user(full_name, username, email, password):
                        st.markdown('<div class="success-msg">Registration successful! You can now log in.</div>', unsafe_allow_html=True)
                        # Clear form (requires page rerun)
                        st.experimental_rerun()
                    else:
                        st.markdown('<div class="error-msg">An error occurred during registration. Please try again.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>Already have an account? <a href="#">Login here</a></p>
            <p>© 2024 NutriGen. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()