import streamlit as st
import sys
import os
import datetime 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from backend.db import Database

db = Database()

if "email" not in st.session_state:
    st.session_state.email = None
    st.session_state.user_id = None
    st.session_state.birthdate = None
    
email_input = st.text_input("Enter your email")
birthdate = st.date_input("Enter your birthdate", min_value=datetime.date(1900, 1, 1))

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
        
