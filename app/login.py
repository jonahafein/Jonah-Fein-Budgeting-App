import streamlit as st
import sys
import os

folder_path = os.path.abspath("/Users/jonahafein//Desktop/Python Projects/Jonah-Fein-Budgeting-App/backend")

if folder_path not in sys.path:
    sys.path.append(folder_path)

from db import Database

db = Database()

if "email" not in st.session_state:
    st.session_state.email = None
    st.session_state.user_id = None
    
email_input = st.text_input("Enter your email address")

if st.button("Start"):
    if email_input:
        user = db.get_user(email_input)
        if user:
            st.session_state.email = user["email"]
            st.session_state.user_id = user["user_id"]
            st.success("Welcome back!")
        else:
            db.insert_user(email_input)
            user = db.get_user(email_input)
            st.session_state.email = user["email"]
            st.session_state.user_id = user["user_id"]
            st.success("New account created!")
    else:
        st.warning("Please enter an email")
        
