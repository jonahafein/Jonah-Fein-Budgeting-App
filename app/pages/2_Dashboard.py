import streamlit as st 
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime

from backend.db import Database
import backend.utils

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
    
# snapshot
st.subheader("Your Current Financial Snapshot:")
net_worth = utils.calculate_net_worth(home_value = st.session_state.home_value, home_debt = st.session_state.home_balance, savings = st.session_state.savings, brokerage = st.session_state.brokerage, retirement = st.session_state.retirement, debt_total = st.session_state.debt_df["Balance"].sum())
st.write(f"Net Worth: ${net_worth:,.2f}")
# put some 401k slider in here
if continue_on_step4 == False:
    trad_401k_contributions = 0
    monthly_take_home = utils.calculate_monthly_take_home(single = single, annual_income = annual_income, trad_401k_contributions = trad_401k_contributions, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc, months_worked = st.session_state.months_worked)
    monthly_margin = utils.calculate_monthly_margin(monthly_take_home = monthly_take_home, expenses_df = st.session_state.expenses_df, trad_401k_contributions = trad_401k_contributions, months_worked = months_worked)
else:
    # TODO: implement slider for 401k contributions! (remember to get match in here)
    dummy_take_home = utils.calculate_monthly_take_home(single = single, annual_income = annual_income, trad_401k_contributions = 0, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc, months_worked = st.session_state.months_worked)
    dummy_monthly_margin = utils.calculate_monthly_margin(monthly_take_home = dummy_take_home, expenses_df = st.session_state.expenses_df, trad_401k_contributions = 0, months_worked = months_worked)
    trad_401k_contributions = st.slider("How much would you like to contribute to your traditional 401k this calendar year? (if you have a roth 401k, we recommend you max that out first). You will have a chance to input contributions to other accounts under financial projections.", max_value=int(12*(dummy_monthly_margin)), step=1, value = st.session_state.trad_401k_contributions)
    trad_401k_match_annual = 0
    if trad_401k_contributions > 0:
        trad_401k_match_annual = st.slider(f"How much will your employer match of the ${trad_401k_contributions} you put into your traditional 401k this year?", max_value = trad_401k_contributions, step=1, value = st.session_state.trad_401k_match_annual)
    st.session_state.trad_401k_match_annual = trad_401k_match_annual
    monthly_take_home = utils.calculate_monthly_take_home(single = single, annual_income = annual_income, trad_401k_contributions = trad_401k_contributions, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc, months_worked = st.session_state.months_worked)
    monthly_margin = utils.calculate_monthly_margin(monthly_take_home = monthly_take_home, expenses_df = st.session_state.expenses_df, trad_401k_contributions = trad_401k_contributions, months_worked = months_worked)
st.write(f"Your monthly margin (post traditional 401k): ${monthly_margin}")
# check or x if reached, if x by how much
st.write(f"3 month emergency fund: ${three_month_expenses:,.2f}", three_month_expenses_met)
st.write(f"6 month emergency fund: ${six_month_expenses:,.2f}", six_month_expenses_met)
if st.session_state.debt_df is not None and not st.session_state.debt_df.empty and st.session_state.debt_df["Balance"].sum() > 0:
    st.write(f"Your debt: ${st.session_state.debt_df["Balance"].sum()} with average interest: {np.average(st.session_state.debt_df['Interest Rate'], weights=st.session_state.debt_df['Balance']):,.2f}") 
else:
    st.write("You are not in debt!")
if st.session_state.savings > six_month_expenses:
    st.write(f"You have ${st.session_state.savings - six_month_expenses:,.2f} in savings that exceed your 6 month emergency fund (i.e., regular savings).")
age = datetime.today().date() - st.session_state.birthdate

salary_income_prorated = st.session_state.annual_income * (months_worked / 12)
salary_taxable = utils.get_annual_federal_taxable_income(annual_income = salary_income_prorated,trad_401k_contributions = trad_401k_contributions,standard_deduction = standard_deduction)
salary_federal_tax = utils.calculate_federal_tax(single = single,annual_federal_taxable_income = salary_taxable)
recommended_withholding = salary_federal_tax / months_worked
# total income with bonus
annual_take_home_no_bonus = months_worked*(utils.calculate_monthly_take_home(single = single, annual_income = annual_income,trad_401k_contributions = trad_401k_contributions, standard_deduction = standard_deduction, state_tax_perc = state_tax_perc, local_tax_perc = local_tax_perc, months_worked = months_worked))
annual_taxes_no_bonus = salary_income_prorated - annual_take_home_no_bonus
adjusted_total_income = st.session_state.annual_income + (annual_bonus * (12 / months_worked))
total_income = salary_income_prorated + annual_bonus
annual_take_home_with_bonus = months_worked*(utils.calculate_monthly_take_home(single = single, annual_income = adjusted_total_income,trad_401k_contributions = trad_401k_contributions, standard_deduction = standard_deduction, state_tax_perc = state_tax_perc, local_tax_perc = local_tax_perc, months_worked = months_worked))
annual_taxes_with_bonus = total_income - annual_take_home_with_bonus

bonus_taxes = annual_taxes_with_bonus - annual_taxes_no_bonus
# incremental tax caused by bonus
bonus_after_tax = annual_bonus - bonus_taxes
if bonus_after_tax > 0:
    st.write(f"Estimated after-tax bonus: ${bonus_after_tax:,.2f}")

# for each of these, add an estimated time to completion for goals
st.subheader("Recommendations:")

# baby step 1
if st.session_state.savings < 1000:
    st.write("We recommend that for now, you pause investing (including for retirement), and put all of your monthly margin towards building a $1000 starter emergency fund.")
    monthly_take_home = utils.calculate_monthly_take_home(single = single, annual_income = annual_income, trad_401k_contributions = 0, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc, months_worked = st.session_state.months_worked)
    monthly_margin = utils.calculate_monthly_margin(monthly_take_home = monthly_take_home, expenses_df = st.session_state.expenses_df, trad_401k_contributions = trad_401k_contributions, months_worked = months_worked)
    st.write(f"Your monthly margin this month should be roughly {monthly_margin:,.2f} dollars (assuming no investing). It should take you about {max((1000-st.session_state.savings)/max(monthly_margin,1),1)} months to achieve this.")
# baby step 2 
# TODO: change to first recommend using savings to get out of debt, and if that isnt enough then we use margin
elif "debt_df" in st.session_state and not st.session_state.debt_df.empty and st.session_state.savings >= 1000:
    highest_interest_debt = st.session_state.debt_df.loc[st.session_state.debt_df['Interest Rate'].idxmax()]['Item'] 
    monthly_take_home = utils.calculate_monthly_take_home(single = single, annual_income = annual_income, trad_401k_contributions = 0, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc, months_worked = st.session_state.months_worked)
    monthly_margin = utils.calculate_monthly_margin(monthly_take_home = monthly_take_home, expenses_df = st.session_state.expenses_df, trad_401k_contributions = trad_401k_contributions, months_worked = months_worked)
    if st.session_state.savings > 1000:
        st.write(f"We recommend you take ${st.session_state.savings - 1000:,.2f} from your savings and put in on your debt starting with {highest_interest_debt}.")
        difference = st.session_state.savings - 1000
        if difference < st.session_state.debt_df["Balance"].sum():
            st.write(f"Next, we recommend you temporarily pause all saving and investing (including retirement) and put your entire monthly margin at your non-mortgage debt, starting with {highest_interest_debt} as it is your highest interest debt.")
            st.write(f"Your monthly margin this month should be roughly ${monthly_margin:,.2f} dollars (assuming no investing). It should take you about {max((max(st.session_state.debt_df["Balance"].sum() - difference),0)/max(monthly_margin,1), 1):,.0f} months to be out of debt.")
        elif difference >= st.session_state.debt_df["Balance"].sum() and difference < three_month_expenses:
            st.write("You should be out of debt after that step!")
            st.write("Now, we recommend you temporarily pause all saving and investing (including retirement) and put your entire monthly margin at building up at least 3 months of expenses in savings.")
            savings_remainder = st.session_state.savings - st.session_state.debt_df["Balance"].sum()
            st.write(f"You should now have roughly ${savings_remainder:,.2f} savings with a monthly margin of ${monthly_margin:,.2f} (assuming no investing). Three months of expenses for you is approximately ${three_month_expenses:,.2f}. It should take you roughly {max((three_month_expenses - savings_remainder)/max(monthly_margin,1), 1):.0f} months to have 3 months of expenses saved.")
        else:
            st.write("You should now be out of debt and have over three months of expenses saved!")
# baby step 3
elif "debt_df" in st.session_state and st.session_state.debt_df.empty and st.session_state.savings < three_month_expenses:
    monthly_take_home = utils.calculate_monthly_take_home(single = single, annual_income = annual_income, trad_401k_contributions = 0, standard_deduction = standard_deduction, state_tax_perc = st.session_state.state_tax_perc, local_tax_perc = st.session_state.local_tax_perc, months_worked = st.session_state.months_worked)
    monthly_margin = utils.calculate_monthly_margin(monthly_take_home = monthly_take_home, expenses_df = st.session_state.expenses_df, trad_401k_contributions = trad_401k_contributions, months_worked = months_worked)
    st.write("We recommend you temporarily pause all saving and investing (including retirement) and put your entire monthly margin at building up at least 3 months of expenses in savings.")
    st.write(f"You current have ${st.session_state.savings:,.2f} in savings with a monthly margin of ${monthly_margin:,.2f} (assuming no investing). Three months of expenses for you is approximately ${three_month_expenses:,.2f}, meaning you are {three_month_gap:,.2f} dollars away. It should take you about {max(three_month_gap/max(monthly_margin,1), 1):.0f} months to reach this goal.")
# next build up to 6 months of emergency, maybe now with option to choose agressiveness towards saving vs investing
elif continue_on_step4:
    # TODO: logic for house, logic for moving on to step 7 (will need bool defined above and mutable here), slider for investing aggression, saving up to 6 mo, etc.
    # have active mortgage
    if st.session_state.home_balance > 0 and st.session_state.home_value > 0:
        st.write("Congratulations! You aren't in debt. We recommend you invest roughly 15% of your annual income into retirement, and put some of your extra margin on paying off your house early.")
        fifteen_perc_annual = float(0.15*st.session_state.annual_income)
        fifteen_perc_monthly = float(fifteen_perc_annual/12)
        st.write(f"15% of your annual income is ${fifteen_perc_annual:,.2f} which is roughly ${fifteen_perc_monthly:,.2f} a month.")
        if st.session_state.trad_401k_contributions/12 + st.session_state.roth_ira_monthly + st.session_state.roth_401k_contributions_monthly < fifteen_perc_monthly:
            difference = fifteen_perc_monthly - (st.session_state.trad_401k_contributions/12 + st.session_state.roth_ira_monthly + st.session_state.roth_401k_contributions_monthly)
            st.write(f"Warning ⛔️: You are investing ${difference:,.2f} a month less than 15% of your monthly income. We recommend you close the gap.")
    # have no mortgage but no house yet
    elif st.session_state.home_balance == 0 and st.session_state.home_value == 0:
        st.write("Congratulations! You aren't in debt. We recommend you invest roughly 15% of your annual income into retirement, and put a large portion of your additional margin on saving for a down payment on a house. If you plan on buying a home within 3-4 years, we recommend you put all of this money in a high yield savings account, otherwise we recommend you invest some of this money and save some of it.")
        fifteen_perc_annual = float(0.15*st.session_state.annual_income)
        fifteen_perc_monthly = float(fifteen_perc_annual/12)
        st.write(f"15% of your annual income is ${fifteen_perc_annual:,.2f} which is roughly ${fifteen_perc_monthly:,.2f} a month.")
        if st.session_state.trad_401k_contributions/12 + st.session_state.roth_ira_monthly + st.session_state.roth_401k_contributions_monthly < fifteen_perc_monthly:
            difference = fifteen_perc_monthly - (st.session_state.trad_401k_contributions/12 + st.session_state.roth_ira_monthly + st.session_state.roth_401k_contributions_monthly)
            st.write(f"Warning ⛔️: You are investing ${difference:,.2f} a month less than 15% of your monthly income. We recommend you close the gap.")
    elif  st.session_state.home_balance == 0 and st.session_state.home_value > 0:
        st.write("Congratulations! You aren't in debt including your house! We recommend you invest at least 15% of your annual income into retirement. Otherwise, make sure to keep saving, enjoying, and being generous with the rest of your margin!")
        fifteen_perc_annual = float(0.15*st.session_state.annual_income)
        fifteen_perc_monthly = float(fifteen_perc_annual/12)
        st.write(f"15% of your annual income is ${fifteen_perc_annual:,.2f} which is roughly ${fifteen_perc_monthly:,.2f} a month.")
        if st.session_state.trad_401k_contributions/12 + st.session_state.roth_ira_monthly + st.session_state.roth_401k_contributions_monthly < fifteen_perc_monthly:
            difference = fifteen_perc_monthly - (st.session_state.trad_401k_contributions/12 + st.session_state.roth_ira_monthly + st.session_state.roth_401k_contributions_monthly)
            st.write(f"Warning ⛔️: You are investing ${difference:,.2f} a month less than 15% of your monthly income. We recommend you close the gap.")

st.write(f"We recommend you withhold approximately ${recommended_withholding:,.2f} per month for federal income tax (excludes state/local & FICA).")
if bonus_taxes > 0:
    st.write(f"Estimated total tax on bonus (federal, state, FICA): ${bonus_taxes:,.2f}")
st.write("See the tax optimization page for more tax details/recommendations.")

st.subheader("Financial Projections:")
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
    
if continue_on_step4:
    st.write(f"Recall, under the assumption that you put ${trad_401k_contributions:,.2f} annually (which is ${float(trad_401k_contributions/months_worked):,.2f} a month) into a traditional 401k this year, you will have ${monthly_margin:,.2f} left a month. (Note: margin here is defined as post traditional 401k contributions).")
    roth_ira_monthly = st.slider("How much will you put into your roth (and/or traditional) ira a month?", max_value=int(monthly_margin), value = st.session_state.roth_ira_monthly)
    roth_401k_contributions_monthly = st.slider("How much will you put into a roth 401k a month? (ignore if you don't have a roth 401k).", max_value=int(monthly_margin - roth_ira_monthly), step=1, value = st.session_state.roth_401k_contributions_monthly)
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
    PMT = trad_401k_contributions/months_worked + trad_401k_match_annual/months_worked + roth_ira_monthly + roth_401k_contributions_monthly + roth_401k_match_monthly
    if r_nominal == 0:
        total_in_retirement_nominal = P + t*PMT
    else:
        total_in_retirement_nominal = P * (1 + r_nominal)**t + PMT * (((1 + r_nominal)**t - 1) / r_nominal)
    if r_real == 0:
        total_in_retirement_real = P + PMT * t
    else:
        total_in_retirement_real = P * (1 + r_real)**t + PMT * (((1 + r_real)**t - 1) / r_real)
    st.write(f"You will have approximately ${total_in_retirement_nominal:,.2f} nominal in retirement when you retire. That is the equivalent of ${total_in_retirement_real:,.2f} today's value if we assume inflation will average 4% annually.")
    # now brokerage, and remainder savings
    st.write(f"Margin left after retirement investing: ${monthly_margin - roth_ira_monthly - roth_401k_contributions_monthly:,.2f}")
    brokerage_contributions_monthly = st.slider("How much will you put into a your brokerage monthly?", max_value=int(monthly_margin - roth_ira_monthly - roth_401k_contributions_monthly), step=1, value = st.session_state.brokerage_contributions_monthly)
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
    st.write(f"Under this plan, after all investing you will have ${monthly_margin - roth_ira_monthly - roth_401k_contributions_monthly - brokerage_contributions_monthly:,.2f} for savings or further spending (once again, not including bonus).")
    future_savings_view = st.slider("How many months ahead would you like to look at your expected savings total?", max_value = 700, value = st.session_state.future_savings_view)
    P = st.session_state.savings
    r_nominal = (st.session_state.apy / 100) / 12
    r_real = ((1 + st.session_state.apy/100) / (1 + 0.04)) - 1
    r_real = r_real / 12
    t = future_savings_view
    PMT = monthly_margin - roth_ira_monthly - roth_401k_contributions_monthly - brokerage_contributions_monthly
    if r_nominal == 0:
        total_in_savings_nominal = P + t*PMT
    else:
        total_in_savings_nominal = P * (1 + r_nominal)**t + PMT * (((1 + r_nominal)**t - 1) / r_nominal)
    if r_real == 0:
        total_in_savings_real = P + PMT * t
    else:
        total_in_savings_real = P * (1 + r_real)**t + PMT * (((1 + r_real)**t - 1) / r_real)
    st.write(f"In {future_savings_view} months,  you will have approximately ${total_in_savings_nominal:,.2f}. That is the equivalent of ${total_in_savings_real:,.2f} today's value.")
    if st.button("Save dashboard projections values"):
        st.session_state.profile = {
            "email": st.session_state.email,
            "trad_401k_contributions": trad_401k_contributions,
            "trad_401k_match_annual": trad_401k_match_annual,
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
        db.update_dashboard(user_id, trad_401k_contributions, trad_401k_match_annual, roth_ira_monthly, roth_401k_contributions_monthly, roth_401k_match_monthly, years_from_retirement, brokerage_contributions_monthly, years_from_brokerage, future_savings_view)
        st.success("Dashboard projection values saved!")
else:
    if st.session_state.debt_df["Balance"].sum() > 0:
        st.write("NOTE: This section will be left blank for now until you are fully out of debt and have built up at least 3 months of expenses saved.")
    elif st.session_state.debt_df["Balance"].sum() == 0 and st.session_state.savings < three_month_expenses:
        st.write("NOTE: This section will be left blank for now until you have built up at least 3 months of expenses saved.")
        

    
    

    




