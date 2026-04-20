import streamlit as st 
import pandas as pd
import sys
import os

folder_path = os.path.abspath("/Users/jonahafein//Desktop/Python Projects/Jonah-Fein-Budgeting-App/backend")

if folder_path not in sys.path:
    sys.path.append(folder_path)

from db import Database
import utils

if not st.session_state.get("email"):
    st.warning("Please log in first")
    st.stop()

st.title("Account Dashboard")

st.write("Please fill out the other two pages fully before returning here for best results. Also, please wait a few seconds for this dashboard to load.")
st.subheader(f"Account insights for {st.session_state.email}:")

# getting their user_id  
db = Database()
user = db.get_user(st.session_state.email)
if not user:
    st.error("User not found")
    st.stop()

user_id = user["user_id"]

# bringing the full picture together

# income and expenses
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
    
if "expenses_df" not in st.session_state:
    st.session_state.expenses_df = pd.DataFrame(columns = ["category", "amount"])
    

# now let's load assets and goals:
assets = db.get_non_home_assets(user_id)
home_data = db.get_home(user_id)
goals = db.get_goals(user_id)
debt_df = db.get_debts(user_id)
st.session_state.savings = assets["savings"] if assets else 0
st.session_state.apy = assets["apy"] if assets else 0
st.session_state.brokerage = assets["brokerage"] if assets else 0
st.session_state.brokerage_returns = assets["brokerage_returns"] if assets else 0
st.session_state.retirement = assets["retirement"] if assets else 0
st.session_state.retirement_returns = assets["retirement_returns"] if assets else 0
st.session_state.goals = goals if goals else []
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
    
if st.session_state.marriage_status =="single":
    standard_deduction = 16100
else:
    standard_deduction = 32200
    
if st.session_state.marriage_status =="single":
    single = True
else:
    single = False
    
total_income = st.session_state.annual_income + st.session_state.annual_bonus

# snapshot
st.subheader("Your Current Finnancial Snapshot:")
    
# for each of these, add an estimated time to completion for goals
st.subheader("Reccomendations:")
if st.session_state.savings < 1000:
    st.write("We reccomend that for now, you pay minimum payments on all debt, pause investing (including for retirement), and put all of your monthly margin towards building a $1000 starter emergency fund.")
    monthly_take_home = utils.calculate_monthly_take_home(single = single, annual_income = total_income, trad_401k_contributions = 0, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc)
    monthly_margin = utils.calculate_monthly_margin(monthly_take_home = monthly_take_home, expenses_df = st.session_state.expenses_df)
    st.write(f"Your monthly margin this month should be roughly {monthly_margin:.2f} dollars.")
elif "debt_df" in st.session_state and not st.session_state.debt_df.empty and st.session_state.savings >= 1000:
    highest_interest_debt = st.session_state.debt_df.loc[st.session_state.debt_df['Interest Rate'].idxmax()]['Item'] 
    monthly_take_home = utils.calculate_monthly_take_home(single = single, annual_income = total_income, trad_401k_contributions = 0, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc)
    monthly_margin = utils.calculate_monthly_margin(monthly_take_home = monthly_take_home, expenses_df = st.session_state.expenses_df)
    st.write(f"We reccomend you temporarily pause all saving and investing (including retirement) and invest your entire monthly margin at your non-mortgage debt, starting with {highest_interest_debt} as it is your highest interest debt.")
    st.write(f"Your monthly margin this month should be roughly {monthly_margin:.2f} dollars.")
    st.write(f"We also reccomend you take {st.session_state.savings - 1000: .2f} from your savings and put in on your debt, again starting with {highest_interest_debt}")
    
# next build up to 6 months of emergency
    
    

    




