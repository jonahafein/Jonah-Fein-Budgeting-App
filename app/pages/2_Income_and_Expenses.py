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

if "income_loaded" not in st.session_state:
    pass
    # TODO: make these methods in db
    income = db.get_income(user_id)
    annual_income = income["annual_income"] if income else 0
    annual_bonus = income["annual_bonus"] if income else 0
    state_tax_perc = income["state_tax_perc"] if income else 0
    local_tax_perc = income["local_tax_perc"] if income else 0
    marriage_status = income["marriage_status"] if income else "single"
    employer_match = income["employer_match"] if income else 0
    expenses_df = db.get_expenses(user_id)
    
    st.session_state.annual_income = annual_income if annual_income else 0
    st.session_state.annual_bonus = annual_bonus if annual_bonus else 0
    st.session_state.state_tax_perc = state_tax_perc if state_tax_perc else 0
    st.session_state.local_tax_perc = local_tax_perc if local_tax_perc else 0
    st.session_state.marriage_status = marriage_status if marriage_status else "single"
    st.session_state.employer_match = employer_match if employer_match else 0
    if expenses_df:
        st.session_state.expenses_df = pd.DataFrame([{
            "category": expense["category"],
            "amount": expense["amount"]
        }for expense in expenses_df])
    
    st.session_state.income_loaded = True

if "expenses_df" not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame(columns = ["category", "amount"])
    
st.title("Income and Expenses")

# initialize expenses_df if not there
if "expenses_df" not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame(columns = ["category", "amount"])
    
if st.session_state.email:
    email = st.session_state.email
    
    # now get all the user inputs:
    annual_income = st.number_input("What is your annual base income?", value = float(st.session_state.annual_income))
    st.session_state.annual_income = annual_income
    annual_bonus = st.number_input("What is your expected annual bonus?", value = float(st.session_state.annual_bonus))
    st.session_state.annual_bonus = annual_bonus
    state_tax_perc = st.number_input("What is your state income tax %?", value = float(st.session_state.state_tax_perc))
    st.session_state.state_tax_perc = state_tax_perc
    local_tax_perc = st.number_input("What is your local income tax %?", value = float(st.session_state.local_tax_perc))
    st.session_state.local_tax_perc = local_tax_perc
    marriage_status = st.radio("What is your marriage status?", ["single", "married"])
    st.session_state.marriage_status = marriage_status
    employer_match = st.number_input("What dollar amount will your employer match you for your 401k?", value = float(st.session_state.employer_match))
    st.session_state.employer_match = employer_match
    
    st.write("Please all of your monthly expenses. Include rent/mortgage, property taxes, debt minimum payments, and all other required expenses. You may also include fun spending or any other category that you will allocate as an expense.")
    if 'expenses_df' not in st.session_state:
        st.session_state.expenses_df = pd.DataFrame(columns = ["category", "amount"])
    
    col1,col2 = st.columns(2)
    with col1:
        category = st.text_input("Enter expense category:", key = "category")
    with col2:
        amount = st.number_input("Enter expense amount", key = "amount")
        
    if st.button("Add Expense"):
        if category:
            st.session_state.expenses_df.loc[len(st.session_state.expenses_df)] = [category, amount]
        else:
            st.warning("Please enter an expense")
            
    st.write("### Monthly Expenses:", st.session_state.expenses_df)
    if st.button("Save Income and Expenses"):
        st.session_state.profile = {
            "email": email,
            "annual_income": annual_income,
            "annual_bonus": annual_bonus,
            "state_tax_perc": state_tax_perc,
            "local_tax_perc": local_tax_perc,
            "marriage_status": marriage_status,
            "employer_match": employer_match,
            "expenses_df": st.session_state.expenses_df if not st.session_state.expenses_df.empty else None
        }
        # TODO: make the update methods
        db = Database()
        user_id = db.get_user(email)["user_id"]
        db.update_income(user_id, annual_income, annual_bonus, state_tax_perc, local_tax_perc, marriage_status, employer_match)
        db.update_expenses(user_id, st.session_state.expenses_df)
        st.success("Income and Expenses Saved!")
