import streamlit as st 
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.db import Database
import backend.utils as utils
from backend.recs_llm import ai_recs

import re

def clean_text(text):
    import re
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)
    # Fix camelCase
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # REMOVE markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)

    # add spaces in long merged words
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # again just in case
    text = re.sub(r'([a-z]{2,})([A-Z])', r'\1 \2', text)

    # Add space before parentheses if missing
    text = re.sub(r'([a-zA-Z])\(', r'\1 (', text)

    # Fix multiple spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

if not st.session_state.get("email"):
    st.warning("Please log in first")
    st.stop()

st.title("Account Dashboard")

st.write("Fill out the other two pages fully before returning here for best results. If you take any of our recommendations, or make any changes, be sure to update the other pages before returning here. Refer to the help page for assistance, logic behind recommendations, concept explanations, and additional resources. Please wait a few seconds for this dashboard to load.")

# getting their user_id  
db = Database()
user = db.get_user(st.session_state.email)
if not user:
    st.error("User not found")
    st.stop()

user_id = user["user_id"]
if user and user["birthdate"]:
    st.session_state.birthdate = datetime.strptime(user["birthdate"], "%Y-%m-%d").date()
else:
    st.session_state.birthdate = None

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
margin_on_debt_monthly = dashboard["margin_on_debt_monthly"] if dashboard else 0
trad_401k_contributions_monthly = dashboard["trad_401k_contributions_monthly"] if dashboard else 0
trad_401k_match_monthly = dashboard["trad_401k_match_monthly"] if dashboard else 0
roth_ira_monthly = dashboard["roth_ira_monthly"] if dashboard else 0
roth_401k_contributions_monthly = dashboard["roth_401k_contributions_monthly"] if dashboard else 0
roth_401k_match_monthly = dashboard["roth_401k_match_monthly"] if dashboard else 0
years_from_retirement = dashboard["years_from_retirement"] if dashboard else 0
brokerage_contributions_monthly = dashboard["brokerage_contributions_monthly"] if dashboard else 0
years_from_brokerage = dashboard["years_from_brokerage"] if dashboard else 0
future_savings_view = dashboard["future_savings_view"] if dashboard else 0

st.session_state.margin_on_debt_monthly = margin_on_debt_monthly if margin_on_debt_monthly else 0
st.session_state.trad_401k_contributions_monthly = trad_401k_contributions_monthly if trad_401k_contributions_monthly else 0
st.session_state.trad_401k_match_monthly = trad_401k_match_monthly if trad_401k_match_monthly else 0
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
debt_df = db.get_debts(user_id)
st.session_state.savings = assets["savings"] if assets else 0
st.session_state.apy = assets["apy"] if assets else 0
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
    
    
# snapshot
st.subheader("Your Current Financial Snapshot:")
net_worth = utils.calculate_net_worth(home_value = st.session_state.home_value, home_debt = st.session_state.home_balance, savings = st.session_state.savings, brokerage = st.session_state.brokerage, retirement = st.session_state.retirement, debt_total = st.session_state.debt_df["Balance"].sum())
trad_401k_contributions_monthly = 0
monthly_take_home = utils.calculate_monthly_take_home(single = single, annual_income = annual_income, trad_401k_contributions_monthly = trad_401k_contributions_monthly, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc, months_worked = st.session_state.months_worked)
monthly_margin = utils.calculate_monthly_margin(monthly_take_home = monthly_take_home, expenses_df = st.session_state.expenses_df, trad_401k_contributions_monthly = trad_401k_contributions_monthly, months_worked = months_worked)
st.session_state.monthly_margin = monthly_margin
st.write(f"Net Worth: ${net_worth:,.2f}")
st.write(f"Monthly Income After Tax (before any traditional 401k investing): ${monthly_margin + st.session_state.expenses_df["amount"].sum():,.2f}")
st.write(f"Monthly Expenses: ${st.session_state.expenses_df["amount"].sum():,.2f}")
st.write(f"Monthly Margin (before any traditional 401k investing): ${monthly_margin:,.2f}")

# check or x if reached, if x by how much
st.write(f"3 month emergency fund: ${three_month_expenses:,.2f}", three_month_expenses_met)
st.write(f"6 month emergency fund: ${six_month_expenses:,.2f}", six_month_expenses_met)
if st.session_state.debt_df is not None and not st.session_state.debt_df.empty and st.session_state.debt_df["Balance"].sum() > 0:
    st.write(f"Your debt: ${st.session_state.debt_df["Balance"].sum()} with average interest: {np.average(st.session_state.debt_df['Interest Rate'], weights=st.session_state.debt_df['Balance']):,.2f}") 
else:
    st.write("You Have no Debt!")
if st.session_state.savings > six_month_expenses:
    st.write(f"You have ${st.session_state.savings - six_month_expenses:,.2f} in savings that exceed your 6 month emergency fund (i.e., regular savings).")
age = datetime.today().date() - st.session_state.birthdate

salary_income_prorated = st.session_state.annual_income * (months_worked / 12)
salary_taxable = utils.get_annual_federal_taxable_income(annual_income = salary_income_prorated,trad_401k_contributions_monthly = trad_401k_contributions_monthly,standard_deduction = standard_deduction, months_worked = months_worked)
salary_federal_tax = utils.calculate_federal_tax(single = single,annual_federal_taxable_income = salary_taxable)
recommended_withholding = salary_federal_tax / months_worked
# total income with bonus
annual_take_home_no_bonus = months_worked*(utils.calculate_monthly_take_home(single = single, annual_income = annual_income,trad_401k_contributions_monthly = trad_401k_contributions_monthly, standard_deduction = standard_deduction, state_tax_perc = state_tax_perc, local_tax_perc = local_tax_perc, months_worked = months_worked))
annual_taxes_no_bonus = salary_income_prorated - annual_take_home_no_bonus
adjusted_total_income = st.session_state.annual_income + (annual_bonus * (12 / months_worked))
total_income = salary_income_prorated + annual_bonus
annual_take_home_with_bonus = months_worked*(utils.calculate_monthly_take_home(single = single, annual_income = adjusted_total_income,trad_401k_contributions_monthly = trad_401k_contributions_monthly, standard_deduction = standard_deduction, state_tax_perc = state_tax_perc, local_tax_perc = local_tax_perc, months_worked = months_worked))
annual_taxes_with_bonus = total_income - annual_take_home_with_bonus

bonus_taxes = annual_taxes_with_bonus - annual_taxes_no_bonus
# incremental tax caused by bonus
bonus_after_tax = annual_bonus - bonus_taxes
if bonus_after_tax > 0:
    st.write(f"Estimated after-tax bonus: ${bonus_after_tax:,.2f}")

# for each of these, add an estimated time to completion for goals
st.subheader("Recommendations:")


def build_user_context_data():
    return f"""
Here is the user's financial data:

Income:
- Annual income: {st.session_state.get("annual_income", 0)}
- Bonus: {st.session_state.get("annual_bonus", 0)}
- Months worked this calendar year: {st.session_state.get("months_worked", 12)}
- Monthly margin (take home - expenses): {st.session_state.get("monthly_margin")}

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
- Traditional 401k monthly: {st.session_state.get("trad_401k_contributions_monthly", 0)}
- Roth IRA monthly: {st.session_state.get("roth_ira_monthly", 0)}
- Roth 401k monthly: {st.session_state.get("roth_401k_contributions_monthly", 0)}

Goals:
- {st.session_state.get("goals", [])}

User Preferences:
debt agression (or willingness to pay extra on debt): {st.session_state.get("debt_aggression", "extremely")}
Importance of having 3-6 months of expenses saved: {st.session_state.get("emergency_importance", "extremely")}
Investing aggression: {st.session_state.get("investing_aggression", "balanced")}
Do they want to save, invest, or split bonus: {st.session_state.get("bonus_strategy", "save")}
"""

client = ai_recs()

user_context = build_user_context_data()

response = client.chat(
    messages=[
        {"role": "system", "content": user_context}
    ],
    stream=False
)

recommendations = clean_text(response.choices[0].message.content)

st.write(recommendations)

st.write(f"We recommend you withhold approximately ${recommended_withholding:,.2f} per month for federal income tax (excludes state/local & FICA).")
if bonus_taxes > 0:
    st.write(f"Estimated total tax on bonus (federal, state, FICA): ${bonus_taxes:,.2f}")
st.write("See the tax optimization page for more tax details/recommendations.")

st.subheader("Financial Planning:")
# single, no house yet
if st.session_state.marriage_status == "single" and st.session_state.home_balance == 0 and st.session_state.home_value == 0:
    st.markdown("""
This section simulates various scenarios to help you set goals and allocate your money effectively.

**NOTE:** This section assumes you never get a raise, never get married and combine income/assets, and never buy or pay off a home (which would increase your monthly margin). It also does **not** include your annual bonus. These assumptions are very unlikely to be true, so projections are likely underestimates depending on how these factors change over time.
""")
# single, house with mortgage
elif st.session_state.marriage_status == "single" and st.session_state.home_balance > 0 and st.session_state.home_value > 0:
    st.markdown("""
This section simulates various scenarios to help you set goals and allocate your money effectively.

**NOTE:** This section assumes you never get a raise, never get married and combine income/assets, and never pay off your home (which would increase your monthly margin).It also does **not** include your annual bonus. These assumptions are very unlikely to be true, so projections are likely underestimates depending on how these factors change over time.
""")
# single, house paid off
elif st.session_state.marriage_status == "single" and st.session_state.home_balance == 0 and st.session_state.home_value > 0:
    st.markdown("""
This section simulates various scenarios to help you set goals and allocate your money effectively.

**NOTE:** This section assumes you never get a raise and never get married and combine income/assets (which would increase your monthly margin). It also does **not** include your annual bonus. These assumptions are very unlikely to be true, so projections are likely underestimates depending on how these factors change over time.
""")
# married, no house yet
elif st.session_state.marriage_status == "married" and st.session_state.home_balance == 0 and st.session_state.home_value == 0:
    st.markdown("""
This section simulates various scenarios to help you set goals and allocate your money effectively.

**NOTE:** This section assumes you never get a raise and never buy or pay off a home (which would increase your monthly margin). It also does **not** include your annual bonus. These assumptions are very unlikely to be true, so projections are likely underestimates depending on how these factors change over time.
""")
# married, house with mortgage
elif st.session_state.marriage_status == "married" and st.session_state.home_balance > 0 and st.session_state.home_value > 0:
    st.markdown("""
This section simulates various scenarios to help you set goals and allocate your money effectively.

**NOTE:** This section assumes you never get a raise and never pay off your home (which would increase your monthly margin). These assumptions are very unlikely to be true, so projections are likely underestimates depending on how these factors change over time.
""")
# married, house paid off
elif st.session_state.marriage_status == "married" and st.session_state.home_balance == 0 and st.session_state.home_value > 0:
    st.markdown("""
This section simulates various scenarios to help you set goals and allocate your money effectively.

**NOTE:** This section assumes you never get a raise, which is very unlikely, and it does **not** include your annual bonus, so projections are likely underestimates.
""")
    
# now lets get all the user inputs:
# if user has debt:
if st.session_state.debt_df is not None and not st.session_state.debt_df.empty and st.session_state.debt_df["Balance"].sum() > 0:
    baseline_take_home = utils.calculate_monthly_take_home(single = single, annual_income = annual_income, trad_401k_contributions_monthly = 0, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc, months_worked = st.session_state.months_worked)
    baseline_monthly_margin = utils.calculate_monthly_margin(monthly_take_home = baseline_take_home, expenses_df = st.session_state.expenses_df, trad_401k_contributions_monthly = 0, months_worked = months_worked)
    st.write(f"Before any tax-adjusted investing, you will have approximately ${baseline_monthly_margin:,.2f} a month in margin.")
    margin_on_debt_monthly = st.slider("How much of your monthly margin would you like to put on your debt? (meaning, money in addition to minimum payments)", max_value=int(baseline_monthly_margin), step=1, value = st.session_state.margin_on_debt_monthly)
    st.write(f"You have ${baseline_monthly_margin - margin_on_debt_monthly:,.2f} monthly margin left after your monthly additional debt payment.")
    
else:
    # else no margin goes to debt
    baseline_take_home = utils.calculate_monthly_take_home(single = single, annual_income = annual_income, trad_401k_contributions_monthly = 0, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc, months_worked = st.session_state.months_worked)
    baseline_monthly_margin = utils.calculate_monthly_margin(monthly_take_home = baseline_take_home, expenses_df = st.session_state.expenses_df, trad_401k_contributions_monthly = 0, months_worked = months_worked)
    st.write(f"Before any investing, you will have approximately ${baseline_monthly_margin:,.2f} a month in margin.")
    margin_on_debt_monthly = 0
    
trad_401k_contributions_monthly = st.slider("How much would you like to contribute to your traditional 401k per month? (if you have a roth 401k, we recommend you max that out first)", max_value=int(baseline_monthly_margin - margin_on_debt_monthly), step=1, value = st.session_state.trad_401k_contributions_monthly)
trad_401k_match_monthly = 0
if trad_401k_contributions_monthly > 0:
    trad_401k_match_monthly = st.slider(f"How much will your employer match of the ${trad_401k_contributions_monthly} you put into your traditional 401k per month?", max_value = trad_401k_contributions_monthly, step=1, value = st.session_state.trad_401k_match_monthly)   

real_take_home = utils.calculate_monthly_take_home(single = single, annual_income = annual_income, trad_401k_contributions_monthly = trad_401k_contributions_monthly, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc, months_worked = st.session_state.months_worked)
real_monthly_margin = utils.calculate_monthly_margin(monthly_take_home = real_take_home, expenses_df = st.session_state.expenses_df, trad_401k_contributions_monthly = trad_401k_contributions_monthly, months_worked = months_worked)

# in debt:
if st.session_state.debt_df is not None and not st.session_state.debt_df.empty and st.session_state.debt_df["Balance"].sum() > 0:
    st.write(f"You have ${real_monthly_margin - margin_on_debt_monthly:,.2f} left after your monthly additional debt payment and 401k contributions.")
else:
    st.write(f"You have ${real_monthly_margin - margin_on_debt_monthly:,.2f} left after your monthly 401k contributions.")  


# retirement
roth_ira_monthly = st.slider("How much will you put into your roth (and/or traditional) ira a month?", max_value=int(real_monthly_margin - margin_on_debt_monthly - trad_401k_contributions_monthly), value = st.session_state.roth_ira_monthly)
st.write(f"You now have ${real_monthly_margin - margin_on_debt_monthly - roth_ira_monthly:,.2f} left a month.")
roth_401k_contributions_monthly = st.slider("How much will you put into a roth 401k a month? (ignore if you don't have a roth 401k).", max_value=int(real_monthly_margin - margin_on_debt_monthly - trad_401k_contributions_monthly - roth_ira_monthly), step=1, value = st.session_state.roth_401k_contributions_monthly)
st.write(f"You now have ${real_monthly_margin - margin_on_debt_monthly - roth_ira_monthly - roth_401k_contributions_monthly:,.2f} left a month.")
roth_401k_match_monthly = 0
if roth_401k_contributions_monthly > 0:
    roth_401k_match_monthly = st.slider(f"How much will your employer match of the ${roth_401k_contributions_monthly} you put into your roth 401k this month?", max_value = roth_401k_contributions_monthly, step=1, value = st.session_state.roth_401k_match_monthly)
st.session_state.roth_401k_match_monthly = roth_401k_match_monthly
years_from_retirement = st.slider("Approximately how much years are you from retirement?", value = st.session_state.years_from_retirement)

# formula for total in retirement: P(1+r)^t + PMT*(((1+r)^t -1))/r) -- P = current total, r = Annual interest rate (divided by 12 for monthly), t = Total number of years (multiplied by 12 for months), PMT = monthly investment amount
P = st.session_state.retirement
r_nominal = (st.session_state.retirement_returns / 100) / 12
r_real = ((1 + st.session_state.retirement_returns/100) / (1 + 0.04)) - 1
r_real = r_real / 12
t = years_from_retirement*12
PMT = trad_401k_contributions_monthly + trad_401k_match_monthly + roth_ira_monthly + roth_401k_contributions_monthly + roth_401k_match_monthly
if r_nominal == 0:
    total_in_retirement_nominal = P + t*PMT
else:
    total_in_retirement_nominal = P * (1 + r_nominal)**t + PMT * (((1 + r_nominal)**t - 1) / r_nominal)
if r_real == 0:
    total_in_retirement_real = P + PMT * t
else:
    total_in_retirement_real = P * (1 + r_real)**t + PMT * (((1 + r_real)**t - 1) / r_real)
st.write(f"You will have approximately ${total_in_retirement_nominal:,.2f} nominal in retirement when you retire. That is the equivalent of ${total_in_retirement_real:,.2f} today's value if we assume inflation will average 4% annually.")

# brokerage
st.write(f"You now have ${real_monthly_margin - margin_on_debt_monthly - roth_ira_monthly - roth_401k_contributions_monthly:,.2f} left a month.")
brokerage_contributions_monthly = st.slider("How much will you put into a your brokerage monthly?", max_value=int(real_monthly_margin - margin_on_debt_monthly - trad_401k_contributions_monthly - roth_ira_monthly - roth_401k_contributions_monthly), step=1, value = st.session_state.brokerage_contributions_monthly)
years_from_brokerage = st.slider("Approximately how much years are you from liquidating your brokerage?", value = st.session_state.years_from_brokerage)
P = st.session_state.brokerage
r_nominal = (st.session_state.brokerage_returns / 100) / 12
r_real = ((1 + st.session_state.brokerage_returns/100) / (1 + 0.04)) - 1
r_real = r_real / 12
t = years_from_brokerage*12
PMT = brokerage_contributions_monthly
if r_nominal == 0:
    total_in_brokerage_nominal = P + t*PMT
else:
    total_in_brokerage_nominal = P * (1 + r_nominal)**t + PMT * (((1 + r_nominal)**t - 1) / r_nominal)
if r_real == 0:
    total_in_brokerage_real = P + PMT * t
else:
    total_in_brokerage_real = P * (1 + r_real)**t + PMT * (((1 + r_real)**t - 1) / r_real)
st.write(f"You will have approximately ${total_in_brokerage_nominal:,.2f} nominal in your brokerage when you liquidate. That is the equivalent of ${total_in_brokerage_real:,.2f} today's value if we assume inflation will average 4% annually.")
#st.error if we go above margin (ADD in to above)
st.write(f"You now have ${real_monthly_margin - margin_on_debt_monthly - roth_ira_monthly - roth_401k_contributions_monthly - brokerage_contributions_monthly:,.2f} left a month for savings.")
future_savings_view = st.slider("How many months ahead would you like to look at your expected savings total?", max_value = 700, value = st.session_state.future_savings_view)
P = st.session_state.savings
r_nominal = (st.session_state.apy / 100) / 12
r_real = ((1 + st.session_state.apy/100) / (1 + 0.04)) - 1
r_real = r_real / 12
t = future_savings_view
PMT = real_monthly_margin - margin_on_debt_monthly - roth_ira_monthly - roth_401k_contributions_monthly - brokerage_contributions_monthly
if r_nominal == 0:
    total_in_savings_nominal = P + t*PMT
else:
    total_in_savings_nominal = P * (1 + r_nominal)**t + PMT * (((1 + r_nominal)**t - 1) / r_nominal)
if r_real == 0:
    total_in_savings_real = P + PMT * t
else:
    total_in_savings_real = P * (1 + r_real)**t + PMT * (((1 + r_real)**t - 1) / r_real)
st.write(f"In {future_savings_view} months,  you will have approximately ${total_in_savings_nominal:,.2f} saved. That is the equivalent of ${total_in_savings_real:,.2f} today's value.")

remaining = real_monthly_margin - margin_on_debt_monthly - roth_ira_monthly - roth_401k_contributions_monthly - brokerage_contributions_monthly
if remaining < 0:
    st.error("You are allocating more than your available monthly margin.")

if margin_on_debt_monthly == 0:
    dashboard_dict1 = {
        "Traditional 401k": f"${trad_401k_contributions_monthly:,.2f}",
        "Traditional 401k Match": f"${trad_401k_match_monthly:,.2f}",
        "Roth IRA": f"${roth_ira_monthly:,.2f}",
    }
    dashboard_df1 = pd.DataFrame(dashboard_dict1, index=[0])

    dashboard_dict2 = {
        "Roth 401k": f"${roth_401k_contributions_monthly:,.2f}",
        "Roth 401k Match": f"${roth_401k_match_monthly:,.2f}",
        "Brokerage": f"${brokerage_contributions_monthly:,.2f}",
        "Savings": f"${real_monthly_margin - margin_on_debt_monthly - roth_ira_monthly - roth_401k_contributions_monthly - brokerage_contributions_monthly:,.2f}",
    }
    dashboard_df2 = pd.DataFrame(dashboard_dict2, index=[0])
else:
    dashboard_dict1 = {
        "Debt Additional Contribution": f"${margin_on_debt_monthly:,.2f}",
        "Traditional 401k": f"${trad_401k_contributions_monthly:,.2f}",
        "Traditional 401k Match": f"${trad_401k_match_monthly:,.2f}",
        "Roth IRA": f"${roth_ira_monthly:,.2f}",
    }
    dashboard_df1 = pd.DataFrame(dashboard_dict1, index=[0])

    dashboard_dict2 = {
        "Roth 401k": f"${roth_401k_contributions_monthly:,.2f}",
        "Roth 401k Match": f"${roth_401k_match_monthly:,.2f}",
        "Brokerage": f"${brokerage_contributions_monthly:,.2f}",
        "Savings": f"${real_monthly_margin - margin_on_debt_monthly - roth_ira_monthly - roth_401k_contributions_monthly - brokerage_contributions_monthly:,.2f}",
    }
    dashboard_df2 = pd.DataFrame(dashboard_dict2, index=[0])

st.subheader("Monthly Margin Allocation Plan:")
st.dataframe(dashboard_df1) 
st.dataframe(dashboard_df2)

if st.button("Save dashboard projections values"):
    st.session_state.profile = {
        "email": st.session_state.email,
        "trad_401k_contributions_monthly": trad_401k_contributions_monthly,
        "trad_401k_match_monthly": trad_401k_match_monthly,
        "roth_ira_monthly": roth_ira_monthly,
        "roth_401k_contributions_monthly": roth_401k_contributions_monthly,
        "roth_401k_match_monthly": roth_401k_match_monthly,
        "years_from_retirement": years_from_retirement,
        "brokerage_contributions_monthly": brokerage_contributions_monthly,
        "years_from_brokerage": years_from_brokerage,
        "future_savings_view": future_savings_view
    }
    db = Database()
    user_id = db.get_user(st.session_state.email)["user_id"]
    db.update_dashboard(user_id, margin_on_debt_monthly, trad_401k_contributions_monthly, trad_401k_match_monthly, roth_ira_monthly, roth_401k_contributions_monthly, roth_401k_match_monthly, years_from_retirement, brokerage_contributions_monthly, years_from_brokerage, future_savings_view)
    st.success("Dashboard projection values saved!")

        

    
    

    




