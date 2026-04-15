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
        #TODO
        pass
    
    def insert_home(self, user_id, paid_off, home_value, years, balance, interest, fees):
        #TODO
        pass
    
    def insert_goals(self, goals_id, user_id, goal):
        #TODO
        pass
    
    def insert_debt(self, debt_id, user_id, debt_item, debt_balance, debt_interest):
        #TODO
        pass
       
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
    