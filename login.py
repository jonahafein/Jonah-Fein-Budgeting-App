import streamlit as st

if "email" not in st.session_state:
    st.session_state.email = None
    
email_input = st.text_input("Enter your email address")

if st.button("Start"):
    if email_input:
        st.session_state.email = email_input
    else:
        st.warning("Please enter an email")