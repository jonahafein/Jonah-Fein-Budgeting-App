import streamlit as st
import pandas as pd
import sys
import os

folder_path = os.path.abspath("/Users/jonahafein//Desktop/Python Projects/Jonah-Fein-Budgeting-App/backend")

if folder_path not in sys.path:
    sys.path.append(folder_path)

from db import Database

# need logic to actually save a profile, and be able to update/edit a profile

if not st.session_state.get("email"):
    st.warning("Please log in first")
    st.stop()
    
def build_profile():
    return {
        "email": st.session_state.email,
        "savings": st.session_state.get("savings"),
        'apy': st.session_state.get("apy"),
        'brokerage': st.session_state.get("brokerage"),
        'retirement': st.session_state.get('retirement'),
        'goals': st.session_state.get('goals'),
        'debt_df': st.session_state.debt_df.to_dict()
    }

st.title("Account Info")

# initialize the session state
if "email" not in st.session_state:
    st.session_state.email = None
    
if "debt_df" not in st.session_state:
    st.session_state.debt_df = pd.DataFrame(columns = ["Item", "Balance", "Interest Rate"])
    
if "profile" not in st.session_state:
    st.session_state.profile = build_profile()


if st.session_state.email: 
    email = st.session_state.email
    savings = None
    apy = None
    brokerage = None
    brokerage_returns = None
    retirement = None
    retirement_returns = None
    goals = None
    monthly_other = None
    debt_df = None
    home = None
    paid = None
    mortgage_info = None
    house_info = None
    
    savings = st.number_input("Enter your total liquid savings:", key = "savings")
    if savings > 0:
        apy = st.number_input("Enter your savings account's apy %:", key = "apy")

    brokerage = st.number_input("Enter your non retirement investment total:", key = "brokerage")
    if brokerage > 0:
        brokerage_returns = st.number_input("Enter your expected brokerage percentage average returns based on your fund's history", key = "brokerage_returns")

    retirement = st.number_input("Enter your retirement account(s) total:", key = "retirement")
    if retirement > 0:
        retirement_returns = st.number_input("Enter your expected retirement percentage average returns based on your fund's history", key = "retirement_returns")
        
    home = st.selectbox("Do you own a home?", ["no", "yes"])
    
    # do an option for those who have paid off their house
    
    if home == "yes":
        paid = st.selectbox("Is it paid off?", ['no', 'yes'])
        if paid == 'no': 
            col1,col2,col3, col4, col5 = st.columns(5)
            with col1:
                years = st.number_input("How many years left on the mortgage?", key = "years")
            with col2:
                balance = st.number_input("What is the remaining balance?", key = "balance")
            with col3:
                interest = st.number_input("What is the interest rate? (If variable, give an average)", key = "interest")
            with col4:
                fees = st.number_input("Typical monthly non-mortgage house costs?", key = "fees")  
            with col5:
                value = st.number_input("What is your home's estimated value?", key = "value")             
            mortgage_info = [years, balance, interest, fees, value]
        else:
            col1,col2 = st.columns(2)
            with col1:
                value = st.number_input("What is your home's value?", key = "value")
            with col2:
                fees = st.number_input("Typical monthly non-mortgage house costs?", key = "fees")
            house_info = [value, fees]
    # add other necessary questions

    goals = st.multiselect('Goals:', ['Build up my emergency fund', 'invest/save for non retirement', 'invest for retirement', 'get out of debt', 'other'])
    if 'other' in goals:
        monthly_other = st.number_input("Estimate how many dollars a month you will need to put away for your other category:", key = "monthly_other")
    if 'get out of debt' in goals:
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
            "debt_df": st.session_state.debt_df if "get out of debt" in goals else None,
            "home": home,
            "paid": paid,
            "mortgage_info": mortgage_info if paid == "no" else None,
            "house_info": house_info if paid == "yes" else None
        }
        st.success("profile saved!")
    
        
        
    
    


