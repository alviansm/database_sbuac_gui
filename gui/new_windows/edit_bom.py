import tkinter as tk
from tkinter import ttk
from tkinter import filedialog  
import subprocess, os, platform

from database.database import Database
import gui.new_windows.edit_po as ep
import gui.new_windows.edit_spp as ess

db = Database("sbu_projects.db")

bom_selection_id = 0
def window_edit_bom(master, project_id=0, project_name=""):
    # WINDOW -> konfigurasi window proyek baru
    lihat_bom = tk.Toplevel(master)
    lihat_bom.title("Edit BOM")
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

    project_id = project_id
    filename_path = ""

    # ===FUNCTIONS===
    def fn_clear_view_bom():
        entry_material_rev.delete(0, tk.END)
        entry_material_code.delete(0, tk.END)
        entry_deskripsi.delete(0, tk.END)
        entry_spesifikasi.delete(0, tk.END)
        entry_kuantitas.delete(0, tk.END)
        entry_satuan.delete("1.0", "end")
        entry_keterangan.delete(0, tk.END)
        entry_datasheet_path.delete("1.0", "end")
    
    def fn_clear_search_bom():
        entry_search_material_deskripsi.delete(0, tk.END)
        entry_search_material_kode.delete(0, tk.END)
        entry_search_material_spec.delete(0, tk.END)

    def select_item(event):
        try:            
            selected = treeview_result.selection()[0]
            values = treeview_result.item(selected, 'values')
            # ID    
            global bom_selection_id
            bom_selection_id = values[0]        
            # Rev
            entry_material_rev.delete(0, tk.END)
            entry_material_rev.insert(tk.END, values[1])
            # Kode material
            entry_material_code.delete(0, tk.END)
            entry_material_code.insert(tk.END, values[2])
            # Stok Material
            entry_keterangan.delete(0, tk.END)
            entry_keterangan.insert(tk.END, values[3])
            # Deskripsi
            entry_deskripsi.delete(0, tk.END)
            entry_deskripsi.insert(tk.END, values[4])
            # Spesifikasi
            entry_spesifikasi.delete(0, tk.END)
            entry_spesifikasi.insert(tk.END, values[5])
            # Kuantitas
            entry_kuantitas.delete(0, tk.END)
            entry_kuantitas.insert(tk.END, values[6])
            # Unit
            entry_satuan.delete("1.0", "end")
            entry_satuan.insert(tk.END, values[7])
            # Datasheet Path
            datasheet_row = db.fetch_view_bom_datasheet(entry_material_code.get())
            entry_datasheet_path.delete("1.0", "end")
            entry_datasheet_path.insert(tk.END, datasheet_row)
        except IndexError:
            pass
    
    def clear_treeview_bom():
        for record in treeview_result.get_children():
            treeview_result.delete(record)

    def populate_treeview_bom(project_id):
        clear_treeview_bom()
        for row in db.fetch_view_bom(project_id):
            treeview_result.insert(parent="", index=row[0], iid=row[0], values=(row[0], row[1], row[2], row[7], row[3], row[4], row[5], row[6]))

    def fn_search_treeview(project_id, kode_bom, deskripsi, spesifikasi):
        clear_treeview_bom()
        count = 0
        for row in db.search_material_by(kode_bom, deskripsi, spesifikasi, project_id):
            treeview_result.insert(parent="", index=count, iid=count, values=(row[0], row[1], row[2], row[7], row[3], row[4], row[5], row[6]))
            count += 1

    def update_bom(project_id=0, rev="", kode_material="", deskripsi="", spesifikasi="", kuantitas=0, satuan="", keterangan="", datasheet_path=""):
        # update in database
        db.update_bom(project_id, rev, kode_material, deskripsi, spesifikasi, kuantitas, satuan, keterangan, entry_datasheet_path.get("1.0", "end"))
        # update project filename
        if len(datasheet_path) > 0:
            db.update_bom_filename(str(datasheet_path).strip(), id)
        # clear entries
        fn_clear_view_bom()
        # clear treeview data
        clear_treeview_bom()
        # repopulate bom treeview data
        populate_treeview_bom(project_id)

    def fn_choose_image():
        filepath = filedialog.askopenfilename(initialdir="/", title="Pilih file yang dilink untuk proyek", filetypes=[("All files", ".*")])
        entry_datasheet_path.delete("1.0", "end")
        entry_datasheet_path.insert(tk.END, str(filepath).strip())
        global filename_path
        filename_path = filepath

    def fn_preview_bom_datasheet(kode_material):
        filepath = db.fetch_view_bom_datasheet(kode_material)
        if platform.system() == "Darwin":
            subprocess.call(('open', filepath[0]))
        elif platform.system() == "Windows":
            os.startfile(filepath[0])
        else:
            subprocess.call(('xdg-open', filepath[0]))

    def fn_refresh_treeview():
        clear_treeview_bom()
        populate_treeview_bom()

    def fn_remove_delete(selection_id):
        db.remove_bom(selection_id)
        clear_treeview_bom()
        populate_treeview_bom(bom_selection_id)

    # ===WIDGETS===
    # JUDUL
    if project_name == "":
            title = tk.Label(lihat_bom, text="Edit BOM", pady=4, padx=4, font=("Verdana bold", 12))
            title.grid(row=0, column=0, columnspan=6)        
    else:
            title = tk.Label(lihat_bom, text="Edit BOM : Proyek " + str(project_name), pady=4, padx=4, font=("Verdana bold", 12))
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
    button_search = ttk.Button(group_button_search, text="Clear", command=fn_clear_search_bom)
    button_search.grid(row=0, column=0, sticky=tk.W, padx=12)
    # clear
    button_refresh = ttk.Button(group_button_search, text="Refresh", command=fn_refresh_treeview)
    button_refresh.grid(row=0, column=1, sticky=tk.W, padx=12)
    # cari
    button_search = ttk.Button(group_button_search, text="Cari", command=lambda: fn_search_treeview(project_id, entry_search_material_kode.get(), entry_search_material_deskripsi.get(), entry_search_material_spec.get()))
    button_search.grid(row=0, column=2)
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
    # pilih gambar
    button_select_datasheet = ttk.Button(group_insert, text="Pilih Datasheet", width=14, command=fn_choose_image)
    button_select_datasheet.grid(row=2, column=2, columnspan=2, padx=3, sticky=tk.E)
    # datasheet path
    entry_datasheet_path = tk.Text(group_insert, height=1, width=17)
    entry_datasheet_path.grid(row=2, column=4, columnspan=2, padx=3, sticky=tk.W)
    # GROUP BUTTON REVIEW MATERIAL
    group_button_review = tk.Frame(lihat_bom)
    group_button_review.grid(row=5, column=0, columnspan=6, pady=3, padx=12, sticky=tk.E)
    # hapus bom
    button_delete_bom = ttk.Button(group_button_review, text="Hapus BOM", command=lambda: fn_remove_delete(bom_selection_id))
    button_delete_bom.grid(row=0, column=0, padx=3)
    # clear
    button_clear = ttk.Button(group_button_review, text="Clear", command=fn_clear_view_bom)
    button_clear.grid(row=0, column=2, padx=3)
    # update
    button_update_bom = ttk.Button(group_button_review, text="Update", command=lambda: update_bom(project_id, entry_material_rev.get(), entry_material_code.get(), entry_deskripsi.get(), entry_spesifikasi.get(), entry_kuantitas.get(), entry_satuan.get("1.0", "end"), entry_keterangan.get()))
    button_update_bom.grid(row=0, column=3, padx=3)
    # lihat spp
    button_lihat_spp = ttk.Button(group_button_review, text="Edit SPP", command=lambda: ess.window_edit_spp(master, bom_selection_id, bom_selection_id, project_id))
    button_lihat_spp.grid(row=0, column=4, padx=3)
    # lihat po
    button_lihat_po = ttk.Button(group_button_review, text="Edit PO", command=lambda: ep.window_edit_po(master, bom_selection_id, bom_selection_id, project_id))
    button_lihat_po.grid(row=0, column=5, padx=3)
    # data sheet
    button_datasheet = ttk.Button(group_button_review, text="Data Sheet", command=lambda: fn_preview_bom_datasheet(entry_material_code.get()))
    button_datasheet.grid(row=0, column=6, padx=3)
    # label message
    if project_id == 0:
        label_message = tk.Label(lihat_bom, text="Silahkan pilih proyek dengan mengklik baris proyek pada tabel", font=("Verdana bold", 9), fg="red")
        label_message.grid(row=7, column=0, columnspan=6, pady=2)
    # LISTBOX
    # list_result = tk.Listbox(lihat_bom, height=12, width=82, border=1)
    # list_result.grid(row=6, column=0, columnspan=6, pady=5)
    # scrollbar = tk.Scrollbar(lihat_bom)
    # scrollbar.grid(row=6, column=0, columnspan=6, padx=13, sticky=tk.E)
    # list_result.configure(yscrollcommand=scrollbar.set)
    # scrollbar.configure(command=list_result.yview)
    
    # Treeview
    treeview_result = ttk.Treeview(lihat_bom, height=8)
    
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
    treeview_result.bind("<<TreeviewSelect>>", select_item)

    # commands.populate_view_bom(treeview_result, project_id)
    # list_result.bind('<<ListboxSelect>>', select_item)

    populate_treeview_bom(project_id)
