import tkinter as tk
from tkinter import ttk
from database.database import Database
import gui.commands.commands as commands

db = Database("sbu_projects.db")

global_selected_spp_id = 0
def window_edit_spp(master, bom_id=0, spp_bom_id=0, project_id=0):
    # WINDOW -> konfigurasi window proyek baru
    lihat_po = tk.Toplevel(master)
    lihat_po.title("Edit SPP")
    lihat_po.geometry("720x520")
    lihat_po.resizable(False, False)
    lihat_po.iconbitmap("./favicon.ico")

    # ===VARIABLES===
    project_name = ""
    global global_selected_spp_id
    global_selected_spp_id = 0

    input_material_nomor = tk.StringVar()
    input_material_kuantitas = tk.StringVar()
    input_bom_code = tk.StringVar()
    input_material_deskripsi = tk.StringVar()
    input_material_spesifikasi = tk.StringVar()
    input_satuan = tk.StringVar()
    input_keterangan = tk.StringVar()
    input_status = tk.StringVar()

    input_cari_kode = tk.StringVar()
    input_cari_deskripsi = tk.StringVar()
    input_cari_spec = tk.StringVar()

    # ===FUNCTIONS===
    def fn_clear_selection():
        entry_material_nomor.delete(0, tk.END)
        entry_material_code.delete(0, tk.END)
        entry_material_deskripsi.delete(0, tk.END)
        entry_material_spesifikasi.delete(0, tk.END)
        entry_kuantitas.delete(0, tk.END)
        entry_satuan.delete("1.0", "end")
        entry_material_status.delete(0, tk.END)

    def fn_clear_search():
        entry_search_material_spec.delete(0, tk.END)
        entry_search_material_kode.delete(0, tk.END)
        entry_search_material_deskripsi.delete(0, tk.END)

    def clear_treeview_spp():
        for record in treeview_result.get_children():
            treeview_result.delete(record)

    def populate_treeview_spp(x):
        clear_treeview_spp()
        i = 0
        for row in db.fetch_view_spp(x):
            treeview_result.insert(parent="", index=i, iid=i, values=(row[0], row[4], row[1], row[2], row[3], row[5], row[6], row[7]))
            i = i + 1

    def fn_search_treeview(project_id, kode_bom, deskripsi, spesifikasi):
        clear_treeview_spp()
        count = 0
        for row in db.search_material_by(kode_bom, deskripsi, spesifikasi, project_id):
            treeview_result.insert(parent="", index=count, iid=count, values=(row[0], row[4], row[1], row[2], row[3], row[5], row[6], row[7]))
            count += 1

    def select_item(event):
        try:
            selected = treeview_result.selection()[0]
            values = treeview_result.item(selected, 'values')
            
            global global_selected_spp_id
            global_selected_spp_id = values[0]
            # nomor
            entry_material_nomor.delete(0, tk.END)
            entry_material_nomor.insert(tk.END, values[1])
            # kode bom -> bom
            entry_material_code.delete(0, tk.END)
            entry_material_code.insert(tk.END, values[2])
            # deskripsi -> bom
            entry_material_deskripsi.delete(0, tk.END)
            entry_material_deskripsi.insert(tk.END, values[3])
            # spesifikasi
            entry_material_spesifikasi.delete(0, tk.END)
            entry_material_spesifikasi.insert(tk.END, values[4])
            # kuantitas
            entry_kuantitas.delete(0, tk.END)
            entry_kuantitas.insert(tk.END, values[5])
            # unit
            input_satuan = values[6]
            entry_satuan.delete("1.0", "end")
            entry_satuan.insert(tk.END, input_satuan)
            # status
            input_status = values[7]
            entry_material_status.delete(0, tk.END)
            entry_material_status.insert(tk.END, values[7])
            input_material_nomor = values[1]
            input_bom_code = values[2]
            input_material_deskripsi = values[3]
            input_material_spesifikasi = values[4]
            input_material_kuantitas = values[5]
            input_keterangan = values[7]
        except IndexError:
            pass           

    def fn_update_selection(selected_id, nomor, kuantitas, satuan, status):
        clear_treeview_spp()
        fn_clear_selection()
        db.update_spp(selected_id, nomor, kuantitas, satuan, status)
        populate_treeview_spp(project_id)

    def fn_refresh(project_id):
        clear_treeview_spp()
        populate_treeview_spp(project_id)

    # ===WIDGETS===
    # JUDUL
    if project_name == "":
            title = tk.Label(lihat_po, text="Edit SPP", pady=4, padx=4, font=("Verdana bold", 12))
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
    button_search = ttk.Button(group_button_search, text="Clear", command=fn_clear_search)
    button_search.grid(row=0, column=0, sticky=tk.W, padx=12)
    # cari
    button_search = ttk.Button(group_button_search, text="Cari", command=lambda: fn_search_treeview(project_id, entry_search_material_kode.get(), entry_search_material_deskripsi.get(), entry_search_material_spec.get()))
    button_search.grid(row=0, column=1)
    # GROUP -> REVIEW MATERIAL TERPILIH
    group_insert = tk.LabelFrame(lihat_po, text="Review Material", font=("Verdana bold", 9))
    group_insert.grid(row=4, column=0, columnspan=6, padx=12)
    # GROUP WIDGETS -> REVIEW MATERIAL
    # nomor
    label_material_nomor = tk.Label(group_insert, text="Nomor : ", font=("Arial", 11))
    label_material_nomor.grid(row=0, column=0, padx=12, sticky=tk.E, pady=3)
    entry_material_nomor = tk.Entry(group_insert, textvariable=input_material_nomor, font=("Arial", 11), width=16)
    entry_material_nomor.grid(row=0, column=1, padx=3)
    # kuantitas
    label_kuantitas = tk.Label(group_insert, text="Kuantitas : ", font=("Arial", 11))
    label_kuantitas.grid(row=0, column=4, padx=12, sticky=tk.E, pady=3)
    entry_kuantitas = tk.Entry(group_insert, textvariable=input_material_kuantitas, font=("Arial", 11), width=12)
    entry_kuantitas.grid(row=0, column=5, padx=12)
    # satuan
    entry_satuan = tk.Text(group_insert, height=1, width=4)
    entry_satuan.grid(row=1, column=4, columnspan=2, padx=3)
    # kode material
    label_material_code = tk.Label(group_insert, text="Kode BOM : ", font=("Arial", 11))
    label_material_code.grid(row=1, column=0, padx=12, sticky=tk.E, pady=3)
    entry_material_code = tk.Entry(group_insert, textvariable=input_bom_code, font=("Arial", 11), width=16)
    entry_material_code.grid(row=1, column=1, padx=3)
    # deskripsi  
    label_material_deskripsi = tk.Label(group_insert, text="Deskripsi : ", font=("Arial", 11))
    label_material_deskripsi.grid(row=0, column=2, padx=12, sticky=tk.E, pady=3)
    entry_material_deskripsi = tk.Entry(group_insert, textvariable=input_material_deskripsi, font=("Arial", 11), width=12)
    entry_material_deskripsi.grid(row=0, column=3, padx=3)  
    # spesifikasi
    label_material_spesifikasi = tk.Label(group_insert, text="Spesifikasi : ", font=("Arial", 11))
    label_material_spesifikasi.grid(row=1, column=2, padx=12, sticky=tk.E, pady=3)
    entry_material_spesifikasi = tk.Entry(group_insert, textvariable=input_material_spesifikasi, font=("Arial", 11), width=12)
    entry_material_spesifikasi.grid(row=1, column=3, padx=3)
    # status
    label_material_status = tk.Label(group_insert, text="Status : ", font=("Arial", 11))
    label_material_status.grid(row=2, column=0, padx=12, sticky=tk.E, pady=3)
    entry_material_status = tk.Entry(group_insert, textvariable=input_status, font=("Arial", 11), width=16)
    entry_material_status.grid(row=2, column=1, padx=3)
    # GROUP BUTTON REVIEW MATERIAL
    group_button_review = tk.Frame(lihat_po)
    group_button_review.grid(row=5, column=0, columnspan=6, pady=3, padx=12, sticky=tk.E)
    # update
    button_update = ttk.Button(group_button_review, text="Update", command=lambda: fn_update_selection(global_selected_spp_id, entry_material_nomor.get(), entry_kuantitas.get(), entry_satuan.get("1.0", "end"), entry_material_status.get()))
    button_update.grid(row=0, column=0, padx=3)
    # clear
    button_clear = ttk.Button(group_button_review, text="Clear", command=fn_clear_selection)
    button_clear.grid(row=0, column=1, padx=3)
    # refresh
    button_update = ttk.Button(group_button_review, text="Refresh", command=lambda: fn_refresh(project_id))
    button_update.grid(row=0, column=2, padx=3)
    # LISTBOX
    # list_result = tk.Listbox(lihat_po, height=12, width=82, border=1)
    # list_result.grid(row=6, column=0, columnspan=6, pady=5)
    # scrollbar = tk.Scrollbar(lihat_po)
    # scrollbar.grid(row=6, column=0, columnspan=6, padx=13, sticky=tk.E)
    # list_result.configure(yscrollcommand=scrollbar.set)
    # scrollbar.configure(command=list_result.yview)
    # Treeview
    treeview_result = ttk.Treeview(lihat_po, height=8)
    # Treeview -> Column declaration
    treeview_result["columns"] = ("ID", "Nomor", "Kode BOM", "Deskripsi", "Spesifikasi", "Kuantitas", "Unit", "Status")
    treeview_result.column("#0", anchor=tk.CENTER, width=0)
    treeview_result.column("ID", anchor=tk.CENTER, width=40)
    treeview_result.column("Nomor", anchor=tk.CENTER, width=80)
    treeview_result.column("Kode BOM", anchor=tk.CENTER, width=80)
    treeview_result.column("Deskripsi", anchor=tk.CENTER, width=140)
    treeview_result.column("Spesifikasi", anchor=tk.CENTER, width=140)
    treeview_result.column("Kuantitas", anchor=tk.CENTER, width=40)
    treeview_result.column("Unit", anchor=tk.CENTER, width=50)
    treeview_result.column("Status", anchor=tk.CENTER, width=125)
    # Treeview -> Heading declaration
    treeview_result.heading("#0", text="", anchor=tk.CENTER)
    treeview_result.heading("ID", text="ID", anchor=tk.CENTER)
    treeview_result.heading("Nomor", text="Nomor", anchor=tk.CENTER)
    treeview_result.heading("Kode BOM", text="Kode BOM", anchor=tk.CENTER)
    treeview_result.heading("Deskripsi", text="Deskripsi", anchor=tk.CENTER)
    treeview_result.heading("Spesifikasi", text="Spesifikasi", anchor=tk.CENTER)
    treeview_result.heading("Kuantitas", text="Σ", anchor=tk.CENTER)
    treeview_result.heading("Unit", text="Satuan", anchor=tk.CENTER)
    treeview_result.heading("Status", text="Keterangan", anchor=tk.CENTER)
    treeview_result.grid(row=6, column=0, padx=13, sticky=tk.E)
    treeview_result.bind("<<TreeviewSelect>>", select_item)
    # Populate to Listbox
    # commands.populate_view_spp(list_result, bom_id, spp_bom_id)
    # Bind selection
    # list_result.bind('<<ListboxSelect>>', select_item)
    populate_treeview_spp(project_id)