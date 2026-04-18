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
    income = db.get_income(user_id)
    annual_income = income["annual_income"]
    annual_bonus = income["annual_bonus"]
    expenses_df = db.get_expenses(user_id)
    
    st.session_state.annual_income = annual_income if annual_income else 0
    st.session_state.annual_bonus = annual_bonus if annual_bonus else 0
    if expenses_df:
        st.session_state.expenses_df = pd.DataFrame([{
            "category": expense["category"],
            "amount": expense["amount"]
        }for expense in expenses_df])
    
    st.session_state.loaded = True
    
st.title("Income and Expenses")

# initialize expenses_df if not there
if "expenses_df" not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame(columns = ["category", "amount"])
    
if st.session_state.email:
    email = st.session_state.email
    
    # now get all the user inputs:
    annual_income = st.number_input("What is your annual base income?", value = st.session_state.annual_income)
    annual_bonus = st.number_input("What is your expected annual bonus?", value = st.session_state.annual_bonus)
    
    st.write("List all of monthly expenses:")
    if 'debt_df' not in st.session_state:
        st.session_state.expenses_df = pd.DataFrame(columns = ["category", "amount"])
    
    col1,col2 = st.columns(2)
    with col1:
        category = st.text_input("Enter expense category:")
    with col2:
        amount = st.number_input("Enter expense amount", key = "amount")
        
    if st.button("Add Expense"):
        if category:
            st.session_state.expense_df.loc[len(st.session_state.expense_df)] = [category, amount]
        else:
            st.warning("Please enter an expense")
            
    st.write("### Expenses:", st.session_state.expense_df)
    if st.button("Save Income and Expenses"):
        st.session_state.profile = {
            "email": email,
            "annual_income": annual_income,
            "annual_bonus": annual_bonus,
            "expense_df": st.session_state.expense_df if not st.session_state.expense_df.empty else None
        }
        # TODO: make the update methods
        db = Database()
        user_id = db.get_user(email)["user_id"]
        db.update_income(user_id, annual_income, annual_bonus)
        db.update_expenses(user_id, st.session_state.expense_df)
        st.success("Income and Expenses Saved!")
