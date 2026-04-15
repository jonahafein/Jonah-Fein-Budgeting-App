import streamlit as st

if not st.session_state.get("email"):
    st.warning("Please log in first")
    st.stop()

st.title("This is where all income and expenses will be logged")