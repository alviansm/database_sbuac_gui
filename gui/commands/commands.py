import tkinter as tk
import pandas as pd
from tkinter import messagebox

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

def populate_view_po(widget_listbox, bom_id, spp_bom_id):
	widget_listbox.delete(0, tk.END)
	for row in db.fetch_view_po(bom_id, spp_bom_id):
		widget_listbox.insert(tk.END, row)

def fn_clear_entries(*entries):
	temp_entries = list(entries)
	for entry in temp_entries:
		entry.delete(0, tk.END)

def excel_to_list_insert(path, selected_project, label_to_update):
	try:
		bom_id_ref = 1
		df = pd.read_excel(path, sheet_name="BOM", skiprows=5, usecols='B:R')
		df_value = df.values
		for val in df_value:
			db.insert_bom(int(val[1]), val[2], val[3], val[4], val[5], val[6], selected_project[0], val[16])
			db.insert_spp(int(val[7]), val[8], val[9], val[10], selected_project[0], bom_id_ref)
			db.insert_po(int(val[11]), val[12], val[13], val[14], val[15], selected_project[0], bom_id_ref)
			bom_id_ref = bom_id_ref + 1
		label_to_update.configure(text="Berhasil mengimpor.", fg="green")
		messagebox.showinfo("Info", "Berhasil mengimpor")
	except:
		messagebox.showerror("Error", "Terjadi kegagalan, silahkan laporkan ke pengembang")