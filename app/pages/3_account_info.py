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
user_id = db.get_user(st.session_state.email)["user_id"]

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
    st.session_state.home_data = home_data if home_data else []
    if debt_df:
        st.session_state.debt_df = pd.DataFrame([{
            "Item": d["debt_item"],
            "Balance": d["debt_balance"],
            "Interest Rate": d["debt_interest"]
        }for d in debt_df])
    
    # now the session state is loaded
    st.session_state.loaded = True
    

st.title("Account Info")

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


    home = st.selectbox("Do you own a home?", ["no", "yes"])
    
    # do an option for those who have paid off their house
    
    if home == "yes":
        paid = st.selectbox("Is it paid off?", ['no', 'yes'])
        if paid == 'no': 
            col1,col2,col3, col4, col5 = st.columns(5)
            with col1:
                years = st.number_input("How many years left on the mortgage?", key = "years")
            with col2:
                balance = st.number_input("What is the remaining balance?", key = "debt_balance")
            with col3:
                interest = st.number_input("What is the interest rate? (If variable, give an average)", key = "debt_interest")
            with col4:
                fees = st.number_input("Typical monthly non-mortgage house costs?", key = "fees")  
            with col5:
                value = st.number_input("What is your home's estimated value?", key = "value")             
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
                value = st.number_input("What is your home's value?", key = "value")
            with col5:
                fees = st.number_input("Typical monthly non-mortgage house costs?", key = "fees")
            house_info = [years, balance, interest, value, fees]
    # add other necessary questions

    goals = st.multiselect('Goals:', ['Build up my emergency fund', 'invest/save for non retirement', 'invest for retirement', 'other'], default = st.session_state.goals)
    st.session_state.goals = goals
    if 'other' in goals:
        monthly_other = st.number_input("Estimate how many dollars a month you will need to put away for your other category:", key = "monthly_other")
    
    
    st.write("List all of your non mortgage debt 1 by 1:")
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
                
    if st.button("Save profile"):
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
            "debt_df": st.session_state.debt_df if st.session_state.debt_df else None,
            "home": home,
            "paid": paid,
            "house_info": house_info if paid == "yes" else None
        }
        # TODO: make the update methods
        # db = Database()
        # user_id = db.get_user(email)["user_id"]
        # db.update_non_home_assets(user_id, savings, apy, brokerage, brokerage_returns, retirement, retirement_returns)
        # db.update_home(user_id, paid, value, years, balance, interest, fees)
        # for goal in goals:
        #     db.update_goal(user_id, goal)
        # for _, row in st.session_state.debt_df.iterrows():
        #     db.update_debt(user_id, row["Item"], row["Balance"], row["Interest Rate"])
        
        st.success("profile saved!")
    
        
        
    
    


