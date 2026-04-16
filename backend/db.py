import pandas as pd
from azure import identity
import struct, pyodbc
import config

class Database:
    def __init__(self):
        self.connection_string = config.connection_string
        
    # method needed to connect for other methods
    def get_conn(self):
        credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential = False)
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
            return {"savings": row[0], "apy": row[1], "brokerage": row[2], "brokerage_returns": row[3], "retirement": row[4], "retirement_returns": row[5]}
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
            return {"paid_off": row[0], "home_value": row[1], "years": row[2], "balance": row[3], "interest": row[4], "fees": row[5]}
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
            return [{"debt_item": row[0], "debt_balance": row[1], "debt_interest": row[2]} for row in rows]
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
        
    