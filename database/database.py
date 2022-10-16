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
            kuantitas DOUBLE, 
            satuan VARCHAR(12),
            filepath TEXT, 
            project_id INTEGER, 
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
            project_id INTEGER,
            bom_id INTEGER,
            PRIMARY KEY (id),
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (bom_id) REFERENCES bom(id)
            )'''
        )
        self.conn.commit()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS po 
            (
            id INTEGER, 
            nomor TEXT, 
            kuantitas DOUBLE, 
            satuan VARCHAR(12), 
            kode TEXT, 
            tanggal_kedatangan DATETIME,
            project_id INTEGER,
            bom_id INTEGER,
            PRIMARY KEY (id),
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (bom_id) REFERENCES bom(id)
            )'''
        )
        self.conn.commit()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS user_admin 
            (
            id INTEGER, 
            username TEXT,
            password TEXT, 
            time_created TEXT,
            PRIMARY KEY (id)
            )'''
        )
        self.conn.commit()

    # Fetch -> projects
    def fetch(self):
        self.cur.execute('''SELECT id, project_name, year, capacity, customer, totals FROM projects''')
        rows = self.cur.fetchall()  
        return rows
    # Fetch -> BOM
    def fetch_view_bom(self, project_id):
        self.cur.execute('''SELECT id, rev, kode_material, deskripsi, spesifikasi, kuantitas, satuan, keterangan FROM bom WHERE project_id = ?''', (project_id,))
        rows = self.cur.fetchall()
        return rows
    # Fetch bom datasheet
    def fetch_view_bom_datasheet(self, kode_material):
        self.cur.execute('''SELECT filepath FROM bom WHERE kode_material=?''', (kode_material,))
        row = self.cur.fetchone()
        return row
    # Fetch -> SPP
    def fetch_view_spp(self, bom_id, spp_bom_id):
        self.cur.execute('''SELECT * FROM bom AS a INNER JOIN spp AS b ON (a.id = ? AND b.bom_id = ?)''', (bom_id, spp_bom_id))
        rows = self.cur.fetchall()
        result_rows = []
        for row in rows:
            # id, kode_material (bom), deskripsi (bom), spesifikasi (bom), nomor, satuan, unit, status
            values = [row[0], row[2], row[3], row[4], row[11], row[12], row[13], row[14]]
            temp_tuple = tuple(values)
            result_rows.append(temp_tuple)
        return result_rows
    # Fetch -> PO
    def fetch_view_po(self, bom_id, spp_bom_id):
        self.cur.execute('''SELECT * FROM bom AS a INNER JOIN po AS b ON (a.id = ? AND b.bom_id = ?)''', (bom_id, spp_bom_id))
        rows = self.cur.fetchall()
        result_rows = []
        for row in rows:
            # kode bom, kode, kuantitas, nomor, deskripsi, tanggal, spesifikasi, satuan
            values = [
                row[0], # id
                row[2], # kode_bom
                row[14], # kode
                row[12], # kuantitas
                row[11], # nomor
                row[3], # deskripsi
                row[15], # tanggal
                row[4], # spesifikasi
                row[13] # satuan
            ]
            temp_tuple = tuple(values)
            result_rows.append(temp_tuple)
        return result_rows
    # Fetch -> Overall bom for export feature
    def fetch_all_bom(self, project_id):
        pass
    def select_project_image(self, project_id):
        self.cur.execute("SELECT image FROM projects WHERE id=?", (project_id,))
        rows = self.cur.fetchall()
        return rows

    # INSERT
    # Insert -> projects
    def insert(self, project_name, year, capacity, customer, totals, image):
        self.cur.execute("INSERT INTO projects VALUES (NULL, ?, ?, ?, ?, ?, ?)", (project_name, year, capacity, customer, totals, image,))
        self.conn.commit()
    # Insert bom -> bom (id, rev, kode_material, deskripsi, spesifikasi, kuantitas, satuan, filepath, project_id, spp_id, po_id, keterangan)
    def insert_bom(self, rev, kode_material, deskripsi, spesifikasi, kuantitas, satuan, project_id, keterangan):
        self.cur.execute('''INSERT INTO bom VALUES (NULL, ?, ?, ?, ?, ?, ?, NULL, ?, ?)''',
        (rev, kode_material, deskripsi, spesifikasi, kuantitas, satuan, project_id, keterangan))
        self.conn.commit()
    # Insert spp
    def insert_spp(self, nomor, kuantitas, satuan, status, project_id, bom_id):
        sql = '''
            INSERT INTO spp VALUES (NULL, ?, ?, ?, ?, ?, ?)
        '''
        variables = (nomor, kuantitas, satuan, status, project_id, bom_id)
        self.cur.execute(sql, variables)
        self.conn.commit()
    # Insert po
    def insert_po(self, nomor, kuantitas, satuan, kode, tanggal_kedatangan, project_id, bom_id):
        sql = '''
            INSERT INTO po VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
        '''
        variables = (nomor, kuantitas, satuan, kode, tanggal_kedatangan, project_id, bom_id)
        self.cur.execute(sql, variables)
        self.conn.commit()
    # Insert user
    def insert_user(self, username, password):
        self.cur.execute('''
            INSERT INTO user_admin VALUES (NULL, ?, ?, NULL)
        ''', (username, password))
        self.conn.execute()

    # Remove -> projects
    def remove(self, id):
        self.cur.execute("DELETE FROM projects WHERE id=?", (id,))
        self.conn.commit()

    # UPDATE ROW
    # Update -> projects    
    def update(self, id, project_name, year, capacity, customer, totals):
        self.cur.execute("UPDATE projects SET project_name=?, year=?, capacity=?, customer=?, totals=? WHERE id=?", (project_name, year, capacity, customer, totals, id))
        self.conn.commit()
    def update_project_filename(self, filepath, project_id):
        self.cur.execute('''
                UPDATE projects SET image=? WHERE id=?
            ''', (filepath, project_id))
        self.conn.commit()
    # Update -> BOM
    def update_bom(self, id, rev, kode_material, deskripsi, spesifikasi, kuantitas, satuan, keterangan):
        sql = "UPDATE bom SET rev=?, kode_material=?, deskripsi=?, spesifikasi=?, kuantitas=?, satuan=?, keterangan=? WHERE id=?"
        variables = (rev, kode_material, deskripsi, spesifikasi, kuantitas, satuan, keterangan, id)
        self.cur.execute(sql, variables)
        self.conn.commit()
    def update_bom_filename(self, filepath, project_id):
        self.cur.execute('''
                UPDATE bom SET filepath=? WHERE id=?
            ''', (filepath, project_id))
        self.conn.commit()
    # Update -> SPP
    def update_spp(self, id, nomor, kuantitas, satuan, status):
        sql = "UPDATE spp SET nomor=?, kuantitas=?, satuan=?, status=? WHERE id=?"
        variables = (nomor, kuantitas, satuan, status, id)
        self.cur.execute(sql, variables)
        self.conn.commit()
    # Update -> PO
    def update_po(self, id, nomor, kuantitas, satuan, kode, tanggal_kedatangan):
        sql = "UPDATE po SET nomor=?, kuantitas=?, satuan=?, kode=?, tanggal_kedatangan=? WHERE id=?"
        variables = (nomor, kuantitas, satuan, kode, tanggal_kedatangan, id)
        self.cur.execute(sql, variables)
        self.conn.commit()

    # SEARCH
    # Query projects by year -> projects
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
    # Query projects -> id, project_name -> importing selection
    def query_for_importing(self):
        sql = '''SELECT id, project_name FROM projects'''
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows

    # Destructor -> projects
    def __del__(self):
        self.conn.close()