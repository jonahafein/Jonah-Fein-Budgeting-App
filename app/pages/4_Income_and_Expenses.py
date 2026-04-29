import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.db import Database

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
    months_worked = income["months_worked"] if income else 12
    expenses_df = db.get_expenses(user_id)
    
    st.session_state.annual_income = annual_income if annual_income else 0
    st.session_state.annual_bonus = annual_bonus if annual_bonus else 0
    st.session_state.state_tax_perc = state_tax_perc if state_tax_perc else 0
    st.session_state.local_tax_perc = local_tax_perc if local_tax_perc else 0
    st.session_state.marriage_status = marriage_status if marriage_status else "single"
    st.session_state.months_worked = months_worked if months_worked else 12
    if expenses_df:
        st.session_state.expenses_df = pd.DataFrame([{
            "category": expense["category"],
            "amount": expense["amount"]
        }for expense in expenses_df])
    
    st.session_state.income_loaded = True

if "expenses_df" not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame(columns = ["category", "amount", "Delete"])
    
st.title("Income and Expenses")
st.write("Make sure to save any changes made.")

# initialize expenses_df if not there
if "expenses_df" not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame(columns = ["category", "amount"])
    
if st.session_state.email:
    email = st.session_state.email
    
    # now get all the user inputs:
    annual_income = st.number_input("What is your annual base income?", value = float(st.session_state.annual_income))
    st.session_state.annual_income = annual_income
    months_worked = st.slider("How many months will you work this calendar year?", 1, 12, int(st.session_state.months_worked))
    st.session_state.months_worked = months_worked
    annual_bonus = st.number_input("What is your expected annual bonus this calendar year? (do not include if you start work mid year and will get a bonus next calendar year). If you don't know, you can wait until you get your bonus to add.", value = float(st.session_state.annual_bonus))
    st.session_state.annual_bonus = annual_bonus
    state_tax_perc = st.number_input("What is your state income tax %?", value = float(st.session_state.state_tax_perc))
    st.session_state.state_tax_perc = state_tax_perc
    local_tax_perc = st.number_input("What is your local income tax %?", value = float(st.session_state.local_tax_perc))
    st.session_state.local_tax_perc = local_tax_perc
    marriage_status = st.radio("What is your marriage status?", ["single", "married"])
    st.session_state.marriage_status = marriage_status
    
    st.write("Please list all of your monthly expenses. Include (if applicable) rent/mortgage, property taxes, debt minimum payments, and all other required monthly expenses. Additionally, include any want related spending (i.e., non necessities) that you plan to spend money on.")
    if 'expenses_df' not in st.session_state:
        st.session_state.expenses_df = pd.DataFrame(columns = ["category", "amount"])
    
    col1,col2 = st.columns(2)
    with col1:
        category = st.text_input("Enter expense category:", key = "category")
    with col2:
        amount = st.number_input("Enter expense amount", key = "amount")
        
    if st.button("Add Expense"):
        if category:
            st.session_state.expenses_df.loc[len(st.session_state.expenses_df)] = [category, amount, False]
        else:
            st.warning("Please enter an expense")
            
    st.write("### Monthly Expenses:", st.session_state.expenses_df)
    st.session_state.expenses_df["Delete"] = False
    st.write("Edit or delete expenses here:")
    st.session_state.expenses_df = st.data_editor(st.session_state.expenses_df, num_rows = "dynamic", use_container_width=True)
    st.session_state.expenses_df = st.session_state.expenses_df[st.session_state.expenses_df["Delete"] == False]
    if st.button("Save Income and Expenses"):
        st.session_state.profile = {
            "email": email,
            "annual_income": annual_income,
            "months_worked": months_worked,
            "annual_bonus": annual_bonus,
            "state_tax_perc": state_tax_perc,
            "local_tax_perc": local_tax_perc,
            "marriage_status": marriage_status,
            "expenses_df": st.session_state.expenses_df if not st.session_state.expenses_df.empty else None
        }
        # TODO: make the update methods
        db = Database()
        user_id = db.get_user(email)["user_id"]
        db.update_income(user_id, annual_income, annual_bonus, state_tax_perc, local_tax_perc, marriage_status, months_worked)
        df = st.session_state.expenses_df.copy()
        df = df.replace("", None)
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df.dropna(subset=["category", "amount"])
        db.update_expenses(user_id, df)
        st.success("Income and Expenses Saved!")
