import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, project_name TEXT NOT NULL, year INTEGER, capacity INTEGER, customer TEXT, totals INTEGER, image TEXT)"
        )
        self.conn.commit()

    # Fetch -> projects
    def fetch(self):
        self.cur.execute("SELECT id, project_name, year, capacity, customer, totals FROM projects")
        rows = self.cur.fetchall()  
        return rows

    # Insert -> projects
    def insert(self, project_name, year, capacity, customer, totals, image):
        self.cur.execute("INSERT INTO projects VALUES (NULL, ?, ?, ?, ?, ?, ?)", (project_name, year, capacity, customer, totals, image))
        self.conn.commit()

    # Remove -> projects
    def remove(self, id):
        self.cur.execute("DELETE FROM projets WHERE id=?", (id,))
        self.conn.commit()

    # Update -> projects
    def update(self, id, project_name, year, capacity, customer, totals, image):
        self.cur.execute("UPDATE projects SET project_name=?, year=?, capacity=?, customer=?, totals=?, image=? WHERE id=?", (project_name, year, capacity, customer, totals, image, id))
        self.conn.commit()

    # Destructor -> projects
    def __del__(self):
        self.conn.close()

# db = Database("demo_projects.db")
# db.insert("Kereta Ukur HST", 2022, "40000", "PT KAI", 35, "./images/9q02ejo.png")