import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import re

class UserAuth:
    def _init_(self):
        self.conn = sqlite3.connect('nutrigen.db')
        self.create_user_table()
        
    def create_user_table(self):
        query = '''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            name TEXT,
            dietary_preferences TEXT,
            health_conditions TEXT,
            activity_level TEXT,
            allergens TEXT,
            last_login DATETIME
        )'''
        self.conn.execute(query)
        self.conn.commit()
    
    def verify_credentials(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                      (username, hashed_password))
        user_data = cursor.fetchone()
        if user_data:
            cursor.execute("UPDATE users SET last_login=? WHERE username=?", 
                         (datetime.now(), username))
            self.conn.commit()
        return user_data

def main():
    st.set_page_config(
        page_title="NutriGen Login",
        page_icon="🥗",
        layout="wide"
    )
    
    # Using a light background color with subtle fruit pattern
    st.markdown("""
        <style>
        .stApp {
            background-color: #f5f9f5;  /* Light mint green background */
            background-image: url('https://images.unsplash.com/photo-1512621776951-a57141f2eefd');
            background-repeat: no-repeat;
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
            background-blend-mode: overlay;
            opacity: 1;
        }
        .login-container {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin: auto;
            max-width: 500px;
        }
        .app-title {
            color: #2E8B57;
            text-align: center;
            padding: 20px;
            margin-bottom: 30px;
            font-weight: bold;
        }
        .stButton button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize authentication
    auth = UserAuth()
    
    # App title
    st.markdown("<h1 class='app-title'>NutriGen</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='app-title'>Your AI-Powered Nutrition Assistant</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        st.subheader("Welcome Back! 👋")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            col_left, col_right = st.columns(2)
            
            with col_left:
                remember_me = st.checkbox("Remember me")
            with col_right:
                st.markdown("<div style='text-align: right;'><a href='#'>Forgot password?</a></div>", unsafe_allow_html=True)
            
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if not username or not password:
                    st.error("Please fill in all fields")
                else:
                    user_data = auth.verify_credentials(username, password)
                    if user_data:
                        st.session_state.user = {
                            'username': user_data[0],
                            'email': user_data[2],
                            'name': user_data[3],
                            'dietary_preferences': user_data[4],
                            'health_conditions': user_data[5],
                            'activity_level': user_data[6],
                            'allergens': user_data[7]
                        }
                        st.session_state.logged_in = True
                        
                        st.success("Login successful!")
                        st.balloons()
                        
                        st.markdown("Redirecting to dashboard...")
                        st.experimental_rerun()
                    else:
                        st.error("Invalid username or password")
        
        st.markdown("<div style='text-align: center; padding: 20px;'>Don't have an account? <a href='#'>Register here</a></div>", unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Why NutriGen?")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                - 🎯 Personalized meal plans
                - 🥗 Detailed nutrition info
                - 📊 Progress tracking
            """)
        with col2:
            st.markdown("""
                - 🛒 Smart grocery lists
                - 🔍 AI-powered recommendations
                - 📱 Easy to use interface
            """)
        
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()