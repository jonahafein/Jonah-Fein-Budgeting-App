import streamlit as st
import pandas as pd

# need logic to actually save a profile, and be able to update/edit a profile

st.title("Account Info")

# initialize the session state
if "email" not in st.session_state:
    st.session_state.email = None
    
if "debt_df" not in st.session_state:
    st.session_state.debt_df = pd.DataFrame(columns = ["Item", "Balance", "Interest Rate"])
    
if "profile" not in st.session_state:
    st.session_state.profile = {}


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
    
    savings = st.number_input("Enter your total liquid savings:")
    if savings > 0:
        apy = st.number_input("Enter your savings account's apy %:")

    brokerage = st.number_input("Enter your non retirement investment total:")
    if brokerage > 0:
        brokerage_returns = st.number_input("Enter your expected brokerage percentage average returns based on your fund's history")

    retirement = st.number_input("Enter your retirement account(s) total:")
    if retirement > 0:
        retirement_returns = st.number_input("Enter your expected retirement percentage average returns based on your fund's history")
        
    home = st.selectbox("Do you own a home?", ["no", "yes"])
    
    # do an option for those who have paid off their house
    
    if home == "yes":
        paid = st.selectbox("Is it paid off?", ['no', 'yes'])
        if paid == 'no': 
            col1,col2,col3, col4, col5 = st.columns(5)
            with col1:
                years = st.number_input("How many years left on the mortgage?")
            with col2:
                balance = st.number_input("What is the remaining balance?")
            with col3:
                interest = st.number_input("What is the interest rate? (If variable, give an average)")
            with col4:
                fees = st.number_input("Typical monthly non-mortgage house costs?")  
            with col5:
                value = st.number_input("What is your home's estimated value?")             
            mortgage_info = [years, balance, interest, fees, value]
        else:
            col1,col2 = st.columns(2)
            with col1:
                value = st.number_input("What is your home's value?")
            with col2:
                fees = st.number_input("Typical monthly non-mortgage house costs?")
            house_info = [value, fees]
    # add other necessary questions

    goals = st.multiselect('Goals:', ['Build up my emergency fund', 'invest/save for non retirement', 'invest for retirement', 'get out of debt', 'other'])
    if 'other' in goals:
        monthly_other = st.number_input("Estimate how many dollars a month you will need to put away for your other category:")
    if 'get out of debt' in goals:
        st.write("List all of your non mortgage debt 1 by 1:")
        if 'debt_df' not in st.session_state:
            st.session_state.debt_df = pd.DataFrame(columns = ["Item", "Balance", "Interest Rate"])
        
        col1,col2,col3 = st.columns(3)
        with col1:
            item = st.text_input("Enter debt item:")
        with col2:
            balance = st.number_input("Enter debt balance")
        with col3:
            interest = st.number_input("Enter interest rate:")
            
        if st.button("Add"):
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
    
        
        
    
    


