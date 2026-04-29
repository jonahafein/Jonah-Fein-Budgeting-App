import pandas as pd
from decimal import Decimal

def get_annual_federal_taxable_income(annual_income, trad_401k_contributions, standard_deduction):
    taxable = annual_income - trad_401k_contributions - standard_deduction
    return max(0, taxable)
    

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

    
def calculate_monthly_take_home(single: bool, annual_income,trad_401k_contributions, standard_deduction, state_tax_perc, local_tax_perc, months_worked = 12):
    # federal income taxes
    months_worked = max(months_worked, 1)
    actual_income = annual_income * (months_worked / 12)
    annual_taxable_income = actual_income
    
    annual_federal_taxable_income = get_annual_federal_taxable_income(annual_taxable_income, trad_401k_contributions, standard_deduction)
    annual_federal_income_tax = calculate_federal_tax(single, annual_federal_taxable_income)

    # ss:
    ss_cap_2026 = 184500
    if actual_income < ss_cap_2026:
        ss_costs = actual_income*0.062
    else:
        ss_costs = ss_cap_2026*0.062
    
    # medicare:
    if single:
        if  actual_income <= 200000:
            medicare_cost = actual_income*0.0145
        else:
            amount_over = actual_income - 200000
            medicare_cost_over_200k = amount_over*0.0235
            medicare_cost_under_200k = 200000*0.0145
            medicare_cost = medicare_cost_over_200k + medicare_cost_under_200k
    else:
        if  actual_income <= 250000:
            medicare_cost = actual_income*0.0145
        else:
            amount_over = actual_income - 250000
            medicare_cost_over_250k = amount_over*0.0235
            medicare_cost_under_250k = 250000*0.0145
            medicare_cost = medicare_cost_over_250k + medicare_cost_under_250k
    
    # state and local taxes
    state_tax = actual_income*(state_tax_perc/100)
    local_tax = actual_income*(local_tax_perc/100)
    
    # total annual tax
    annual_tax = annual_federal_income_tax + ss_costs + medicare_cost + state_tax + local_tax
    # monthly take home
    return (actual_income - annual_tax) / months_worked
      

def calculate_monthly_margin(monthly_take_home, expenses_df, trad_401k_contributions, months_worked):
    months_worked = max(months_worked, 1)
    if expenses_df is None or expenses_df.empty:
        return monthly_take_home - trad_401k_contributions/months_worked
    expense_total = expenses_df["amount"].sum()
    return round(monthly_take_home - expense_total - trad_401k_contributions/months_worked,2)

def calculate_net_worth(home_value, home_debt, savings, brokerage, retirement, debt_total):
    home_equity = home_value - home_debt
    return home_equity + savings + brokerage + retirement - debt_total

def calculate_federal_marginal_tax_rate(single: bool, annual_federal_taxable_income):
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
        
    for limit, tax_rate in brackets:
        if annual_federal_taxable_income <= limit:
            return tax_rate
        
def calculate_overall_marginal_tax_rate(single: bool, annual_federal_taxable_income, annual_income, months_worked, state_tax_perc, local_tax_perc):
    federal_marginal_tax_rate = calculate_federal_marginal_tax_rate(single = single, annual_federal_taxable_income = annual_federal_taxable_income)
    ss_cap_2026 = 184500
    actual_income = annual_income*(months_worked/12)
    if actual_income < ss_cap_2026:
        ss_marginal_rate = 0.062
    else:
        ss_marginal_rate = 0
        
    state_marginal_tax_rate = state_tax_perc / 100
    local_marginal_tax_rate = local_tax_perc / 100
    
        # medicare:
    if single:
        if  actual_income < 200000:
            medicare_marginal_rate = 0.0145
        else:
            medicare_marginal_rate = 0.0235

    else:
        if  actual_income < 250000:
            medicare_marginal_rate = 0.0145
        else:
            medicare_marginal_rate = 0.0235
            
    return federal_marginal_tax_rate + ss_marginal_rate + state_marginal_tax_rate + local_marginal_tax_rate + medicare_marginal_rate

def calculate_ss_annual(actual_income):
    ss_cap_2026 = 184500
    if actual_income < ss_cap_2026:
        ss_costs = actual_income*0.062
    else:
        ss_costs = ss_cap_2026*0.062
        
    return ss_costs

def calculate_medicare_costs(single: bool, actual_income):
    # medicare:
    if single:
        if  actual_income <= 200000:
            medicare_cost = actual_income*0.0145
        else:
            amount_over = actual_income - 200000
            medicare_cost_over_200k = amount_over*0.0235
            medicare_cost_under_200k = 200000*0.0145
            medicare_cost = medicare_cost_over_200k + medicare_cost_under_200k
    else:
        if  actual_income <= 250000:
            medicare_cost = actual_income*0.0145
        else:
            amount_over = actual_income - 250000
            medicare_cost_over_250k = amount_over*0.0235
            medicare_cost_under_250k = 250000*0.0145
            medicare_cost = medicare_cost_over_250k + medicare_cost_under_250k
            
    return medicare_cost

           
     
