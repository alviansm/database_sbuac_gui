import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox
import time

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

def excel_to_list_insert(path, selected_project):	
	# try:
	df = pd.read_excel(path, skiprows=5, usecols='B:R')
	df = df.dropna()
	df_value = df.values
	for val in df_value:
		db.insert_bom(val[1], val[2], val[3], val[4], val[5], val[6], selected_project[0], val[16], int(val[0]))
		db.insert_spp(val[7], val[8], val[9], val[10], selected_project[0], int(val[0]))
		db.insert_po(val[11], val[12], val[13], val[14], val[15], selected_project[0], int(val[0]))
	# except:
	# 	messagebox.showerror("Error", "Terjadi kegagalan, silahkan laporkan ke pengembang")