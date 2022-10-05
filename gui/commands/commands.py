import tkinter as tk
from database.database import Database

db = Database("sbu_projects.db")

def populate_view_bom(widget_listbox, project_id):
        widget_listbox.delete(0, tk.END)
        for row in db.fetch_view_bom(project_id):
                widget_listbox.insert(tk.END, row)

def populate_view_spp(widget_listbox, bom_id, spp_bom_id):
        widget_listbox.delete(0, tk.END)
        for row in db.fetch_view_spp(bom_id, spp_bom_id):
                widget_listbox.insert(tk.END, row)

def fn_clear_entries(*entries):
        temp_entries = list(entries)
        for entry in temp_entries:
                entry.delete(0, tk.END)
