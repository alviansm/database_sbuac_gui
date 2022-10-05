import tkinter as tk
from tkinter import ttk
from turtle import width

from database.database import Database
import gui.new_windows.lihat_po as lp
import gui.new_windows.lihat_spp as ls
import gui.commands.commands as commands

db = Database("sbu_projects.db")

def window_lihat_bom(master, project_id=0, project_name=""):
    # WINDOW -> konfigurasi window proyek baru
    lihat_bom = tk.Toplevel(master)
    lihat_bom.title("Review BOM")
    lihat_bom.geometry("720x520")
    lihat_bom.resizable(False, False)
    lihat_bom.iconbitmap("./favicon.ico")

    selected_project = ""

    # ===VARIABLES===
    input_rev = tk.StringVar()
    input_kode_material = tk.StringVar()
    input_deskripsi_material = tk.StringVar()
    input_spesifikasi_material = tk.StringVar()
    input_kuantitas = tk.IntVar()
    input_satuan = tk.StringVar()
    input_stok = tk.StringVar()

    input_cari_kode = tk.StringVar()
    input_cari_deskripsi = tk.StringVar()
    input_cari_spec = tk.StringVar()

    # ===FUNCTIONS===
    def fn_clear_view_bom():
        entry_material_rev.delete(0, tk.END)
        entry_material_code.delete(0, tk.END)
        entry_deskripsi.delete(0, tk.END)
        entry_spesifikasi.delete(0, tk.END)
        entry_kuantitas.delete(0, tk.END)
        entry_satuan.delete("1.0", "end")
        entry_keterangan.delete(0, tk.END)
        
    def select_item(event):
        try:
            index = list_result.curselection()[0]
            selected_project = list_result.get(index)
            
            # rev
            entry_material_rev.delete(0, tk.END)
            entry_material_rev.insert(tk.END, selected_project[1])
            # kodebom
            entry_material_code.delete(0, tk.END)
            entry_material_code.insert(tk.END, selected_project[2])
            # deskripsi
            entry_deskripsi.delete(0, tk.END)
            entry_deskripsi.insert(tk.END, selected_project[3])
            # spesifikasi
            entry_spesifikasi.delete(0, tk.END)
            entry_spesifikasi.insert(tk.END, selected_project[4])
            # jumlah
            entry_kuantitas.delete(0, tk.END)
            entry_kuantitas.insert(tk.END, selected_project[5])
            # keterangan
            if selected_project[7] == 0:
                input_stok = "Stok tidak ada"
            if selected_project[7] == 1:
                input_stok = "Stok ada"
            entry_keterangan.delete(0, tk.END)
            entry_keterangan.insert(tk.END, input_stok)
            # unit
            input_satuan = selected_project[6]
            entry_satuan.delete("1.0", "end")
            entry_satuan.insert(tk.END, input_satuan)
        except IndexError:
            pass

    # ===WIDGETS===
    # JUDUL
    if project_name == "":
            title = tk.Label(lihat_bom, text="Review BOM", pady=4, padx=4, font=("Verdana bold", 12))
            title.grid(row=0, column=0, columnspan=6)        
    else:
            title = tk.Label(lihat_bom, text="BOM : Proyek " + str(project_name), pady=4, padx=4, font=("Verdana bold", 12))
            title.grid(row=0, column=0, columnspan=6)
    # GROUP -> Pencarian
    group_search = tk.LabelFrame(lihat_bom, text="Cari Material", font=("Verdana bold", 9))
    group_search.grid(row=2, column=0, columnspan=6, padx=12, pady=6)
    # kode material
    label_search_material_kode = tk.Label(group_search, text="Kode Material : ", font=("Arial", 11))
    label_search_material_kode.grid(row=0, column=0, padx=12, sticky=tk.E, pady=3)
    entry_search_material_kode = tk.Entry(group_search, textvariable=input_cari_kode, font=("Arial", 11), width=10)
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
    group_button_search = tk.Frame(lihat_bom)
    group_button_search.grid(row=3, column=0, columnspan=6, pady=3, padx=12, sticky=tk.E)
    # clear
    button_search = ttk.Button(group_button_search, text="Clear")
    button_search.grid(row=0, column=0, sticky=tk.W, padx=12)
    # cari
    button_search = ttk.Button(group_button_search, text="Cari")
    button_search.grid(row=0, column=1)
    # GROUP -> REVIEW MATERIAL TERPILIH
    group_insert = tk.LabelFrame(lihat_bom, text="Review Material", font=("Verdana bold", 9))
    group_insert.grid(row=4, column=0, columnspan=6, padx=12)
    # GROUP WIDGETS -> REVIEW MATERIAL
    # rev
    label_material_rev = tk.Label(group_insert, text="Rev : ", font=("Arial", 11))
    label_material_rev.grid(row=0, column=0, padx=12, sticky=tk.E, pady=3)
    entry_material_rev = tk.Entry(group_insert, textvariable=input_rev, font=("Arial", 11), width=16)
    entry_material_rev.grid(row=0, column=1, padx=3)
    # kode material
    label_material_code = tk.Label(group_insert, text="Kode Material : ", font=("Arial", 11))
    label_material_code.grid(row=1, column=0, padx=12, sticky=tk.E, pady=3)
    entry_material_code = tk.Entry(group_insert, textvariable=input_kode_material, font=("Arial", 11), width=16)
    entry_material_code.grid(row=1, column=1, padx=3)
    # keterangan
    label_keterangan = tk.Label(group_insert, text="Stok Material : ")
    label_keterangan.grid(row=2, column=0, padx=12, sticky=tk.E, pady=3)
    entry_keterangan = tk.Entry(group_insert, textvariable=input_stok, font=("Arial", 11), width=16)
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
    entry_kuantitas = tk.Entry(group_insert, textvariable=input_kuantitas, font=("Arial", 11), width=5)
    entry_kuantitas.grid(row=0, column=5, padx=12)
    # satuan
    entry_satuan = tk.Text(group_insert, height=1, width=4)
    entry_satuan.grid(row=1, column=4, columnspan=2, padx=3)
    # GROUP BUTTON REVIEW MATERIAL
    group_button_review = tk.Frame(lihat_bom)
    group_button_review.grid(row=5, column=0, columnspan=6, pady=3, padx=12, sticky=tk.E)
    # clear
    button_clear = ttk.Button(group_button_review, text="Clear", command=fn_clear_view_bom)
    button_clear.grid(row=0, column=0, padx=3)
    # lihat spp
    button_lihat_spp = ttk.Button(group_button_review, text="Lihat SPP", command=lambda: ls.window_lihat_spp(master, project_id, project_id))
    button_lihat_spp.grid(row=0, column=1, padx=3)
    # lihat po
    button_lihat_po = ttk.Button(group_button_review, text="Lihat PO", command=lambda: lp.window_lihat_po(master))
    button_lihat_po.grid(row=0, column=2, padx=3)
    # data sheet
    button_datasheet = ttk.Button(group_button_review, text="Data Sheet")
    button_datasheet.grid(row=0, column=3, padx=3)
    # LISTBOX
    list_result = tk.Listbox(lihat_bom, height=12, width=82, border=1)
    list_result.grid(row=6, column=0, columnspan=6, pady=5)
    scrollbar = tk.Scrollbar(lihat_bom)
    scrollbar.grid(row=6, column=0, columnspan=6, padx=13, sticky=tk.E)
    list_result.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=list_result.yview)
    
    commands.populate_view_bom(list_result, project_id)
    list_result.bind('<<ListboxSelect>>', select_item)
