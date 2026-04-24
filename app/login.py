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
    st.session_state.birthdate = None
    
email_input = st.text_input("Enter your email")
birthdate = st.date_input("Enter your birthdate")

if st.button("Start"):
    if email_input:
        user = db.get_user(email_input)
        if user:
            db.update_birthdate(email_input, birthdate)
            st.session_state.email = user["email"]
            st.session_state.user_id = user["user_id"]
            st.session_state.birthdate = birthdate
            st.success("Welcome back!")
        else:
            db.insert_user(email_input, birthdate)
            user = db.get_user(email_input)
            st.session_state.email = user["email"]
            st.session_state.user_id = user["user_id"]
            st.success("New account created!")
    else:
        st.warning("Please enter an email")
        
