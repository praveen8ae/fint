
import sqlite3
from datetime import datetime

class BankDB:
    def __init__(self):
        self.conn = sqlite3.connect("fint.db")
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY,password TEXT,balance REAL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, amount REAL, timestamp TEXT)")
        self.cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO users VALUES ('admin','123456',10000)")
        self.conn.commit()

    def login(self,u,p):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
        return self.cursor.fetchone()

    def get_balance(self,u):
        self.cursor.execute("SELECT balance FROM users WHERE username=?", (u,))
        return self.cursor.fetchone()[0]

    def update_balance(self,u,b):
        self.cursor.execute("UPDATE users SET balance=? WHERE username=?", (b,u))
        self.conn.commit()

    def add_history(self,a,amt):
        self.cursor.execute("INSERT INTO history(action,amount,timestamp) VALUES(?,?,?)",(a,amt,datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.conn.commit()

    def get_history(self):
        self.cursor.execute("SELECT action,amount,timestamp FROM history ORDER BY id DESC LIMIT 20")
        return self.cursor.fetchall()
