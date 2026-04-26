import sys
import os
import streamlit as st
import pandas as pd
    
from backend.help_llm import ai_helper
from backend.db import Database

if not st.session_state.get("email"):
    st.warning("Please log in first")
    st.stop()

if "data_loaded" not in st.session_state:
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
    if "expenses_df" not in st.session_state:
        st.session_state.expenses_df = pd.DataFrame(columns = ["category", "amount"])
        
    months_worked = max(st.session_state.months_worked, 1)
    st.session_state.months_worked = months_worked 

    # add all else to session_state
    dashboard = db.get_dashboard(user_id)
    trad_401k_contributions = dashboard["trad_401k_contributions"] if dashboard else 0
    trad_401k_match_annual = dashboard["trad_401k_match_annual"] if dashboard else 0
    roth_ira_monthly = dashboard["roth_ira_monthly"] if dashboard else 0
    roth_401k_contributions_monthly = dashboard["roth_401k_contributions_monthly"] if dashboard else 0
    roth_401k_match_monthly = dashboard["roth_401k_match_monthly"] if dashboard else 0
    years_from_retirement = dashboard["years_from_retirement"] if dashboard else 0
    brokerage_contributions_monthly = dashboard["brokerage_contributions_monthly"] if dashboard else 0
    years_from_brokerage = dashboard["years_from_brokerage"] if dashboard else 0
    future_savings_view = dashboard["future_savings_view"] if dashboard else 0

    st.session_state.trad_401k_contributions = trad_401k_contributions if trad_401k_contributions else 0
    st.session_state.trad_401k_match_annual = trad_401k_match_annual if trad_401k_match_annual else 0
    st.session_state.roth_ira_monthly = roth_ira_monthly if roth_ira_monthly else 0
    st.session_state.roth_401k_contributions_monthly = roth_401k_contributions_monthly if roth_401k_contributions_monthly else 0
    st.session_state.roth_401k_match_monthly = roth_401k_match_monthly if roth_401k_match_monthly else 0
    st.session_state.years_from_retirement = years_from_retirement if years_from_retirement else 0
    st.session_state.brokerage_contributions_monthly = brokerage_contributions_monthly if brokerage_contributions_monthly else 0
    st.session_state.years_from_brokerage = years_from_brokerage if years_from_brokerage else 0
    st.session_state.future_savings_view = future_savings_view if future_savings_view else 0
        
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
    else:
        st.session_state.years = 0
        st.session_state.home_balance = 0
        st.session_state.home_interest = 0
        st.session_state.fees = 0
        st.session_state.home_value = 0
        
    if debt_df:
        st.session_state.debt_df = pd.DataFrame([{
            "Item": d["debt_item"],
            "Balance": d["debt_balance"],
            "Interest Rate": d["debt_interest"]
        }for d in debt_df])
    else:
        st.session_state.debt_df = pd.DataFrame(columns = ["Item", "Balance", "Interest Rate"])
        
    if st.session_state.marriage_status =="single":
        standard_deduction = 16100
    else:
        standard_deduction = 32200
        
    if st.session_state.marriage_status =="single":
        single = True
    else:
        single = False
        
    annual_income = st.session_state.annual_income
    three_month_expenses = 3*(st.session_state.expenses_df["amount"].sum())
    six_month_expenses = 6*(st.session_state.expenses_df["amount"].sum())

    three_month_expenses_met = st.session_state.savings > three_month_expenses
    if three_month_expenses_met:
        three_month_expenses_met = "✅"
    else:
        three_month_gap = three_month_expenses - st.session_state.savings
        three_month_expenses_met = f"❌ - {three_month_gap:,.2f} dollars away."
    six_month_expenses_met = st.session_state.savings > six_month_expenses
    if six_month_expenses_met:
        six_month_expenses_met = "✅"
    else:
        six_month_gap = six_month_expenses - st.session_state.savings
        six_month_expenses_met = f"❌ - {six_month_gap:,.2f} dollars away."

    # determining if ready for step 4:
    continue_on_step4 = False 
    if "debt_df" in st.session_state and st.session_state.debt_df.empty and st.session_state.savings > three_month_expenses:
        continue_on_step4 = True
    st.session_state.data_loaded = True

st.title("Help Page:")
consent = st.selectbox(
    "Allow the AI assistant to access your financial data for more personalized help?",
    options=["no", "yes"]
)
st.caption(
    "If you choose 'yes', the assistant will use your inputs (income, expenses, assets, etc.) to give better recommendations. "
    "Your data is only used within this app and is not shared externally. "
    "You can still use the assistant without sharing your data."
)
st.session_state.consent = consent
st.write("Please give a second for responses to load.")

def build_user_context_data_consent():
    return f"""
Here is the user's financial data:

Income:
- Annual income: {st.session_state.get("annual_income", 0)}
- Bonus: {st.session_state.get("annual_bonus", 0)}
- Months worked: {st.session_state.get("months_worked", 12)}

Expenses:
- Total monthly expenses: {st.session_state.expenses_df["amount"].sum()}

Breakdown:
{st.session_state.expenses_df.to_dict(orient="records")}

Assets:
- Savings: {st.session_state.get("savings", 0)}
- Brokerage: {st.session_state.get("brokerage", 0)}
- Retirement: {st.session_state.get("retirement", 0)}

Debt:
- Total debt: {st.session_state.debt_df}

Investing:
- Traditional 401k: {st.session_state.get("trad_401k_contributions", 0)}
- Roth IRA monthly: {st.session_state.get("roth_ira_monthly", 0)}
- Roth 401k monthly: {st.session_state.get("roth_401k_contributions_monthly", 0)}

Goals:
- {st.session_state.get("goals", [])}
"""

def build_user_context_no_consent():
    return "The user has not shared financial data. Provide general guidance only."

def stream_response(stream):
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

client = ai_helper()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    if st.session_state.consent == "yes":
        user_context = build_user_context_data_consent()
    else:
        user_context = build_user_context_no_consent()
    with st.chat_message("assistant"):
        stream = client.chat(
            messages=[
                {"role": "system", "content": user_context},  # <-- ADD THIS LINE
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            ],
            stream=True
        )

        response = st.write_stream(stream_response(stream))
    st.session_state.messages.append({"role": "assistant", "content": response})