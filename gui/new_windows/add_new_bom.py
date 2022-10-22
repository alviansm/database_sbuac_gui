import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from database.database import Database

db = Database("sbu_projects.db")

global_latest_bom_no = 0
filename_path = ""
def fn_window_add_new_material(master, project_id=0):
    # ===Window Configuration===
    add_bom = tk.Toplevel(master)
    add_bom.title("Tambah Material Baru")
    add_bom.geometry("720x580")
    add_bom.resizable(False, False)
    add_bom.iconbitmap("./favicon.ico")

    # ===Variables===
    global global_latest_bom_no
    global_latest_bom_no = 0
    # BOM
    input_bom_id = tk.StringVar()
    input_bom_rev = tk.StringVar()
    input_bom_kode_material = tk.StringVar()
    input_bom_keterangan_stok = tk.StringVar()
    input_bom_deskripsi_material = tk.StringVar()
    input_bom_spesifikasi_material = tk.StringVar()
    input_bom_kuantitas = tk.StringVar()
    # PR/SPP
    input_spp_nomor = tk.StringVar()
    input_spp_kuantitas = tk.StringVar()
    input_spp_satuan = tk.StringVar()
    input_spp_status = tk.StringVar()
    # PO
    input_po_nomor = tk.StringVar()
    input_po_kuantitas = tk.StringVar()
    input_po_satuan = tk.StringVar()
    input_po_kode = tk.StringVar()
    input_po_tanggal = tk.StringVar()
    # BOM
    input_bom_stok_barang = tk.StringVar()
    
    # ===Functions===
    def fn_choose_image():
        filepath = filedialog.askopenfilename(initialdir="/", title="Pilih file yang dilink untuk proyek", filetypes=[("All files", ".*")])
        entry_datasheet_path.delete("1.0", "end")
        entry_datasheet_path.insert(tk.END, str(filepath).strip())
        global filename_path
        filename_path = filepath
    
    def clear_treeview_bom():
        for record in treeview_result.get_children():
            treeview_result.delete(record)

    def populate_treeview_bom(x):
        clear_treeview_bom()
        for row in db.fetch_view_bom(x):
            treeview_result.insert(parent="", index=row[0], iid=row[0], values=(row[0], row[1], row[2], row[7], row[3], row[4], row[5], row[6]))

    def clear_entries():
        entry_bom_material_rev.delete(0, tk.END)
        entry_bom_material_code.delete(0, tk.END)
        entry_bom_keterangan.delete(0, tk.END)
        entry_bom_deskripsi.delete(0, tk.END)
        entry_bom_spesifikasi.delete(0, tk.END)
        entry_bom_kuantitas.delete(0, tk.END)
        entry_bom_satuan.delete("1.0", "end")
        entry_datasheet_path.delete("1.0", "end")
        entry_spp_nomor.delete(0, tk.END)
        entry_spp_kuantitas.delete(0, tk.END)
        entry_spp_satuan.delete("1.0", "end")
        entry_spp_status.delete(0, tk.END)
        entry_po_nomor.delete(0, tk.END)
        entry_po_kuantitas.delete(0, tk.END)
        entry_po_satuan.delete("1.0", "end")
        entry_po_kode.delete(0, tk.END)
        entry_po_tanggal.delete(0, tk.END)
        entry_bom_stok.delete(0, tk.END)

    def get_latest_id(x):
        result = []
        for row in db.fetch_view_bom(x):
            result.append(row)
        latest_row = result[len(result)-1]
        latest_id = latest_row[0]
        global global_latest_bom_no
        global_latest_bom_no = latest_id

    get_latest_id(project_id)
    
    def update_bom(selection_id, rev, kode_material, deskripsi, spesifikasi, kuantitas, satuan, keterangan, datasheet_path):
        # clear treeview data
        clear_treeview_bom()        
        # update in database
        db.update_bom(selection_id, rev, kode_material, deskripsi, spesifikasi, kuantitas, satuan, keterangan, entry_datasheet_path.get("1.0", "end"))
        # update project filename
        if len(datasheet_path) > 0:
            db.update_bom_filename(str(datasheet_path).strip(), kode_material)
        # clear entries
        clear_entries()        
        # repopulate bom treeview data
        populate_treeview_bom(project_id)

    def fn_add_new_bom(project_id, latest_bom_id, bom_rev, bom_kode_material, bom_deskripsi, bom_spesifikasi, bom_kuantitas, bom_satuan, datasheet, spp_nomor, spp_kuantitas, spp_satuan, spp_status, po_nomor, po_kuantitas, po_satuan, po_kode, po_tanggal, bom_stok):
        try:
            if len(bom_rev) > 0 and len(bom_kode_material) > 0 and len(bom_deskripsi) > 0 and len(bom_spesifikasi) > 0 and len(bom_kuantitas) > 0 and len(bom_satuan) > 0:
                clear_treeview_bom()                
                # Insert "-" if entry is empty
                datasheet = datasheet
                if len(datasheet) < 1 and len(spp_nomor) < 1 and len(spp_kuantitas) < 1 and len(spp_satuan) < 1 and len(spp_status) < 1 and len(po_nomor) < 1 and len(po_kuantitas) < 1 and len(po_satuan) < 1 and len(po_kode) < 1 and len(po_tanggal) and len(bom_stok) < 1:
                    datasheet = "-"
                    spp_nomor = "-"
                    spp_kuantitas = "-"
                    spp_satuan = "-"
                    spp_status = "-"
                    po_nomor = "-"
                    po_kuantitas = "-"
                    po_satuan = "-"
                    po_kode = "-"
                    po_tanggal = "-"
                    bom_stok = "-"
                # Global variable declaration        
                current_project_id = project_id
                latest_bom_id = latest_bom_id+1
                db.insert_bom(bom_rev, bom_kode_material, bom_deskripsi, bom_spesifikasi, bom_kuantitas, bom_satuan, current_project_id, bom_stok, int(latest_bom_id))
                db.insert_spp(spp_nomor, spp_kuantitas, spp_satuan, spp_status, current_project_id, int(latest_bom_id))
                db.insert_po(po_nomor, po_kuantitas, po_satuan, po_kode, po_tanggal, current_project_id, int(latest_bom_id))
                update_bom(project_id, bom_rev, bom_kode_material, bom_deskripsi, bom_spesifikasi, bom_kuantitas, bom_satuan, bom_stok, datasheet)
                clear_entries()
                populate_treeview_bom(project_id)
                get_latest_id(project_id)                
            else:
                messagebox.showerror("Error", "Silahkan isi entri BOM")
        except:
            messagebox.showerror("Error", "Tidak bisa menambahkan material baru")

    # ===Widgets===
    # window title
    title = tk.Label(add_bom, text="Tambah Material Baru", pady=4, padx=4, font=("Verdana bold", 12))
    title.grid(row=0, column=0, columnspan=6)

    # group -> bom
    group_bom = tk.LabelFrame(add_bom, text="Bill of Material", font=("Verdana bold", 9))
    group_bom.grid(row=1, column=0, columnspan=6, padx=12, pady=6)
    # bom widget entries
    # rev
    label_bom_material_rev = tk.Label(group_bom, text="Rev : ", font=("Arial", 11))
    label_bom_material_rev.grid(row=0, column=0, padx=12, sticky=tk.E, pady=3)
    entry_bom_material_rev = tk.Entry(group_bom, textvariable=input_bom_rev, font=("Arial", 11), width=16)
    entry_bom_material_rev.grid(row=0, column=1, padx=3)
    # kode material
    label_bom_material_code = tk.Label(group_bom, text="Kode Material : ", font=("Arial", 11))
    label_bom_material_code.grid(row=1, column=0, padx=12, sticky=tk.E, pady=3)
    entry_bom_material_code = tk.Entry(group_bom, textvariable=input_bom_kode_material, font=("Arial", 11), width=16)
    entry_bom_material_code.grid(row=1, column=1, padx=3)
    # keterangan
    label_bom_keterangan = tk.Label(group_bom, text="Stok Material : ")
    label_bom_keterangan.grid(row=2, column=0, padx=12, sticky=tk.E, pady=3)
    entry_bom_keterangan = tk.Entry(group_bom, textvariable=input_bom_keterangan_stok, font=("Arial", 11), width=16)
    entry_bom_keterangan.grid(row=2, column=1, padx=3, sticky=tk.E)
    # deskripsi
    label_bom_deskripsi = tk.Label(group_bom, text="Deskripsi : ", font=("Arial", 11))
    label_bom_deskripsi.grid(row=0, column=2, padx=12, sticky=tk.E, pady=3)
    entry_bom_deskripsi = tk.Entry(group_bom, textvariable=input_bom_deskripsi_material, font=("Arial", 11), width=16)
    entry_bom_deskripsi.grid(row=0, column=3, padx=3)
    # spesifikasi
    label_bom_spesifikasi = tk.Label(group_bom, text="Spesifikasi : ", font=("Arial", 11))
    label_bom_spesifikasi.grid(row=1, column=2, padx=12, sticky=tk.E, pady=3)
    entry_bom_spesifikasi = tk.Entry(group_bom, textvariable=input_bom_spesifikasi_material, font=("Arial", 11), width=16)
    entry_bom_spesifikasi.grid(row=1, column=3, padx=3)
    # kuantitas
    label_bom_kuantitas = tk.Label(group_bom, text="Kuantitas : ", font=("Arial", 11))
    label_bom_kuantitas.grid(row=0, column=4, padx=12, sticky=tk.E, pady=3)
    entry_bom_kuantitas = tk.Entry(group_bom, textvariable=input_bom_kuantitas, font=("Arial", 11), width=5)
    entry_bom_kuantitas.grid(row=0, column=5, padx=12)
    # satuan
    entry_bom_satuan = tk.Text(group_bom, height=1, width=4)
    entry_bom_satuan.grid(row=1, column=4, columnspan=2, padx=3)
    # pilih gambar
    button_select_datasheet = ttk.Button(group_bom, text="Pilih Datasheet", width=14, command=fn_choose_image)
    button_select_datasheet.grid(row=2, column=2, columnspan=2, padx=3, sticky=tk.E)
    # datasheet path
    entry_datasheet_path = tk.Text(group_bom, height=1, width=17)
    entry_datasheet_path.grid(row=2, column=4, columnspan=2, padx=3, sticky=tk.W)

    # group -> pr/spp
    group_spp = tk.LabelFrame(add_bom, text="PR/SPP", font=("Verdana bold", 9))
    group_spp.grid(row=2, column=0, columnspan=6, padx=12, pady=6)
    # spp widget entries
    # nomor
    label_spp_nomor = tk.Label(group_spp, text="Nomor : ", font=("Arial", 11))
    label_spp_nomor.grid(row=0, column=0, padx=12, sticky=tk.E, pady=3)
    entry_spp_nomor = tk.Entry(group_spp, textvariable=input_spp_nomor, font=("Arial", 11), width=16)
    entry_spp_nomor.grid(row=0, column=1, padx=3)
    # kuantitas
    label_spp_kuantitas = tk.Label(group_spp, text="Kuantitas : ", font=("Arial", 11))
    label_spp_kuantitas.grid(row=0, column=4, padx=12, sticky=tk.E, pady=3)
    entry_spp_kuantitas = tk.Entry(group_spp, textvariable=input_spp_kuantitas, font=("Arial", 11), width=14)
    entry_spp_kuantitas.grid(row=0, column=5, padx=12)
    # satuan
    entry_spp_satuan = tk.Text(group_spp, height=1, width=4)
    entry_spp_satuan.grid(row=1, column=4, columnspan=2, padx=3, pady=3)
    # status
    label_spp_status = tk.Label(group_spp, text="Status : ", font=("Arial", 11))
    label_spp_status.grid(row=0, column=2, padx=12, sticky=tk.E, pady=3)
    entry_spp_status = tk.Entry(group_spp, textvariable=input_spp_status, font=("Arial", 11), width=16)
    entry_spp_status.grid(row=0, column=3, padx=3)

    # group -> po
    group_po = tk.LabelFrame(add_bom, text="PO", font=("Verdana bold", 9))
    group_po.grid(row=3, column=0, columnspan=6, padx=12, pady=6)
    # po widget entries
    # nomor
    label_po_nomor = tk.Label(group_po, text="Kode : ", font=("Arial", 11))
    label_po_nomor.grid(row=0, column=0, padx=12, sticky=tk.E, pady=3)
    entry_po_nomor = tk.Entry(group_po, textvariable=input_po_nomor, font=("Arial", 11), width=12)
    entry_po_nomor.grid(row=0, column=1, padx=3)    
    # kuantitas
    label_po_kuantitas = tk.Label(group_po, text="Kuantitas : ", font=("Arial", 11))
    label_po_kuantitas.grid(row=0, column=4, padx=12, sticky=tk.E, pady=3)
    entry_po_kuantitas = tk.Entry(group_po, textvariable=input_po_kuantitas, font=("Arial", 11), width=12)
    entry_po_kuantitas.grid(row=0, column=5, padx=12)
    # satuan
    entry_po_satuan = tk.Text(group_po, height=1, width=4)
    entry_po_satuan.grid(row=1, column=4, columnspan=2, padx=3)
    # kode
    label_po_kode = tk.Label(group_po, text="Nomor : ", font=("Arial", 11))
    label_po_kode.grid(row=0, column=2, padx=12, sticky=tk.E, pady=3)
    entry_po_kode = tk.Entry(group_po, textvariable=input_po_kode, font=("Arial", 11), width=16)
    entry_po_kode.grid(row=0, column=3, padx=3, sticky=tk.W)
    # tanggal
    label_po_tanggal = tk.Label(group_po, text="Tgl : ", font=("Arial", 11))
    label_po_tanggal.grid(row=1, column=0, padx=12, sticky=tk.E, pady=3)
    entry_po_tanggal = tk.Entry(group_po, textvariable=input_po_tanggal, font=("Arial", 11), width=16)
    entry_po_tanggal.grid(row=1, column=1, padx=3)
    # stok
    label_bom_stok = tk.Label(group_po, text="Stok Barang : ", font=("Arial", 11))
    label_bom_stok.grid(row=1, column=2, padx=12, sticky=tk.E, pady=3)
    entry_bom_stok = tk.Entry(group_po, textvariable=input_bom_stok_barang, font=("Arial", 11), width=12)
    entry_bom_stok.grid(row=1, column=3, padx=3, sticky=tk.W)

    # GROUP BUTTON REVIEW MATERIAL
    group_button_review = tk.Frame(add_bom)
    group_button_review.grid(row=5, column=0, columnspan=6, pady=3, padx=12, sticky=tk.E)
    # add
    button_add = ttk.Button(group_button_review, text="Tambah Material", command=lambda: fn_add_new_bom(project_id, global_latest_bom_no, entry_bom_material_rev.get(), entry_bom_material_code.get(), entry_bom_deskripsi.get(), entry_bom_spesifikasi.get(), entry_bom_kuantitas.get(), entry_bom_satuan.get("1.0", "end"), entry_datasheet_path.get("1.0", "end"), entry_spp_nomor.get(), entry_spp_kuantitas.get(), entry_spp_satuan.get("1.0", "end"), entry_spp_status.get(), entry_po_nomor.get(), entry_po_kuantitas.get(), entry_po_satuan.get("1.0", "end"), entry_po_kode.get(), entry_po_tanggal.get(), entry_bom_stok.get()))
    button_add.grid(row=0, column=0, padx=3, sticky=tk.E)

    # treeview
    treeview_result = ttk.Treeview(add_bom, height=8)
    
    # Column declaration
    treeview_result['columns'] = ("ID", "Rev", "Kode Material", "Stok Material", "Deskripsi", "Spesifikasi", "Kuantitas", "Unit")
    treeview_result.column("#0", anchor=tk.CENTER, width=0)
    treeview_result.column("ID", anchor=tk.CENTER, width=45)        
    treeview_result.column("Rev", anchor=tk.CENTER, width=45)
    treeview_result.column("Kode Material", anchor=tk.CENTER, width=90)
    treeview_result.column("Stok Material", anchor=tk.CENTER, width=110)
    treeview_result.column("Deskripsi", anchor=tk.CENTER, width=140)
    treeview_result.column("Spesifikasi", anchor=tk.CENTER, width=140)
    treeview_result.column("Kuantitas", anchor=tk.CENTER, width=60)
    treeview_result.column("Unit", anchor=tk.CENTER, width=60)
    # Heading declaration
    treeview_result.heading("#0", text="", anchor=tk.CENTER)
    treeview_result.heading("ID", text="ID", anchor=tk.CENTER)
    treeview_result.heading("Rev", text="Rev", anchor=tk.CENTER)
    treeview_result.heading("Kode Material", text="Kode Material", anchor=tk.CENTER)
    treeview_result.heading("Stok Material", text="Stok Material", anchor=tk.CENTER)
    treeview_result.heading("Deskripsi", text="Deskripsi", anchor=tk.CENTER)
    treeview_result.heading("Spesifikasi", text="Spesifikasi", anchor=tk.CENTER)
    treeview_result.heading("Kuantitas", text="Kuantitas", anchor=tk.CENTER)
    treeview_result.heading("Unit", text="Unit", anchor=tk.CENTER)
    
    treeview_result.grid(row=6, column=0, padx=11, pady=6)

    # Populate
    populate_treeview_bom(project_id)