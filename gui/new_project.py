import tkinter as tk
from tkinter import ttk
from database.database import Database
from PIL import ImageTk, Image
import os

db = Database("sbu_projects.db")

def window_new_project(master, project_name=""):
        # Window -> konfigurasi window proyek baru
        new_project = tk.Toplevel(master)
        new_project.title("Tambah Proyek Baru")
        new_project.geometry("720x480")
        new_project.resizable(False, False)
        new_project.iconbitmap("./favicon.ico")

        # Variables
        # create
        input_project_name = tk.StringVar()
        input_year = tk.IntVar()
        input_capacity = tk.IntVar()
        input_customer = tk.StringVar()
        input_totals = tk.IntVar()
        input_image = tk.StringVar()
        # update
        input_update_project_name = tk.StringVar()
        input_update_year = tk.IntVar()
        input_update_capacity = tk.IntVar()
        input_update_customer = tk.StringVar()
        input_update_totals = tk.IntVar()
        input_update_image = tk.StringVar()

        group_messages(new_project, 0)

        # Judul
        if project_name == "":
                title = tk.Label(new_project, text="Proyek baru", pady=4, padx=4, font=("Verdana bold", 12))
                title.grid(row=0, column=0, columnspan=6)        
        else:
                title = tk.Label(new_project, text=project_name, pady=4, padx=4, font=("Verdana bold", 12))
                title.grid(row=0, column=0, columnspan=6)  
        # Insert proyek baru
        group_insert = tk.LabelFrame(new_project, text="Tambahkan Proyek", font=("Verdana bold", 9))
        group_insert.grid(row=1, column=0, columnspan=6, padx=10)

        label_project_name = tk.Label(group_insert, text="Nama Proyek : ", font=("Arial", 11))
        label_project_name.grid(row=0, column=0, padx=12, sticky=tk.E, pady=3)
        entry_project_name = tk.Entry(group_insert, textvariable=input_project_name, font=("Arial", 11), width=16)
        entry_project_name.grid(row=0, column=1, padx=3)

        label_year = tk.Label(group_insert, text="Tahun: ", font=("Arial", 11))
        label_year.grid(row=0, column=2, sticky=tk.E, padx=6)
        entry_year = tk.Entry(group_insert, textvariable=input_year, font=("Arial", 11), width=6)
        entry_year.grid(row=0, column=3)

        label_capacity = tk.Label(group_insert, text="Kapasitas: ", font=("Arial", 11))
        label_capacity.grid(row=0, column=4, sticky=tk.E, padx=6)
        entry_capacity = tk.Entry(group_insert, textvariable=input_capacity, font=("Arial", 11), width=6)
        entry_capacity.grid(row=0, column=5, sticky=tk.W, padx=6)

        label_customer = tk.Label(group_insert, text="Customer : ", font=("Arial", 11))
        label_customer.grid(row=1, column=0, sticky=tk.E, padx=12, pady=3)
        entry_customer = tk.Entry(group_insert, textvariable=input_customer, font=("Arial", 11), width=16)
        entry_customer.grid(row=1, column=1, padx=3)

        label_totals = tk.Label(group_insert, text="Jumlah Unit: ", font=("Arial", 11))
        label_totals.grid(row=1, column=2, sticky=tk.E, padx=6)
        entry_totals = tk.Entry(group_insert, textvariable=input_totals, font=("Arial", 11), width=6)
        entry_totals.grid(row=1, column=3)

        button_pick_image = ttk.Button(group_insert, text="Pilih Gambar", command=fn_choose_image)
        button_pick_image.grid(row=0, column=6, padx=12, sticky=tk.E)
        # button options for create group -> Tambahkan, Bersihkan
        group_buttons = tk.Frame(new_project)
        group_buttons.grid(row=2, column=0, columnspan=6, padx=10, sticky=tk.W)
        button_insert_project = ttk.Button(group_buttons, text="Tambahkan", command=fn_create_projects)
        button_insert_project.grid(row=0, column=0, padx=6, pady=6, sticky=tk.W)
        button_clear_input = ttk.Button(group_buttons, text="Bersihkan", command=lambda: fn_clear_create_project_form(entry_project_name, entry_year, entry_capacity, entry_customer, entry_totals))
        button_clear_input.grid(row=0, column=1, sticky=tk.W)

        # Update proyek
        group_update = tk.LabelFrame(new_project, text="Update Proyek", font=("Verdana bold", 9))
        group_update.grid(row=3, column=0, columnspan=6, padx=10)

        label_update_project_name = tk.Label(group_update, text="Nama Proyek : ", font=("Arial", 11))
        label_update_project_name.grid(row=0, column=0, padx=12, sticky=tk.E, pady=3)
        entry_update_project_name = tk.Entry(group_update, textvariable=input_update_project_name, font=("Arial", 11), width=16)
        entry_update_project_name.grid(row=0, column=1, padx=3)

        label_update_year = tk.Label(group_update, text="Tahun: ", font=("Arial", 11))
        label_update_year.grid(row=0, column=2, sticky=tk.E, padx=6)
        entry_update_year = tk.Entry(group_update, textvariable=input_update_year, font=("Arial", 11), width=6)
        entry_update_year.grid(row=0, column=3)

        label_update_capacity = tk.Label(group_update, text="Kapasitas: ", font=("Arial", 11))
        label_update_capacity.grid(row=0, column=4, sticky=tk.E, padx=6)
        entry_update_capacity = tk.Entry(group_update, textvariable=input_update_capacity, font=("Arial", 11), width=6)
        entry_update_capacity.grid(row=0, column=5, sticky=tk.W, padx=6)

        label_update_customer = tk.Label(group_update, text="Customer : ", font=("Arial", 11))
        label_update_customer.grid(row=1, column=0, sticky=tk.E, padx=12, pady=3)
        entry_update_customer = tk.Entry(group_update, textvariable=input_update_customer, font=("Arial", 11), width=16)
        entry_update_customer.grid(row=1, column=1, padx=3)

        label_update_totals = tk.Label(group_update, text="Jumlah Unit: ", font=("Arial", 11))
        label_update_totals.grid(row=1, column=2, sticky=tk.E, padx=6)
        entry_update_totals = tk.Entry(group_update, textvariable=input_update_totals, font=("Arial", 11), width=6)
        entry_update_totals.grid(row=1, column=3)

        button_update_img = ttk.Button(group_update, text="Ganti Gambar", command=fn_choose_image)
        button_update_img.grid(row=0, column=6, padx=12, sticky=tk.E)
        # Tombol opsi -> Edit BOM, SPP, PO
        group_buttons_update = tk.Frame(new_project)
        group_buttons_update.grid(row=4, column=0, columnspan=6, padx=10, sticky=tk.W)
        button_update_project = ttk.Button(group_buttons_update, text="Update", command=fn_create_projects)
        button_update_project.grid(row=0, column=0, padx=6, pady=6, sticky=tk.W)
        button_clear_update = ttk.Button(group_buttons_update, text="Bersihkan", command=fn_clear_create_project_form)
        button_clear_update.grid(row=0, column=1, sticky=tk.W, padx=6)
        button_remove_update = ttk.Button(group_buttons_update, text="Hapus", command=fn_clear_create_project_form)
        button_remove_update.grid(row=0, column=2, sticky=tk.W, padx=6)
        
        button_edit_bom = ttk.Button(group_buttons_update, text="Edit PO", command=fn_clear_create_project_form)
        button_edit_bom.grid(row=0, column=3, sticky=tk.E, padx=6)
        button_edit_bom = ttk.Button(group_buttons_update, text="Edit SPP", command=fn_clear_create_project_form)
        button_edit_bom.grid(row=0, column=4, sticky=tk.E, padx=6)
        button_edit_bom = ttk.Button(group_buttons_update, text="Edit BOM", command=fn_clear_create_project_form)
        button_edit_bom.grid(row=0, column=5, sticky=tk.E, padx=6)

        # Listbox
        listbox_result = tk.Listbox(new_project, height=8, width=84, border=1)
        listbox_result.grid(row=5, column=0, pady=5, padx=10)
        result_scrollbar = tk.Scrollbar(new_project)
        result_scrollbar.grid(row=5, column=0, sticky=tk.E)
        listbox_result.configure(yscrollcommand=result_scrollbar.set)
        result_scrollbar.configure(command=listbox_result.yview)

        # Clear available inputs
        fn_clear_create_project_form(entry_project_name, entry_year, entry_capacity, entry_customer, entry_totals)
        fn_clear_create_project_form(entry_update_project_name, entry_update_year, entry_update_capacity, entry_update_customer, entry_update_totals)
        populate_list(listbox_result)

def populate_list(parent_widget):
        parent_widget.delete(0, tk.END)
        for row in db.fetch():
            parent_widget.insert(tk.END, row)

def fn_choose_image():
        print("Choose Image")

def fn_create_projects():
        print("Added 1 row")

def fn_clear_create_project_form(*entries):
        temp_entries = list(entries)
        for entry in temp_entries:
                entry.delete(0, tk.END)

def group_messages(parent, code=0):
        MESSAGES = [
            "Database berhasil dipilih",
            "Berhasil menambahkan proyek baru",
            "Berhasil mengupdate data proyek",
            "Pencarian ditemukan",
            "Pencarian tidak ditemukan",
            "Database masih kosong"
        ]
        msg_selection = MESSAGES[0]

        # Switch case

        # Label -> messages
        label_message = tk.Label(parent, text=msg_selection, fg="red", font=("Arial", 9))
        label_message.grid(row=6, column=0)
