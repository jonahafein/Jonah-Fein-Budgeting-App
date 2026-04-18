import pandas as pd
from azure import identity
import struct, pyodbc
import config

class Database:
    def __init__(self):
        self.connection_string = config.connection_string
        
    # method needed to connect for other methods
    def get_conn(self):
        credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential = True)
        token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
        conn = pyodbc.connect(self.connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
        return conn
    
    
    def insert_user(self, email):
       conn = self.get_conn()
       cursor = conn.cursor()
       cursor.execute("INSERT INTO users (user_email) VALUES (?)", email)
       conn.commit() 
       cursor.close()
       conn.close()
       
    def insert_non_home_assets(self, user_id, savings, apy, brokerage, brokerage_returns, retirement, retirement_returns):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO non_home_assets (user_id, savings, apy, brokerage, brokerage_returns, retirement, retirement_returns) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       user_id, savings, apy, brokerage, brokerage_returns, retirement, retirement_returns)
        conn.commit()
        cursor.close()
        conn.close()
    
    def insert_home(self, user_id, paid_off, home_value, years, balance, interest, fees):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO home (user_id, paid_off, home_value, years, balance, interest, fees) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       user_id, paid_off, home_value, years, balance, interest, fees)
        conn.commit()
        cursor.close()
        conn.close()
    
    def insert_goal(self, user_id, goal):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO goals (user_id, goal) VALUES (?, ?)", 
                       user_id, goal)
        conn.commit()
        cursor.close()
        conn.close()
    
    def insert_debt(self, user_id, debt_item, debt_balance, debt_interest):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO debt (user_id, debt_item, debt_balance, debt_interest) VALUES (?, ?, ?, ?)", 
                       user_id, debt_item, debt_balance, debt_interest)
        conn.commit()
        cursor.close()
        conn.close()
       
    def get_user(self, email):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, user_email FROM users WHERE user_email = ?", email)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return {"user_id": row[0], "email": row[1]}
        return None 
    
    def get_non_home_assets(self, user_id):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT savings, apy, brokerage, brokerage_returns, retirement, retirement_returns FROM non_home_assets WHERE user_id = ?", user_id)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return {"savings": float(row[0]) if row[0] is not None else 0, "apy": float(row[1]) if row[1] is not None else 0, "brokerage": float(row[2]) if row[2] is not None else 0, "brokerage_returns": float(row[3]) if row[3] is not None else 0, "retirement": float(row[4]) if row[4] is not None else 0, "retirement_returns": float(row[5]) if row[5] is not None else 0}
        else:
            return None
    
    def get_home(self, user_id):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT paid_off, home_value, years, balance, interest, fees FROM home WHERE user_id = ?", user_id)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return {"paid_off": bool(row[0]) if row[0] is not None else False, "home_value": float(row[1]) if row[1] is not None else 0, "years": int(row[2]) if row[2] is not None else 0, "balance": float(row[3]) if row[3] is not None else 0, "interest": float(row[4]) if row[4] is not None else 0, "fees": float(row[5]) if row[5] is not None else 0}
        else:
            return None
    
    def get_goals(self, user_id):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT goal FROM goals WHERE user_id = ?", user_id)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows:
            return [row[0] for row in rows]
        else: 
            return [] 
    
    def get_debts(self, user_id):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT debt_item, debt_balance, debt_interest FROM debt WHERE user_id = ?", user_id)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows:
            return [{"debt_item": row[0] if row[0] is not None else None, "debt_balance": float(row[1]) if row[1] is not None else 0, "debt_interest": float(row[2]) if row[2] is not None else 0} for row in rows]
        else:
            return []  
        
    def get_income(self, user_id):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT annual_income, annual_bonus FROM income WHERE user_id = ?", user_id)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return {"annual_income": float(row[0]) if row[0] is not None else 0, "annual_bonus": float(row[1]) if row[1] is not None else 0}
        else:
            return None
        
    def get_expenses(self, user_id):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT category, amount FROM expenses WHERE user_id = ?", user_id)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows:
            return [{"category": row[0] if row[0] is not None else None, "amount": float(row[1]) if row[1] is not None else 0} for row in rows]
        else:
            return []  
        
        
    # function for all:
    def get_profile(self, user_id):
        return{
            "non_home_assets": self.get_non_home_assets(user_id),
            "home": self.get_home(user_id),
            "goals": self.get_goals(user_id),
            "debts": self.get_debts(user_id)
        } 
        
    # TODO: implement the update methods
    def update_non_home_assets(self, user_id, savings, apy, brokerage, brokerage_returns, retirement, retirement_returns):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM non_home_assets WHERE user_id = ?", user_id)
        exists = cursor.fetchone()[0]
        
        if exists > 0:
            cursor.execute("UPDATE non_home_assets SET savings = ?, apy = ?, brokerage = ?, brokerage_returns = ?, retirement = ?, retirement_returns = ? WHERE user_id = ?",
                       savings, apy, brokerage, brokerage_returns, retirement, retirement_returns, user_id)
        else:
            cursor.execute("INSERT INTO non_home_assets (user_id, savings, apy, brokerage, brokerage_returns, retirement, retirement_returns) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       user_id, savings, apy, brokerage, brokerage_returns, retirement, retirement_returns)
        conn.commit()
        cursor.close()
        conn.close() 
    
    def update_home(self, user_id, paid_off, home_value, years, balance, interest, fees):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM home WHERE user_id = ?", user_id)
        exists = cursor.fetchone()[0]
        
        if exists > 0:
            cursor.execute("UPDATE home SET paid_off = ?, home_value = ?, years = ?, balance = ?, interest = ?, fees = ? WHERE user_id = ?", paid_off,
                           home_value, years, balance, interest, fees, user_id)
        else:
            cursor.execute("INSERT INTO home (user_id, paid_off, home_value, years, balance, interest, fees) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       user_id, paid_off, home_value, years, balance, interest, fees)
        conn.commit()
        cursor.close()
        conn.close()
        
    def delete_home(self, user_id):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM home WHERE user_id = ?", user_id)
        conn.commit()
        cursor.close()
        conn.close()
    
    def update_goals(self, user_id, goals: list):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM goals WHERE user_id = ?", user_id)        
        for goal in goals:
            cursor.execute("INSERT INTO goals (user_id, goal) VALUES (?, ?)", user_id, goal)
        conn.commit()
        cursor.close()
        conn.close()
    
    def update_debts(self, user_id, debt_df):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM debt WHERE user_id = ?", user_id)
        for _, row in debt_df.iterrows():
            cursor.execute("INSERT INTO debt (user_id, debt_item, debt_balance, debt_interest) VALUES (?, ?, ?, ?)", user_id,
                           row["Item"], row["Balance"], row["Interest Rate"])
        conn.commit()
        cursor.close()
        conn.close()
        
    def update_income(self, user_id, annual_income, annual_bonus):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM income WHERE user_id = ?", user_id)
        exists = cursor.fetchone()[0]
        
        if exists > 0:
            cursor.execute("UPDATE income SET annual_income = ?, annual_bonus = ? WHERE user_id = ?",
                       annual_income, annual_bonus, user_id)
        else:
            cursor.execute("INSERT INTO income (user_id, annual_income, annual_bonus) VALUES (?, ?, ?)",
                       user_id, annual_income, annual_bonus)
        conn.commit()
        cursor.close()
        conn.close() 
    
    def update_expenses(self,user_id, expenses_df):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE user_id = ?", user_id)
        for _, row in expenses_df.iterrows():
            cursor.execute("INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?)", user_id,
                           row["category"], row["amount"])
        conn.commit()
        cursor.close()
        conn.close()
        
             
        
    