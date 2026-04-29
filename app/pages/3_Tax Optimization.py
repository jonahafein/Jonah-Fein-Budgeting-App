import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.db import Database
import backend.utils as utils

if not st.session_state.get("email"):
    st.warning("Please log in first")
    st.stop()

st.title("Tax Optimization")
st.write("The goal of this page is to help you pay as close to the right amount of taxes monthly as possible. Getting a big tax refund is actually a bad thing - it means you loaned money to the government at 0% interest! Note: input your monthly traditional 401k contributions into dashboard before continuing (and then save) as that will have implications on your taxes.")

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
trad_401k_contributions_monthly = dashboard["trad_401k_contributions_monthly"] if dashboard else 0
trad_401k_match_monthly = dashboard["trad_401k_match_monthly"] if dashboard else 0
roth_ira_monthly = dashboard["roth_ira_monthly"] if dashboard else 0
roth_401k_contributions_monthly = dashboard["roth_401k_contributions_monthly"] if dashboard else 0
roth_401k_match_monthly = dashboard["roth_401k_match_monthly"] if dashboard else 0
years_from_retirement = dashboard["years_from_retirement"] if dashboard else 0
brokerage_contributions_monthly = dashboard["brokerage_contributions_monthly"] if dashboard else 0
years_from_brokerage = dashboard["years_from_brokerage"] if dashboard else 0
future_savings_view = dashboard["future_savings_view"] if dashboard else 0

st.session_state.trad_401k_contributions_monthly = trad_401k_contributions_monthly if trad_401k_contributions_monthly else 0
st.session_state.trad_401k_match_monthly = trad_401k_match_monthly if trad_401k_match_monthly else 0
st.session_state.roth_ira_monthly = roth_ira_monthly if roth_ira_monthly else 0
st.session_state.roth_401k_contributions_monthly = roth_401k_contributions_monthly if roth_401k_contributions_monthly else 0
st.session_state.roth_401k_match_monthly = roth_401k_match_monthly if roth_401k_match_monthly else 0
st.session_state.years_from_retirement = years_from_retirement if years_from_retirement else 0
st.session_state.brokerage_contributions_monthly = brokerage_contributions_monthly if brokerage_contributions_monthly else 0
st.session_state.years_from_brokerage = years_from_brokerage if years_from_brokerage else 0
st.session_state.future_savings_view = future_savings_view if future_savings_view else 0
    
if st.session_state.marriage_status =="single":
    standard_deduction = 16100
else:
    standard_deduction = 32200
    
if st.session_state.marriage_status =="single":
    single = True
else:
    single = False
    
annual_income = st.session_state.annual_income

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
st.write(f"NOTE: The following assumes you put ${trad_401k_contributions_monthly:,.2f} into your traditional 401k per month. If that is not the case, please update your contribution in dashboard, save, and return here for an accurate view.")



# now the stuff for the user
st.subheader("Tax Overview:")
st.write(f"Your federally taxable income (before bonus) based on a standard deduction of {standard_deduction} is approximately ${salary_taxable:,.2f}.")
st.write(f"This means you owe approximately ${salary_federal_tax:,.2f} in federal income tax (not including bonus), giving you a monthly average of ${float(salary_federal_tax/months_worked):,.2f}")
if salary_income_prorated > 0:
    effective_tax_rate = float(annual_taxes_no_bonus/salary_income_prorated)
else:
    effective_tax_rate = 0.0
st.write(f"Your estimated effective total tax rate (not including bonus) is approximately {effective_tax_rate:.2%}.")
ss_costs = utils.calculate_ss_annual(actual_income = salary_income_prorated)
medicare_costs = utils.calculate_medicare_costs(single = single, actual_income = salary_income_prorated)
st.write(f"Of the ${annual_taxes_no_bonus:,.2f} you will pay in taxes this year (not including bonus), ${salary_federal_tax:,.2f} goes to federal income tax, ${ss_costs:,.2f} goes to social security, ${medicare_costs:,.2f} goes to medicare, ${salary_income_prorated*(state_tax_perc/100):,.2f} goes to state tax, and ${salary_income_prorated*(local_tax_perc/100):,.2f} goes to local tax.")
after_tax_income = salary_income_prorated - annual_taxes_no_bonus
monthly_take_home = after_tax_income/months_worked
st.write(f"Your monthly take home is approximately ${monthly_take_home:,.2f}.")
federal_marginal_tax_rate = utils.calculate_federal_marginal_tax_rate(single = single, annual_federal_taxable_income = salary_taxable)
st.write(f"Your federal income marginal tax rate is {federal_marginal_tax_rate:.2%}. That means if you invest another dollar into your traditional 401k, you will save ${federal_marginal_tax_rate:,.2f} in federal income tax (and potentially additional state tax).")
overall_marginal_tax_rate = utils.calculate_overall_marginal_tax_rate(single = single, annual_federal_taxable_income = salary_taxable, annual_income = annual_income, months_worked = months_worked, state_tax_perc = state_tax_perc, local_tax_perc = local_tax_perc)
st.write(f"Your overall marginal tax rate is {overall_marginal_tax_rate:.2%}. That means if you make another dollar, you will pay ${overall_marginal_tax_rate:,.2f} of tax on it. Note: contributing to traditional 401k only reduces federal income tax (and sometimes state tax).")
bonus_rate = bonus_taxes/annual_bonus if annual_bonus > 0 else 0
if annual_bonus > 0:
    st.write(f"Estimated total tax on bonus (federal, state, FICA): ${bonus_taxes:,.2f}. This means your bonus is taxed at approximately {bonus_rate:.2%}")

st.subheader("Recommendations:")
st.write("""
We recommend setting your federal withholding based on your salary only. 
This keeps your monthly withholding accurate and avoids relying on bonus timing.
""")
if months_worked < 12:
    payroll_annual_federal_taxable_estimate = utils.get_annual_federal_taxable_income(annual_income = annual_income, trad_401k_contributions_monthly = trad_401k_contributions_monthly, standard_deduction = standard_deduction, months_worked = months_worked)
    payroll_federal_tax_estimate = utils.calculate_federal_tax(single = single, annual_federal_taxable_income = payroll_annual_federal_taxable_estimate)
    monthly_payroll_federal_tax_estimate = payroll_federal_tax_estimate/12
    st.write(f"Based on your current paycheck, payroll may withhold approximately, payroll may withhold approximately ${months_worked*monthly_payroll_federal_tax_estimate:,.2f}.")
    st.write(f"Since you are working less than 12 months this calendar year, you are overpaying federal income tax by about ${months_worked*monthly_payroll_federal_tax_estimate - salary_federal_tax:,.2f}. To correct for this, you could enter approximately {max(months_worked*monthly_payroll_federal_tax_estimate - salary_federal_tax - 100, 0):,.0f} in Step 3 of your W-4. This will reduce your total withholding for the year and bring you closer to your true tax liability (with a small buffer to be safe).")
st.write("""
A small refund (a few hundred dollars) is normal and can act as a buffer against underpayment penalties. 
We do not recommend targeting a perfect $0 balance.
""")
st.write(f"We recommend you withhold approximately ${recommended_withholding:,.2f} per month for federal income tax (excludes state/local & FICA). This is based on your salary only and excludes bonus-related withholding.")

