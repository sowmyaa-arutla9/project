import streamlit as st
import google.generativeai as genai
import os

# Set your API key
genai.configure(api_key="AIzaSyCGhWxrlQ8S-fC_kWJmzU5kcaKH_h8olyE")

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

# Streamlit UI
st.title("💬 Google Gemini AI Chat")
st.write("Ask anything and get intelligent responses!")

# User input
user_input = st.text_input("Enter your question:")

# Process input and display output
if st.button("Get Response"):
    if user_input:
        try:
            response = model.generate_content(user_input)
            st.success(response.text)  # Display AI output
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question!")
