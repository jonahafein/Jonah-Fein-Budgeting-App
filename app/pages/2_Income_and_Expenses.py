import streamlit as st
import pandas as pd
import sys
import os

folder_path = os.path.abspath("/Users/jonahafein//Desktop/Python Projects/Jonah-Fein-Budgeting-App/backend")

if folder_path not in sys.path:
    sys.path.append(folder_path)

from db import Database

if not st.session_state.get("email"):
    st.warning("Please log in first")
    st.stop()

# getting their user_id  
db = Database()
user = db.get_user(st.session_state.email)
if not user:
    st.error("User not found")
    st.stop()

user_id = user["user_id"]

if "loaded" not in st.session_state:
    pass
    # TODO: make these methods in db
    annual_income = db.get_income(user_id)["annual_income"]
    annual_bonus = db.get_income(user_id)["annual_bonus"]
    expenses_df = db.get_expenses(user_id)
    
    st.session_state.annual_income = annual_income if annual_income else 0
    st.session_state.annual_bonus = annual_bonus if annual_bonus else 0
    if expenses_df:
        st.session_state.expenses_df = pd.DataFrame([{
            "category": expense["category"],
            "amount": d["amount"]
        }for expense in expenses_df])
    
    st.session_state.loaded = True
    
st.title("Income and Expenses")

# initialize expenses_df if not there
if "expenses_df" not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame(columns = ["category", "amount"])
    
if st.session_state.email:
    email = st.session_state.email
    
    # now get all the user inputs: