import streamlit as st 

if not st.session_state.get("email"):
    st.warning("Please log in first")
    st.stop()

st.title("Account Dashboard")

st.write("Account insights for", st.session_state.email, ":")

