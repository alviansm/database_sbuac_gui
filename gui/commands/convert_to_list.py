import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import time
from database.database import Database
import gui.commands.commands as commands

db = Database("sbu_projects.db")

filename_path = "Silahkan pilih Excel"
PROJECT_SELECTION = []

def fn_window_import_excel(parent):
    window_import = tk.Toplevel(parent)
    window_import.title("Import")
    window_import.geometry("356x164")
    window_import.resizable(True, True)
    window_import.iconbitmap("./favicon.ico")
    window_import.attributes('-topmost', True)
    window_import.update()

    global filename_path
    global PROJECT_SELECTION
    project_selected = tk.StringVar()

    def query_project_name():
        res = []        
        temp_res = db.query_for_importing()
        res.append("Silahkan Pilih Proyek")
        for r in temp_res:
            res.append(r)
        return res    

    PROJECT_SELECTION = query_project_name()
    project_selected.set(PROJECT_SELECTION[0])

    def start_import(path, project):
        messagebox.showinfo("Memulai", "Silahkan tunggu hingga muncul notifikasi berikutnya..")
        label_status.configure(text="Loading..", background="cyan")
        # Progress
        commands.excel_to_list_insert(path, project)
        label_status.configure(text="Berhasil mengimpor", fg="green")
        messagebox.showinfo("Info", "Berhasil mengimpor")

    # Judul
    label_title = tk.Label(window_import, text="Impor database dari Excel", font=("Verdana bold", 8))
    label_title.pack(pady=6)
    # Tombol
    group_buttons = tk.Frame(window_import)
    group_buttons.pack()

    button_choose = ttk.Button(group_buttons, text="Pilih Excel", command=lambda: fn_choose_file(label_filename))
    button_choose.grid(row=0, column=0, padx=3)
    button_submit = ttk.Button(group_buttons, text="Mulai", command=lambda:  start_import(filename_path, project_selected.get()))
    button_submit.grid(row=0, column=1)
    # Select project group
    group_select_project = tk.Frame(window_import)
    group_select_project.pack()

    label_select_project = tk.Label(group_select_project, text="Proyek :", font=("Arial", 11))
    label_select_project.grid(row=0, column=0)
    entry_select_project = ttk.OptionMenu(group_select_project, project_selected, *PROJECT_SELECTION)
    entry_select_project.grid(row=0, column=1)
    # Progress bar
    label_status = tk.Label(window_import, text="Silahkan pilih excel kemudian proyek untuk ditambah BOM", fg="gray", font=("Arial", 9))
    label_status.pack()
    # Label
    label_filename = tk.Text(window_import, font=("Arial", 8), width=20, height=2)
    label_filename.insert(tk.END, filename_path)
    label_filename.pack(pady=6)

    def fn_choose_file(wid_to_update):
        global filename_path    
        try:        
            filename = filedialog.askopenfilename(initialdir="/", title="Pilih file excel", filetypes=[("Excel file", ".xlsx .xls")])
            filename_path = filename        
            wid_to_update.delete("1.0", "end")
            wid_to_update.insert(tk.END, filename_path)               
            label_status.configure(text="Berhasil mengimpor, silahkan pilih proyek kemudian mulai", fg="green") 
        except:
            filename_path = "Gagal dalam memilih file"
            wid_to_update.delete("1.0", "end")
            wid_to_update.insert(tk.END, filename_path)
            label_status.configure(text="Gagal", fg="red")
        return filename_path