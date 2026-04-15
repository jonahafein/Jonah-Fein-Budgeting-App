import streamlit as st
import sys
import os

folder_path = os.path.abspath("/Users/jonahafein//Desktop/Python Projects/Jonah-Fein-Budgeting-App/backend")

if folder_path not in sys.path:
    sys.path.append(folder_path)

from db import Database

if "email" not in st.session_state:
    st.session_state.email = None
    
email_input = st.text_input("Enter your email address")

if st.button("Start"):
    if email_input:
        st.session_state.email = email_input
        conn = Database.get_conn()
        cursor = conn.cursor()
        number = cursor.execute("SELECT COUNT(*) FROM users WHERE user_email = ?", email_input)
        cursor.close()
        conn.close()
        if number == 0:
            Database().insert_user(email_input)
        else:
            Database().get_user(email_input)
    else:
        st.warning("Please enter an email")
        
