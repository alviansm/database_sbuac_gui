import tkinter as tk
from tkinter import ttk
from turtle import width
from database.database import Database

db = Database("sbu_projects.db")

def window_edit_bom(master, project_name=""):
    # WINDOW -> konfigurasi window proyek baru
    edit_bom = tk.Toplevel(master)
    edit_bom.title("Edit BOM")
    edit_bom.geometry("720x480")
    edit_bom.resizable(False, False)
    edit_bom.iconbitmap("./favicon.ico")

    K_OPTIONS = [
        "Sudah Lengkap",
        "Sudah Lengkap",
        "Belum Lengkap",
    ]
    QUANTITY_OPTIONS = [
        "unit",
        "unit",
        "pcs",
        "mater",
        "tabung",
        "roll",
        "lembar",
        "batang",
        "kg",
        "pack",
        "sausage"
    ]

    # ===VARIABLES===
    input_rev = tk.StringVar()
    input_kode_material = tk.StringVar()
    input_deskripsi_material = tk.StringVar()
    input_spesifikasi_material = tk.StringVar()
    input_kuantitas = tk.IntVar()
    input_satuan = tk.StringVar()
    input_keterangan = tk.StringVar()
    input_keterangan.set(K_OPTIONS[0])
    input_satuan.set(QUANTITY_OPTIONS[0])

    # ===WIDGETS===
    # JUDUL
    if project_name == "":
            title = tk.Label(edit_bom, text="Proyek baru", pady=4, padx=4, font=("Verdana bold", 12))
            title.grid(row=0, column=0, columnspan=6)        
    else:
            title = tk.Label(edit_bom, text=project_name, pady=4, padx=4, font=("Verdana bold", 12))
            title.grid(row=0, column=0, columnspan=6)
    # GROUP -> INSERT MATERIAL BARU
    group_insert = tk.LabelFrame(edit_bom, text="Tambah Material", font=("Verdana bold", 9))
    group_insert.grid(row=1, column=0, columnspan=6, padx=10)
    # GROUP WIDGETS -> INSERT MATERIAL BARU
    # rev
    label_material_rev = tk.Label(group_insert, text="Rev : ", font=("Arial", 11))
    label_material_rev.grid(row=0, column=0, padx=12, sticky=tk.E, pady=3)
    entry_material_rev = tk.Entry(group_insert, textvariable=input_rev, font=("Arial", 11), width=16)
    entry_material_rev.grid(row=0, column=1, padx=3)
    # kode material
    label_material_rev = tk.Label(group_insert, text="Kode Material : ", font=("Arial", 11))
    label_material_rev.grid(row=1, column=0, padx=12, sticky=tk.E, pady=3)
    entry_material_rev = tk.Entry(group_insert, textvariable=input_kode_material, font=("Arial", 11), width=16)
    entry_material_rev.grid(row=1, column=1, padx=3)
    # keterangan
    label_keterangan = tk.Label(group_insert, text="Stok Material : ")
    label_keterangan.grid(row=2, column=0, padx=12, sticky=tk.E, pady=3)
    entry_keterangan = ttk.OptionMenu(group_insert, input_keterangan, *K_OPTIONS)
    entry_keterangan.grid(row=2, column=1, padx=3, sticky=tk.E)
    # deskripsi
    label_deskripsi = tk.Label(group_insert, text="Deskripsi : ", font=("Arial", 11))
    label_deskripsi.grid(row=0, column=2, padx=12, sticky=tk.E, pady=3)
    entry_deskripsi = tk.Entry(group_insert, textvariable=input_deskripsi_material, font=("Arial", 11), width=16)
    entry_deskripsi.grid(row=0, column=3, padx=3)
    # spesifikasi
    label_spesifikasi = tk.Label(group_insert, text="Spesifikasi : ", font=("Arial", 11))
    label_spesifikasi.grid(row=1, column=2, padx=12, sticky=tk.E, pady=3)
    entry_spesifikasi = tk.Entry(group_insert, textvariable=input_spesifikasi_material, font=("Arial", 11), width=16)
    entry_spesifikasi.grid(row=1, column=3, padx=3)
    # kuantitas
    label_kuantitas = tk.Label(group_insert, text="Kuantitas : ", font=("Arial", 11))
    label_kuantitas.grid(row=0, column=4, padx=12, sticky=tk.E, pady=3)
    entry_kuantitas = tk.Entry(group_insert, textvariable=input_kuantitas, font=("Arial", 11), width=8)
    entry_kuantitas.grid(row=0, column=5, padx=12)
    # satuan
    label_satuan = tk.Label(group_insert, text="Satuan : ")
    label_satuan.grid(row=1, column=4, padx=12, sticky=tk.E, pady=3)
    entry_satuan = ttk.OptionMenu(group_insert, input_satuan, *QUANTITY_OPTIONS)
    entry_satuan.grid(row=1, column=5, padx=3, sticky=tk.E)