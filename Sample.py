import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import webbrowser

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("C:\\Users\\keert\\Downloads\\nutrigen-3b09b-firebase-adminsdk-fbsvc-acb1f50bd0.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore Database
db = firestore.client()

# Custom CSS for styling
st.markdown(
        f"""
        <style>
        .header {{
            font-size:50px;
            text-align:center;
        }}
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

# User Session State
if "user" not in st.session_state:
    st.session_state.user = None

# Register User
def register():

    st.markdown("""
        <div class="title-container">
            <div class="nutrition-icon">🥗</div>
            <h1>Welcome to NutriGen</h1>
            <p>Your Personal Nutrition Assistant</p>
        </div>
    """, unsafe_allow_html=True)

    st.title("Create Your Account")

    fullname = st.text_input("Full Name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not (fullname and username and email and password and confirm_password):
            st.error("All fields are required!")
            return

        if password != confirm_password:
            st.error("Passwords do not match!")
            return

        try:
            # Create user in Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password,
                display_name=username
            )
            st.success("Registration successful! You can now log in.")

            # Store user details in Firestore
            db.collection("users").document(user.uid).set({
                "fullname": fullname,
                "username": username,
                "email": email
            })

            st.info("Now, please log in.")

            # Footer
            st.markdown(
                """
                <div class="footer">
                    <p>Already have an account? <a href="#">Login here</a></p>
                    <p>© 2024 NutriGen. All rights reserved.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error: {e}")

# Login User
def login():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not (email and password):
            st.error("Please enter both email and password.")
            return

        try:
            # Find user in Firestore by email
            user_query = db.collection("users").where("email", "==", email).stream()
            user_doc = next(user_query, None)

            if user_doc:
                st.session_state.user = user_doc.to_dict()
                st.success(f"Welcome back, {st.session_state.user['username']}!")
                webbrowser.open_new_tab("http://localhost:8501/stream")
            else:
                st.error("Invalid email or password.")
        except Exception as e:
            st.error(f"Error: {e}")
    
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

# Main Application Logic
if st.session_state.user:
    webbrowser.open_new_tab("http://localhost:8501/stream")
else:
    option = st.sidebar.selectbox("Choose an option", ["Login", "Register"])
    if option == "Register":
        register()
    else:
        login()
