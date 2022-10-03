import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS projects 
            (
            id INTEGER, 
            project_name TEXT NOT NULL, 
            year INTEGER, 
            capacity INTEGER, 
            customer TEXT, 
            totals INTEGER, 
            image TEXT, 
            bom_id INTEGER AUTO INCREMENT,
            PRIMARY KEY (id)
            )'''
        )
        self.conn.commit()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS bom 
            (
            id INTEGER, 
            rev VARCHAR(6), 
            kode_material TEXT NOT NULL, 
            deskripsi TEXT, 
            spesifikasi TEXT, 
            kuantitas INTEGER, 
            satuan VARCHAR(12), 
            project_id INTEGER, 
            spp_id INTEGER, 
            po_id INTEGER, 
            keterangan BOOLEAN, 
            PRIMARY KEY (id),
            FOREIGN KEY (project_id) REFERENCES projects(id)
            )'''
        )
        self.conn.commit()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS spp 
            (
            id INTEGER, 
            nomor TEXT, 
            kuantitas DOUBLE, 
            satuan VARCHAR(12), 
            status BOOLEAN, 
            bom_id INTEGER, 
            po_id INTEGER,
            PRIMARY KEY (id)
            )'''
        )
        self.conn.commit()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS po 
            (
            id INTEGER, 
            nomor TEXT, 
            kuantitas DOUBLE, satuan VARCHAR(12), 
            kode TEXT, 
            tanggal_kedatangan DATETIME, 
            bom_id INTEGER, 
            spp_id INTEGER, 
            PRIMARY KEY (id)
            )'''
        )
        self.conn.commit()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS user_admin 
            (
            id INTEGER, 
            username TEXT,
            password TEXT, 
            PRIMARY KEY (id)
            )'''
        )
        self.conn.commit()

    # Fetch -> projects
    def fetch(self):
        self.cur.execute('''SELECT id, project_name, year, capacity, customer, totals FROM projects''')
        rows = self.cur.fetchall()  
        return rows

    # Insert -> projects
    def insert(self, project_name, year, capacity, customer, totals, image):
        self.cur.execute("INSERT INTO projects VALUES (NULL, ?, ?, ?, ?, ?, ?, NULL)", (project_name, year, capacity, customer, totals, image))
        self.conn.commit()

    # Remove -> projects
    def remove(self, id):
        self.cur.execute("DELETE FROM projets WHERE id=?", (id,))
        self.conn.commit()

    # Update -> projects
    def update(self, id, project_name, year, capacity, customer, totals):
        self.cur.execute("UPDATE projects SET project_name=?, year=?, capacity=?, customer=?, totals=? WHERE id=?", (project_name, year, capacity, customer, totals, id))
        self.conn.commit()

    # Query projects by year
    def search_by_year(self, year, name, id):
        sql = '''SELECT id, project_name, year, capacity, customer, totals FROM projects WHERE year=?'''
        try:
            params = [int(year)]
        except ValueError:            
            params = []
        
        if year == "SEMUA":
            sql = '''SELECT id, project_name, year, capacity, customer, totals FROM projects WHERE year > 0'''

        try:
            if int(id) > 0:
                sql += " AND id=?"
                params.append(int(id))
        except ValueError:
            params = params

        if str(name) != "":
            sql += ' AND project_name LIKE ?'
            params.append('%'+name+'%')
        tuple_params = tuple(params)
        self.cur.execute(sql, tuple_params)
        rows = self.cur.fetchall()
        return rows

    # Destructor -> projects
    def __del__(self):
        self.conn.close()