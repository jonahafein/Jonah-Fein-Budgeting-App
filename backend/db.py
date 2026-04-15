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
    
    def insert_user(email):
       conn = Database().get_conn()
       cursor = conn.cursor()
       cursor.execute("INSERT INTO users (user_email) VALUES (?)", email)
       conn.commit() 
       cursor.close()
       conn.close()
       
    def get_user(email):
        conn = Database.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_email = ?", email)
        user = cursor.fetchall()
        cursor.close()
        conn.close()
        return user
    
# test = Database()
# conn = test.get_conn()
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM dbo.users")
# rows = cursor.fetchall()
# print(rows)
# cursor.close()
# conn.close()