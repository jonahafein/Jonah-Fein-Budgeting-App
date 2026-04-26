import pandas as pd
from supabase import create_client

class Database:
    def __init__(self):
        self.supabase = create_client(
            st.secrets["supabase_url"],
            st.secrets["publishable_key_supabase"]
        )
    
    def insert_user(self, email_input, birthdate):
        self.supabase.table("users").insert({
            "user_email": email_input,
            "birthdate": str(birthdate) if birthdate else None
        }).execute()
       
    def insert_non_home_assets(self, user_id, savings, apy, brokerage, brokerage_returns, retirement, retirement_returns):
        self.supabase.table("non_home_assets").upsert({
            "user_id": user_id,
            "savings": savings,
            "apy": apy,
            "brokerage": brokerage,
            "brokerage_returns": brokerage_returns,
            "retirement": retirement,
            "retirement_returns": retirement_returns
        }).execute()
    
    def insert_home(self, user_id, paid_off, home_value, years, balance, interest, fees):
        self.supabase.table("home").upsert({
            "user_id": user_id,
            "paid_off": paid_off,
            "home_value": home_value,
            "years": years,
            "balance": balance,
            "interest": interest,
            "fees": fees
        }).execute()
    
    def insert_goal(self, user_id, goal):
        self.supabase.table("goals").insert({
            "user_id": user_id,
            "goal": goal
        }).execute()
    
    def insert_debt(self, user_id, debt_item, debt_balance, debt_interest):
        self.supabase.table("debt").insert({
            "user_id": user_id,
            "debt_item": debt_item,
            "debt_balance": debt_balance,
            "debt_interest": debt_interest
        }).execute()
       
    def get_user(self, email):
        res = self.supabase.table("users") \
            .select("user_id, user_email, birthdate") \
            .eq("user_email", email) \
            .execute()
        
        if res.data:
            row = res.data[0]
            return {
                "user_id": row["user_id"],
                "email": row["user_email"],
                "birthdate": row["birthdate"]
            }
        
        return None
    
    def get_non_home_assets(self, user_id):
        res = self.supabase.table("non_home_assets") \
            .select("savings, apy, brokerage, brokerage_returns, retirement, retirement_returns") \
            .eq("user_id", user_id) \
            .execute()
        
        if res.data:
            row = res.data[0]
            return {
                "savings": float(row["savings"]) if row["savings"] is not None else 0,
                "apy": float(row["apy"]) if row["apy"] is not None else 0,
                "brokerage": float(row["brokerage"]) if row["brokerage"] is not None else 0,
                "brokerage_returns": float(row["brokerage_returns"]) if row["brokerage_returns"] is not None else 0,
                "retirement": float(row["retirement"]) if row["retirement"] is not None else 0,
                "retirement_returns": float(row["retirement_returns"]) if row["retirement_returns"] is not None else 0
            }
        
        return None
    
    def get_home(self, user_id):
        res = self.supabase.table("home") \
            .select("paid_off, home_value, years, balance, interest, fees") \
            .eq("user_id", user_id) \
            .execute()
        
        if res.data:
            row = res.data[0]
            return {
                "paid_off": bool(row["paid_off"]) if row["paid_off"] is not None else False,
                "home_value": float(row["home_value"]) if row["home_value"] is not None else 0,
                "years": int(row["years"]) if row["years"] is not None else 0,
                "balance": float(row["balance"]) if row["balance"] is not None else 0,
                "interest": float(row["interest"]) if row["interest"] is not None else 0,
                "fees": float(row["fees"]) if row["fees"] is not None else 0
            }
        
        return None
    
    def get_goals(self, user_id):
        res = self.supabase.table("goals") \
            .select("goal") \
            .eq("user_id", user_id) \
            .execute()
        
        if res.data:
            return [row["goal"] for row in res.data]
        
        return []
    
    def get_debts(self, user_id):
        res = self.supabase.table("debt") \
            .select("debt_item, debt_balance, debt_interest") \
            .eq("user_id", user_id) \
            .execute()
        
        if res.data:
            return [
                {
                    "debt_item": row["debt_item"] if row["debt_item"] is not None else None,
                    "debt_balance": float(row["debt_balance"]) if row["debt_balance"] is not None else 0,
                    "debt_interest": float(row["debt_interest"]) if row["debt_interest"] is not None else 0
                }
                for row in res.data
            ]
        
        return []
        
    def get_income(self, user_id):
        res = self.supabase.table("income") \
            .select("annual_income, annual_bonus, state_tax_perc, local_tax_perc, marriage_status, months_worked") \
            .eq("user_id", user_id) \
            .execute()
        
        if res.data:
            row = res.data[0]
            return {
                "annual_income": float(row["annual_income"]) if row["annual_income"] is not None else 0,
                "annual_bonus": float(row["annual_bonus"]) if row["annual_bonus"] is not None else 0,
                "state_tax_perc": float(row["state_tax_perc"]) if row["state_tax_perc"] is not None else 0,
                "local_tax_perc": float(row["local_tax_perc"]) if row["local_tax_perc"] is not None else 0,
                "marriage_status": row["marriage_status"] if row["marriage_status"] else "single",
                "months_worked": row["months_worked"] if row["months_worked"] else 12
            }
        
        return None
        
    def get_expenses(self, user_id):
        res = self.supabase.table("expenses") \
            .select("category, amount") \
            .eq("user_id", user_id) \
            .execute()
        
        if res.data:
            return [
                {
                    "category": row["category"] if row["category"] is not None else None,
                    "amount": float(row["amount"]) if row["amount"] is not None else 0
                }
                for row in res.data
            ]
        
        return []
        
    def get_dashboard(self, user_id):
        res = self.supabase.table("dashboard") \
            .select("trad_401k_contributions, trad_401k_match_annual, roth_ira_monthly, roth_401k_contributions_monthly, roth_401k_match_monthly, years_from_retirement, brokerage_contributions_monthly, years_from_brokerage, future_savings_view") \
            .eq("user_id", user_id) \
            .execute()
        
        if res.data:
            row = res.data[0]
            return {
                "trad_401k_contributions": row["trad_401k_contributions"] if row["trad_401k_contributions"] is not None else 0,
                "trad_401k_match_annual": row["trad_401k_match_annual"] if row["trad_401k_match_annual"] is not None else 0,
                "roth_ira_monthly": row["roth_ira_monthly"] if row["roth_ira_monthly"] is not None else 0,
                "roth_401k_contributions_monthly": row["roth_401k_contributions_monthly"] if row["roth_401k_contributions_monthly"] is not None else 0,
                "roth_401k_match_monthly": row["roth_401k_match_monthly"] if row["roth_401k_match_monthly"] is not None else 0,
                "years_from_retirement": row["years_from_retirement"] if row["years_from_retirement"] is not None else 0,
                "brokerage_contributions_monthly": row["brokerage_contributions_monthly"] if row["brokerage_contributions_monthly"] is not None else 0,
                "years_from_brokerage": row["years_from_brokerage"] if row["years_from_brokerage"] is not None else 0,
                "future_savings_view": row["future_savings_view"] if row["future_savings_view"] is not None else 0
            }
        
        return None
        
        
    # function for all:
    # I don't think I use this, and I haven't updated it 
    def get_profile(self, user_id):
        return{
            "non_home_assets": self.get_non_home_assets(user_id),
            "home": self.get_home(user_id),
            "goals": self.get_goals(user_id),
            "debts": self.get_debts(user_id)
        } 
        
    # TODO: implement the update methods
    def update_non_home_assets(self, user_id, savings, apy, brokerage, brokerage_returns, retirement, retirement_returns):
        self.supabase.table("non_home_assets").upsert({
            "user_id": user_id,
            "savings": savings,
            "apy": apy,
            "brokerage": brokerage,
            "brokerage_returns": brokerage_returns,
            "retirement": retirement,
            "retirement_returns": retirement_returns
        }).execute()
    
    def update_home(self, user_id, paid_off, home_value, years, balance, interest, fees):
        self.supabase.table("home").upsert({
            "user_id": user_id,
            "paid_off": paid_off,
            "home_value": home_value,
            "years": years,
            "balance": balance,
            "interest": interest,
            "fees": fees
        }).execute()
        
    def delete_home(self, user_id):
        self.supabase.table("home") \
            .delete() \
            .eq("user_id", user_id) \
            .execute()
    
    def update_goals(self, user_id, goals: list):
        # delete existing
        self.supabase.table("goals") \
            .delete() \
            .eq("user_id", user_id) \
            .execute()

        # insert new
        data = [{"user_id": user_id, "goal": goal} for goal in goals]

        if data:
            self.supabase.table("goals").insert(data).execute()
    
    def update_debts(self, user_id, debt_df):
        # delete existing
        self.supabase.table("debt") \
            .delete() \
            .eq("user_id", user_id) \
            .execute()

        # filter + build data
        data = []
        for _, row in debt_df.iterrows():
            if (
                pd.isna(row["Balance"]) or
                pd.isna(row["Interest Rate"]) or
                not row["Item"] or
                str(row["Item"]).strip() == ""
            ):
                continue

            data.append({
                "user_id": user_id,
                "debt_item": row["Item"],
                "debt_balance": row["Balance"],
                "debt_interest": row["Interest Rate"]
            })

        # insert
        if data:
            self.supabase.table("debt").insert(data).execute()
        
    def update_income(self, user_id, annual_income, annual_bonus, state_tax_perc, local_tax_perc, marriage_status, months_worked):
        self.supabase.table("income").upsert({
            "user_id": user_id,
            "annual_income": annual_income,
            "annual_bonus": annual_bonus,
            "state_tax_perc": state_tax_perc,
            "local_tax_perc": local_tax_perc,
            "marriage_status": marriage_status,
            "months_worked": months_worked
        }).execute()
    
    def update_expenses(self, user_id, expenses_df):
        # delete existing
        self.supabase.table("expenses") \
            .delete() \
            .eq("user_id", user_id) \
            .execute()

        # insert new
        data = [
            {
                "user_id": user_id,
                "category": row["category"],
                "amount": row["amount"]
            }
            for _, row in expenses_df.iterrows()
        ]

        if data:
            self.supabase.table("expenses").insert(data).execute()

    def update_birthdate(self, user_email, birthdate):
        self.supabase.table("users") \
            .update({
                "birthdate": str(birthdate) if birthdate else None
            }) \
            .eq("user_email", user_email) \
            .execute()
        
    def update_dashboard(
        self, user_id,
        trad_401k_contributions,
        trad_401k_match_annual,
        roth_ira_monthly,
        roth_401k_contributions_monthly,
        roth_401k_match_monthly,
        years_from_retirement,
        brokerage_contributions_monthly,
        years_from_brokerage,
        future_savings_view
    ):
        self.supabase.table("dashboard").upsert({
            "user_id": user_id,
            "trad_401k_contributions": trad_401k_contributions,
            "trad_401k_match_annual": trad_401k_match_annual,
            "roth_ira_monthly": roth_ira_monthly,
            "roth_401k_contributions_monthly": roth_401k_contributions_monthly,
            "roth_401k_match_monthly": roth_401k_match_monthly,
            "years_from_retirement": years_from_retirement,
            "brokerage_contributions_monthly": brokerage_contributions_monthly,
            "years_from_brokerage": years_from_brokerage,
            "future_savings_view": future_savings_view
        }).execute()

        
        
             
        
    