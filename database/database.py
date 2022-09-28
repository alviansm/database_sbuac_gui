import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, nama text, customer text, retailer text, price text)"
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()