import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

filename_path = "Silahkan pilih Excel"

def fn_window_import_excel(parent):
    window_import = tk.Toplevel(parent)
    window_import.title("Import")
    window_import.geometry("296x148")
    window_import.resizable(False, False)
    window_import.iconbitmap("./favicon.ico")
    window_import.attributes('-topmost', True)
    window_import.update()

    global filename_path

    # Judul
    label_title = tk.Label(window_import, text="Impor database dari Excel", font=("Verdana bold", 9))
    label_title.pack()
    # Tombol
    button_choose = ttk.Button(window_import, text="Pilih", command=lambda: fn_choose_file(window_import, label_filename))
    button_choose.pack()
    # Label
    label_filename = tk.Text(window_import, font=("Arial", 8), width=20, height=2)
    label_filename.insert(tk.END, filename_path)
    label_filename.pack(pady=6)    
    
def fn_choose_file(parent, wid_to_update):
    global filename_path
    try:
        filename = filedialog.askopenfilename(initialdir="/", title="Pilih file excel", filetypes=[("Excel file", ".xlsx .xls")])
        filename_path = filename
        wid_to_update.delete("1.0", "end")
        wid_to_update.insert(tk.END, filename_path)
    except:
        filename_path = "Gagal dalam memilih file"
        wid_to_update.delete("1.0", "end")
        wid_to_update.insert(tk.END, filename_path)

    print(filename_path)
    return filename_path

