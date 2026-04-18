import streamlit as st
import pandas as pd
import sys
import os

folder_path = os.path.abspath("/Users/jonahafein//Desktop/Python Projects/Jonah-Fein-Budgeting-App/backend")

if folder_path not in sys.path:
    sys.path.append(folder_path)

from db import Database

# making user enter email to log in first
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

# setting the session state by pulling existing data from azure for this specific user_id
if "loaded" not in st.session_state:
    # first pull the data
    assets = db.get_non_home_assets(user_id)
    home_data = db.get_home(user_id)
    goals = db.get_goals(user_id)
    debt_df = db.get_debts(user_id)
    
    # next set the session state 
    st.session_state.savings = assets["savings"] if assets else 0
    st.session_state.apy = assets["apy"] if assets else 0
    st.session_state.brokerage = assets["brokerage"] if assets else 0
    st.session_state.brokerage_returns = assets["brokerage_returns"] if assets else 0
    st.session_state.retirement = assets["retirement"] if assets else 0
    st.session_state.retirement_returns = assets["retirement_returns"] if assets else 0
    st.session_state.goals = goals if goals else []
    st.session_state.home_data = home_data if home_data else None
    if debt_df:
        st.session_state.debt_df = pd.DataFrame([{
            "Item": d["debt_item"],
            "Balance": d["debt_balance"],
            "Interest Rate": d["debt_interest"]
        }for d in debt_df])
    
    # now the session state is loaded
    st.session_state.loaded = True
    

st.title("Assets and Goals")

# initialize debt_df if not there
if "debt_df" not in st.session_state:
    st.session_state.debt_df = pd.DataFrame(columns = ["Item", "Balance", "Interest Rate"])

# (probably a redundant check but harmless)
if st.session_state.email: 
    email = st.session_state.email
    monthly_other = None
    home_data = st.session_state.home_data
    paid = True if home_data and home_data["balance"] == 0 else False
    house_info = home_data
    
    # now we allow for inputs and updated session state - will have update methods used later
    savings = st.number_input("Savings:", value = st.session_state.savings)
    st.session_state.savings = savings
    apy = st.number_input("Apy:", value = st.session_state.apy)
    st.session_state.apy = apy
    brokerage = st.number_input("Brokerage:", value = st.session_state.brokerage)
    st.session_state.brokerage = brokerage
    brokerage_returns = st.number_input("Brokerage expected returns:", value = st.session_state.brokerage_returns)
    st.session_state.brokerage_returns = brokerage_returns
    retirement = st.number_input("Retirement:", value = st.session_state.retirement)
    st.session_state.retirement = retirement
    retirement_returns = st.number_input("Retirement expected returns:", value = st.session_state.retirement_returns)
    st.session_state.retirement_returns = retirement_returns

    home_exists = True if home_data else False
    home = st.selectbox("Do you own a home?", ["no", "yes"], index=1 if home_exists else 0)
    if home == "yes":
        home_exists = True
    else:
        home_exists = False
        
    
    # do an option for those who have paid off their house
    
    if home_exists:
        paid_default = 1 if (home_data and home_data.get("paid_off")) else 0
        paid = st.selectbox("Is it paid off?", ['no', 'yes'], index=paid_default)
        if paid == 'no': 
            col1,col2,col3, col4, col5 = st.columns(5)
            with col1:
                years = st.number_input("How many years left on the mortgage?", value = st.session_state.home_data["years"] if st.session_state.home_data else 0)
            with col2:
                balance = st.number_input("What is the remaining balance?", value = st.session_state.home_data["balance"] if st.session_state.home_data else 0)
            with col3:
                interest = st.number_input("What is the interest rate? (If variable, give an average)", st.session_state.home_data["interest"] if st.session_state.home_data else 0)
            with col4:
                fees = st.number_input("Typical monthly non-mortgage house costs?", st.session_state.home_data["fees"] if st.session_state.home_data else 0)  
            with col5:
                value = st.number_input("What is your home's estimated value?", st.session_state.home_data["home_value"] if st.session_state.home_data else 0)             
            house_info = [years, balance, interest, fees, value]
        else:
            col1,col2, col3, col4, col5 = st.columns(5)
            with col1:
                years = None
            with col2:
                balance = None
            with col3:
                interest = None
            with col4:
                value = st.number_input("What is your home's value?", st.session_state.home_data["home_value"]if st.session_state.home_data else 0)
            with col5:
                fees = st.number_input("Typical monthly non-mortgage house costs?", st.session_state.home_data["fees"] if st.session_state.home_data else 0)
            house_info = [years, balance, interest, value, fees]
    else:
        paid = None 
        value = None 
        years = None
        balance = None 
        interest = None
        fees = None
    # add other necessary questions

    goals = st.multiselect('Goals:', ['Build up my emergency fund', 'invest/save for non retirement', 'invest for retirement', 'other'], default = st.session_state.goals)
    st.session_state.goals = goals
    if 'other' in goals:
        monthly_other = st.number_input("Estimate how many dollars a month you will need to put away for your other category:", key = "monthly_other")
    
    
    st.write("List all of your non-mortgage debts:")
    if 'debt_df' not in st.session_state:
        st.session_state.debt_df = pd.DataFrame(columns = ["Item", "Balance", "Interest Rate"])
    
    col1,col2,col3 = st.columns(3)
    with col1:
        item = st.text_input("Enter debt item:")
    with col2:
        balance = st.number_input("Enter debt balance", key = "balance")
    with col3:
        interest = st.number_input("Enter interest rate:", key = "interest")
        
    if st.button("Add Debt"):
        if item:
            st.session_state.debt_df.loc[len(st.session_state.debt_df)] = [item, balance, interest]
        else:
            st.warning("Please enter an item")
            
    st.write("### Debt:", st.session_state.debt_df)
                
    if st.button("Save Assets and Goals"):
        st.session_state.profile = {
            "email": email,
            "savings": savings,
            "apy": apy if savings > 0 else None,
            "brokerage": brokerage,
            "brokerage_returns": brokerage_returns if brokerage > 0 else None,
            "retirement": retirement,
            "retirement_returns": retirement_returns if retirement > 0 else None,
            "goals": goals,
            "monthly_other": monthly_other if "other" in goals else None,
            "debt_df": st.session_state.debt_df if not st.session_state.debt_df.empty else None,
            "home": home,
            "paid": paid,
            "house_info": house_info if paid == "yes" else None
        }
        # TODO: make the update methods
        db = Database()
        user_id = db.get_user(email)["user_id"]
        db.update_non_home_assets(user_id, savings, apy, brokerage, brokerage_returns, retirement, retirement_returns)
        paid_bool = True if paid == "yes" else False
        if home == "yes":
            db.update_home(user_id, paid_bool, value, years, balance, interest, fees)
        else:
            db.delete_home(user_id)
        goals = list(st.session_state.goals)
        db.update_goals(user_id, goals)
        db.update_debts(user_id, st.session_state.debt_df)
        st.success("Assets and Goals Saved!")
    
        
        
    
    


