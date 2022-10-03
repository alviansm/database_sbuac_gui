import tkinter as tk

def fn_clear_entries(*entries):
        temp_entries = list(entries)
        for entry in temp_entries:
                entry.delete(0, tk.END)
