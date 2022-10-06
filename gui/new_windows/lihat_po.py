import tkinter as tk
from tkinter import ttk
from database.database import Database
import gui.commands.commands as commands

db = Database("sbu_projects.db")

def window_lihat_po(master, bom_id=0, spp_bom_id=0, project_name=""):
    # WINDOW -> konfigurasi window proyek baru
    lihat_po = tk.Toplevel(master)
    lihat_po.title("Review PO")
    lihat_po.geometry("720x520")
    lihat_po.resizable(False, False)
    lihat_po.iconbitmap("./favicon.ico")

    def fn_clear_selection():
        entry_bom_code.delete(0, tk.END)
        entry_material_kode.delete(0, tk.END)
        entry_material_kuantitas.delete(0, tk.END)
        entry_material_number.delete(0, tk.END)
        entry_material_deskripsi.delete(0, tk.END)
        entry_material_tanggal.delete(0, tk.END)
        entry_material_spesifikasi.delete(0, tk.END)
        entry_satuan.delete("1.0", "end")

    def select_item(event):
        try:
            index = list_result.curselection()[0]
            selected_project = list_result.get(index)
            
            entry_bom_code.delete(0, tk.END)
            entry_bom_code.insert(tk.END, selected_project[1])
            entry_material_kode.delete(0, tk.END)
            entry_material_kode.insert(tk.END, selected_project[2])
            entry_material_kuantitas.delete(0, tk.END)
            entry_material_kuantitas.insert(tk.END, selected_project[3])
            entry_material_number.delete(0, tk.END)
            entry_material_number.insert(tk.END, selected_project[4])
            entry_material_deskripsi.delete(0, tk.END)
            entry_material_deskripsi.insert(tk.END, selected_project[5])
            entry_material_tanggal.delete(0, tk.END)
            entry_material_tanggal.insert(tk.END, selected_project[6])
            entry_material_spesifikasi.delete(0, tk.END)
            entry_material_spesifikasi.insert(tk.END, selected_project[7])
            entry_satuan.delete("1.0", "end")
            entry_satuan.insert(tk.END, selected_project[8])            
        except IndexError:
            pass 

    # ===VARIABLES===
    input_bom_code = tk.StringVar()
    input_deskripsi = tk.StringVar()
    input_spesifikasi = tk.StringVar()
    input_material_nomor = tk.StringVar()
    input_material_tanggal = tk.StringVar()
    input_material_kuantitas = tk.IntVar()
    input_material_kode = tk.StringVar()

    input_cari_kode = tk.StringVar()
    input_cari_deskripsi = tk.StringVar()
    input_cari_spec = tk.StringVar()

    # ===WIDGETS===
    # JUDUL
    if project_name == "":
            title = tk.Label(lihat_po, text="Review PO", pady=4, padx=4, font=("Verdana bold", 12))
            title.grid(row=0, column=0, columnspan=6)        
    else:
            title = tk.Label(lihat_po, text=project_name, pady=4, padx=4, font=("Verdana bold", 12))
            title.grid(row=0, column=0, columnspan=6)
    # GROUP -> Pencarian
    group_search = tk.LabelFrame(lihat_po, text="Cari Material", font=("Verdana bold", 9))
    group_search.grid(row=2, column=0, columnspan=6, padx=12, pady=6)
    # kode material
    label_search_material_kode = tk.Label(group_search, text="Kode BOM: ", font=("Arial", 11))
    label_search_material_kode.grid(row=0, column=0, padx=12, sticky=tk.E, pady=3)
    entry_search_material_kode = tk.Entry(group_search, textvariable=input_cari_kode, font=("Arial", 11), width=12)
    entry_search_material_kode.grid(row=0, column=1, padx=3)
    # deskripsi
    label_search_material_deskripsi = tk.Label(group_search, text="Deskripsi : ", font=("Arial", 11))
    label_search_material_deskripsi.grid(row=0, column=2, padx=6, sticky=tk.E, pady=3)
    entry_search_material_deskripsi = tk.Entry(group_search, textvariable=input_cari_deskripsi, font=("Arial", 11), width=15)
    entry_search_material_deskripsi.grid(row=0, column=3, padx=3)
    # spesifikasi
    label_search_material_spec = tk.Label(group_search, text="Spesifikasi : ", font=("Arial", 11))
    label_search_material_spec.grid(row=0, column=4, padx=6, sticky=tk.E, pady=3)
    entry_search_material_spec = tk.Entry(group_search, textvariable=input_cari_spec, font=("Arial", 11), width=15)
    entry_search_material_spec.grid(row=0, column=5, padx=12, sticky=tk.W, pady=6)
    # GROUP -> Tombol Pencarian
    group_button_search = tk.Frame(lihat_po)
    group_button_search.grid(row=3, column=0, columnspan=6, pady=3, padx=12, sticky=tk.E)
    # clear
    button_search = ttk.Button(group_button_search, text="Clear")
    button_search.grid(row=0, column=0, sticky=tk.W, padx=12)
    # cari
    button_search = ttk.Button(group_button_search, text="Cari")
    button_search.grid(row=0, column=1)
    # GROUP -> REVIEW MATERIAL TERPILIH
    group_insert = tk.LabelFrame(lihat_po, text="Review Material", font=("Verdana bold", 9))
    group_insert.grid(row=4, column=0, columnspan=6, padx=12)
    # GROUP WIDGETS -> REVIEW MATERIAL
    # kode bom (bom)
    label_bom_code = tk.Label(group_insert, text="Kode BOM : ", font=("Arial", 11))
    label_bom_code.grid(row=0, column=0, padx=12, sticky=tk.E, pady=3)
    entry_bom_code = tk.Entry(group_insert, textvariable=input_bom_code, font=("Arial", 11), width=16)
    entry_bom_code.grid(row=0, column=1, padx=3)
    # kode
    label_material_kode = tk.Label(group_insert, text="Kode : ", font=("Arial", 11))
    label_material_kode.grid(row=0, column=2, padx=12, sticky=tk.E, pady=3)
    entry_material_kode = tk.Entry(group_insert, textvariable=input_material_kode, font=("Arial", 11), width=12)
    entry_material_kode.grid(row=0, column=3, padx=3)    
    # kuantitas
    label_material_kuantitas = tk.Label(group_insert, text="Kuantitas : ", font=("Arial", 11))
    label_material_kuantitas.grid(row=0, column=4, padx=12, sticky=tk.E, pady=3)
    entry_material_kuantitas = tk.Entry(group_insert, textvariable=input_material_kuantitas, font=("Arial", 11), width=12)
    entry_material_kuantitas.grid(row=0, column=5, padx=12)
    # satuan
    entry_satuan = tk.Text(group_insert, height=1, width=4)
    entry_satuan.grid(row=1, column=4, columnspan=2, padx=3)
    # nomor material
    label_material_number = tk.Label(group_insert, text="Nomor : ", font=("Arial", 11))
    label_material_number.grid(row=1, column=0, padx=12, sticky=tk.E, pady=3)
    entry_material_number = tk.Entry(group_insert, textvariable=input_material_nomor, font=("Arial", 11), width=16)
    entry_material_number.grid(row=1, column=1, padx=3)
    # deskripsi (bom)
    label_material_deskripsi = tk.Label(group_insert, text="Deskripsi : ", font=("Arial", 11))
    label_material_deskripsi.grid(row=1, column=2, padx=12, sticky=tk.E, pady=3)
    entry_material_deskripsi = tk.Entry(group_insert, textvariable=input_deskripsi, font=("Arial", 11), width=12)
    entry_material_deskripsi.grid(row=1, column=3, padx=3)  
    # tanggal
    label_material_tanggal = tk.Label(group_insert, text="Tgl : ", font=("Arial", 11))
    label_material_tanggal.grid(row=2, column=0, padx=12, sticky=tk.E, pady=3)
    entry_material_tanggal = tk.Entry(group_insert, textvariable=input_material_tanggal, font=("Arial", 11), width=16)
    entry_material_tanggal.grid(row=2, column=1, padx=3)
    # spesifikasi
    label_material_spesifikasi = tk.Label(group_insert, text="Spesifikasi : ", font=("Arial", 11))
    label_material_spesifikasi.grid(row=2, column=2, padx=12, sticky=tk.E, pady=3)
    entry_material_spesifikasi = tk.Entry(group_insert, textvariable=input_spesifikasi, font=("Arial", 11), width=12)
    entry_material_spesifikasi.grid(row=2, column=3, padx=3)  
    # GROUP BUTTON REVIEW MATERIAL
    group_button_review = tk.Frame(lihat_po)
    group_button_review.grid(row=5, column=0, columnspan=6, pady=3, padx=12, sticky=tk.E)
    # clear
    button_clear = ttk.Button(group_button_review, text="Clear", command=fn_clear_selection)
    button_clear.grid(row=0, column=0, padx=3)
    # refresh
    button_refresh = ttk.Button(group_button_review, text="Refresh")
    button_refresh.grid(row=0, column=1, padx=3)
    # data sheet
    button_datasheet = ttk.Button(group_button_review, text="Data Sheet")
    button_datasheet.grid(row=0, column=2, padx=3)
    # LISTBOX
    list_result = tk.Listbox(lihat_po, height=12, width=82, border=1)
    list_result.grid(row=6, column=0, columnspan=6, pady=5)
    scrollbar = tk.Scrollbar(lihat_po)
    scrollbar.grid(row=6, column=0, columnspan=6, padx=13, sticky=tk.E)
    list_result.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=list_result.yview)

    # Populate to Listbox
    commands.populate_view_po(list_result, bom_id, spp_bom_id)
    # Bind selection
    list_result.bind('<<ListboxSelect>>', select_item)