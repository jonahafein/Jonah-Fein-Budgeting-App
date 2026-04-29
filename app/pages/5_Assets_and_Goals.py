import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.db import Database

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
    debt_df = db.get_debts(user_id)
    
    # next set the session state 
    st.session_state.savings = assets["savings"] if assets else 0
    st.session_state.apy = float(assets["apy"]) if assets and assets["apy"] is not None else 0.0
    st.session_state.brokerage = assets["brokerage"] if assets else 0
    st.session_state.brokerage_returns = assets["brokerage_returns"] if assets else 0
    st.session_state.retirement = assets["retirement"] if assets else 0
    st.session_state.retirement_returns = assets["retirement_returns"] if assets else 0
    st.session_state.home_data = home_data if home_data else None
    if home_data:
        st.session_state.years = home_data["years"]
        st.session_state.home_balance = home_data["balance"]
        st.session_state.home_interest = home_data["interest"]
        st.session_state.fees = home_data["fees"]
        st.session_state.home_value = home_data["home_value"]
    if debt_df:
        st.session_state.debt_df = pd.DataFrame([{
            "Item": d["debt_item"],
            "Balance": d["debt_balance"],
            "Interest Rate": d["debt_interest"]
        }for d in debt_df])
    
    # now the session state is loaded
    st.session_state.loaded = True
    

st.title("Assets")
st.write("Make sure to save any changes made.")

# initialize debt_df if not there
if "debt_df" not in st.session_state:
    st.session_state.debt_df = pd.DataFrame(columns = ["Item", "Balance", "Interest Rate"])

# (probably a redundant check but harmless)
if st.session_state.email: 
    email = st.session_state.email
    monthly_other = None
    home_data = st.session_state.home_data
    paid = home_data["paid_off"] if home_data else False
    house_info = home_data
    
    # now we allow for inputs and updated session state - will have update methods used later
    savings = st.number_input("Savings:", value = st.session_state.savings)
    st.session_state.savings = savings
    apy = st.number_input("Apy:", value = float(st.session_state.apy), step=0.01, format="%.2f")
    st.session_state.apy = apy
    brokerage = st.number_input("Brokerage:", value = st.session_state.brokerage)
    st.session_state.brokerage = brokerage
    brokerage_returns = st.number_input("Brokerage expected returns:", value = float(st.session_state.brokerage_returns), step=0.01, format="%.2f")
    st.session_state.brokerage_returns = brokerage_returns
    retirement = st.number_input("Retirement:", value = st.session_state.retirement)
    st.session_state.retirement = retirement
    retirement_returns = st.number_input("Retirement expected returns:", value = float(st.session_state.retirement_returns), step=0.01, format="%.2f")
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
                years = st.number_input("How many years left on the mortgage?", value = st.session_state.get("years", home_data["years"] if home_data else 0))
                st.session_state.years = years
            with col2:
                home_balance = st.number_input("What is the remaining balance?", value = st.session_state.get("home_balance", home_data["balance"] if home_data else 0))
                st.session_state.home_balance = home_balance
            with col3:
                home_interest = st.number_input("What is the interest rate? (If variable, give an average)", value = float(st.session_state.get("home_interest", home_data["interest"] if home_data else 0)), step=0.01, format="%.2f")
                st.session_state.home_interest = home_interest
            with col4:
                fees = st.number_input("Typical monthly non-mortgage house costs?", value = st.session_state.get("fees", home_data["fees"] if home_data else 0))  
                st.session_state.fees = fees
            with col5:
                value = st.number_input("What is your home's estimated value?", value = st.session_state.get("home_value", home_data["home_value"] if home_data else 0))
                st.session_state.home_value = value             
            house_info = [years, home_balance, home_interest, fees, value]
        else:
            col1,col2, col3, col4, col5 = st.columns(5)
            with col1:
                years = None
                st.session_state.years = 0
            with col2:
                home_balance = None
                st.session_state.home_balance = 0
            with col3:
                home_interest = None
                st.session_state.home_interest = 0
            with col4:
                value = st.number_input("What is your home's value?", st.session_state.get("home_value", home_data["home_value"] if home_data else 0))
                st.session_state.home_value = value
            with col5:
                fees = st.number_input("Typical monthly non-mortgage house costs?", st.session_state.get("fees", home_data["fees"] if home_data else 0))
                st.session_state.fees = fees
            house_info = [years, home_balance, home_interest, value, fees]
    else:
        paid = None 
        value = None 
        years = None
        home_balance = None 
        home_interest = None
        fees = None
    # add other necessary questions
    
    
    st.write("Add debt items here:")
    if 'debt_df' not in st.session_state:
        st.session_state.debt_df = pd.DataFrame(columns = ["Item", "Balance", "Interest Rate"])
    
    col1,col2,col3 = st.columns(3)
    with col1:
        item = st.text_input("Enter debt item:")
    with col2:
        balance = st.number_input("Enter debt balance", key = "balance")
    with col3:
        interest = st.number_input("Enter interest rate:", value=0.0, key = "interest", step=0.01, format="%.2f")
        
    if st.button("Add Debt"):
        if item:
            st.session_state.debt_df.loc[len(st.session_state.debt_df)] = [item, balance, interest]
        else:
            st.warning("Please enter an item")
            
    st.write("### Your Debt:", st.session_state.debt_df)
    st.session_state.debt_df["Delete"] = False
    st.write("Edit or delete debt item's here:")
    st.session_state.debt_df = st.data_editor(st.session_state.debt_df, num_rows = "dynamic", use_container_width=True)
    st.session_state.debt_df = st.session_state.debt_df[st.session_state.debt_df["Delete"] == False]
       
    if st.button("Save Assets"):
        st.session_state.profile = {
            "email": email,
            "savings": savings,
            "apy": apy if savings > 0 else None,
            "brokerage": brokerage,
            "brokerage_returns": brokerage_returns if brokerage > 0 else None,
            "retirement": retirement,
            "retirement_returns": retirement_returns if retirement > 0 else None,
            "debt_df": st.session_state.debt_df if not st.session_state.debt_df.empty else None,
            "home": home,
            "paid": paid,
            "house_info": house_info
        }
        # TODO: make the update methods
        db = Database()
        user_id = db.get_user(email)["user_id"]
        db.update_non_home_assets(user_id, savings, apy, brokerage, brokerage_returns, retirement, retirement_returns)
        paid_bool = True if paid == "yes" else False
        if home == "yes":
            db.update_home(user_id, paid_bool, st.session_state.home_value, st.session_state.years, st.session_state.home_balance, st.session_state.home_interest, st.session_state.fees)
        else:
            db.delete_home(user_id)
        df = st.session_state.debt_df.copy()
        df = df.replace("", None)
        df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce")
        df["Interest Rate"] = pd.to_numeric(df["Interest Rate"], errors="coerce")
        df = df.dropna(subset=["Item", "Balance", "Interest Rate"])
        db.update_debts(user_id, df)
        st.success("Assets Saved!")
        st.session_state.home_data = db.get_home(user_id)
    
        
        
    
    


