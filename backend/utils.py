import pandas as pd
from decimal import Decimal

def get_annual_federal_taxable_income(annual_income, trad_401k_contributions, standard_deduction):
    taxable = annual_income - trad_401k_contributions - standard_deduction
    return max(0, taxable)

def get_annual_taxable_income_non_federal(annual_income, trad_401k_contributions):
    return max(annual_income - trad_401k_contributions, 0)
    

def calculate_federal_tax(single: bool, annual_federal_taxable_income):
    if annual_federal_taxable_income <= 0:
        return 0.0
    # federal income tax brackets
    if single:
        brackets = [
            (12400, 0.10),
            (50400, 0.12),
            (105700, 0.22),
            (201775, 0.24),
            (256225, 0.32),
            (640600, 0.35),
            (float('inf'), 0.37)
        ] 
    else:
        brackets = [
            (24800, 0.10),
            (100800, 0.12),
            (211400, 0.22),
            (403550, 0.24),
            (512450, 0.32),
            (768700, 0.35),
            (float('inf'), 0.37)
        ] 
        
    tax = 0.0
    prev_limit = 0
        
    for limit, tax_rate in brackets:
        if annual_federal_taxable_income > limit:
            tax += (limit - prev_limit)*tax_rate
            prev_limit = limit
        else:
            tax += (annual_federal_taxable_income - prev_limit)*tax_rate
            break
        
    return round(tax, 2)

    
def calculate_monthly_take_home(single: bool, annual_income, trad_401k_contributions, standard_deduction, state_tax_perc, local_tax_perc):
    # federal income taxes
    annual_federal_taxable_income = get_annual_federal_taxable_income(annual_income, trad_401k_contributions, standard_deduction)
    annual_federal_income_tax = calculate_federal_tax(single, annual_federal_taxable_income)
    
    # non federal tax
    annual_taxable_income_non_federal = get_annual_taxable_income_non_federal(annual_income, trad_401k_contributions)
    
    # ss:
    ss_cap_2026 = 184500
    if annual_taxable_income_non_federal < ss_cap_2026:
        ss_costs = annual_taxable_income_non_federal*0.062
    else:
        ss_costs = ss_cap_2026*0.062
    
    # medicare:
    if single:
        if  annual_taxable_income_non_federal <= 200000:
            medicare_cost = annual_taxable_income_non_federal*0.0145
        else:
            amount_over = annual_taxable_income_non_federal - 200000
            medicare_cost_over_200k = amount_over*0.0235
            medicare_cost_under_200k = 200000*0.0145
            medicare_cost = medicare_cost_over_200k + medicare_cost_under_200k
    else:
        if  annual_taxable_income_non_federal <= 250000:
            medicare_cost = annual_taxable_income_non_federal*0.0145
        else:
            amount_over = annual_taxable_income_non_federal - 250000
            medicare_cost_over_250k = amount_over*0.0235
            medicare_cost_under_250k = 250000*0.0145
            medicare_cost = medicare_cost_over_250k + medicare_cost_under_250k
    
    # state and local taxes
    state_tax = annual_taxable_income_non_federal*(state_tax_perc/100)
    local_tax = annual_taxable_income_non_federal*(local_tax_perc/100)
    
    # total annual tax
    annual_tax = annual_federal_income_tax + ss_costs + medicare_cost + state_tax + local_tax
    # monthly take home
    return (annual_income/12) - (annual_tax/12)
      

def calculate_monthly_margin(monthly_take_home, expenses_df):
    if expenses_df is None or expenses_df.empty:
        return monthly_take_home
    expense_total = expenses_df["amount"].sum()
    return round(monthly_take_home - expense_total,2)

def calculate_net_worth(home_value, home_debt, savings, brokerage, retirement, debt_total):
    home_equity = home_value - home_debt
    return home_equity + savings + brokerage + retirement - debt_total
