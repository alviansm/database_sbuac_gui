import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from database.database import Database
import gui.commands.commands as command
import gui.new_windows.edit_bom as eb

db = Database("sbu_projects.db")

input_update_project_id = 0
def window_new_project(master, project_name=""):
        # Window -> konfigurasi window proyek baru
        new_project = tk.Toplevel(master)
        new_project.title("Tambah Proyek Baru")
        new_project.geometry("720x480")
        new_project.resizable(False, False)
        new_project.iconbitmap("./favicon.ico")

        # Functions
        def populate_list_treeview():
                i = 0
                for row in db.fetch():
                        treeview_result.insert(parent="", index=i, iid=i, values=row)
                        i = i + 1
        def select_item(event):
                try:     
                        global input_update_project_id       
                        selected = treeview_result.selection()[0]
                        values = treeview_result.item(selected, 'values')
                        input_update_project_name = values[1]
                        input_update_year = values[2]
                        input_update_capacity = values[3]
                        input_update_customer = values[4]
                        input_update_totals = values[5]
                        # id
                        input_update_project_id = values[0]
                        # nama proyek
                        entry_update_project_name.delete(0, tk.END)
                        entry_update_project_name.insert(tk.END, input_update_project_name)
                        # tahun
                        entry_update_year.delete(0, tk.END)
                        entry_update_year.insert(tk.END, input_update_year)
                        # kapasitas
                        entry_update_capacity.delete(0, tk.END)
                        entry_update_capacity.insert(tk.END, input_update_capacity)
                        # customer
                        entry_update_customer.delete(0, tk.END)
                        entry_update_customer.insert(tk.END, input_update_customer)
                        # jumlah
                        entry_update_totals.delete(0, tk.END)
                        entry_update_totals.insert(tk.END, input_update_totals)
                except IndexError:
                        pass

        def fn_choose_image():
                filepath = filedialog.askopenfilename(initialdir="/", title="Pilih file yang dilink untuk proyek", filetypes=[("All files", ".*")])
                text_image.delete("1.0", "end")
                text_image.insert(tk.END, filepath)        

        def update_projects(id=0, project_name="", year=0, capacity=0, customer="", totals=0, image=""):                
                db.update(id, project_name, year, capacity, customer, totals)
                db.update_project_filename(str(image).strip(), id)                        
                command.fn_clear_entries(entry_update_project_name, entry_update_year, entry_update_capacity, entry_update_customer, entry_update_totals)
                text_image.delete("1.0", "end")
                clear_treeview_data()
                populate_list_treeview()  

        def project_add():
                if (input_project_name.get() == "" or input_year.get() < 1900 or input_capacity.get() < 0 or input_customer.get() == "" or input_totals.get() <= 0):
                    messagebox.showerror('Semua Entry Harus Diisi', 'Tolong isi semua entry yang tersedia')
                    return
                db.insert(input_project_name.get(), input_year.get(), input_capacity.get(), input_customer.get(), input_totals.get(), "")
                clear_treeview_data()
                # listbox_result.insert(tk.END, (input_project_name.get(), self.update_tahun.get(), self.update_kapasitas.get(), self.update_customer.get(), self.update_jumlah.get()))
                command.fn_clear_entries(entry_project_name, entry_year, entry_capacity, entry_customer, entry_totals)
                clear_treeview_data()
                populate_list_treeview()                      

        def clear_treeview_data():
                for record in treeview_result.get_children():
                        treeview_result.delete(record)

        def fn_remove_project(x):
                db.remove(x)
                clear_treeview_data()
                populate_list_treeview()

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
        button_insert_project = ttk.Button(group_buttons, text="Tambahkan", command=project_add)
        button_insert_project.grid(row=0, column=0, padx=6, pady=6, sticky=tk.W)
        button_clear_input = ttk.Button(group_buttons, text="Bersihkan", command=lambda: command.fn_clear_entries(entry_project_name, entry_year, entry_capacity, entry_customer, entry_totals))
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
        text_image = tk.Text(group_update, height=1, width=6)
        text_image.grid(row=1, column=6)
        # Tombol opsi -> Edit BOM, SPP, PO
        group_buttons_update = tk.Frame(new_project)
        group_buttons_update.grid(row=4, column=0, columnspan=6, padx=10, sticky=tk.W)
        button_update_project = ttk.Button(group_buttons_update, text="Update", command=lambda: update_projects(input_update_project_id, entry_update_project_name.get(), entry_update_year.get(), entry_update_capacity.get(), entry_update_customer.get(), entry_update_totals.get(), text_image.get("1.0", "end")))
        button_update_project.grid(row=0, column=0, padx=6, pady=6, sticky=tk.W)
        button_clear_update = ttk.Button(group_buttons_update, text="Bersihkan", command=lambda: command.fn_clear_entries(entry_update_project_name, entry_update_year, entry_update_capacity, entry_update_customer, entry_update_totals))
        button_clear_update.grid(row=0, column=1, sticky=tk.W, padx=6)
        button_remove_update = ttk.Button(group_buttons_update, text="Hapus", command=lambda: fn_remove_project(input_update_project_id))
        button_remove_update.grid(row=0, column=2, sticky=tk.W, padx=6)
        button_edit_bom = ttk.Button(group_buttons_update, text="Edit BOM", command=lambda: eb.window_edit_bom(new_project, input_update_project_id, entry_update_project_name.get()))
        button_edit_bom.grid(row=0, column=3, sticky=tk.E, padx=6)
        button_refresh_update = ttk.Button(group_buttons_update, text="Refresh", command=populate_list_treeview)
        button_refresh_update.grid(row=0, column=4, sticky=tk.W, padx=6)

        # Treeview
        treeview_result = ttk.Treeview(new_project, height=8)
        # Column declaration
        treeview_result['columns'] = ("ID", "Nama Proyek", "Tahun", "Kapasitas", "Customer", "Jumlah Unit")
        treeview_result.column("#0", anchor=tk.CENTER, width=0)
        treeview_result.column("ID", anchor=tk.CENTER, width=45)        
        treeview_result.column("Nama Proyek", anchor=tk.CENTER, width=125)
        treeview_result.column("Tahun", anchor=tk.CENTER, width=125)
        treeview_result.column("Kapasitas", anchor=tk.CENTER, width=125)
        treeview_result.column("Customer", anchor=tk.CENTER, width=125)
        treeview_result.column("Jumlah Unit", anchor=tk.CENTER, width=125)
        # Heading declaration
        treeview_result.heading("#0", text="", anchor=tk.CENTER)
        treeview_result.heading("ID", text="ID", anchor=tk.CENTER)
        treeview_result.heading("Nama Proyek", text="Nama Proyek", anchor=tk.CENTER)
        treeview_result.heading("Tahun", text="Tahun", anchor=tk.CENTER)
        treeview_result.heading("Kapasitas", text="Kapasitas", anchor=tk.CENTER)
        treeview_result.heading("Customer", text="Customer", anchor=tk.CENTER)
        treeview_result.heading("Jumlah Unit", text="Jumlah Unit", anchor=tk.CENTER)
        # Event binder
        treeview_result.bind("<<TreeviewSelect>>", select_item)
        treeview_result.grid(row=5, column=0, padx=24)
        
        # Clear available inputs
        command.fn_clear_entries(entry_project_name, entry_year, entry_capacity, entry_customer, entry_totals)
        command.fn_clear_entries(entry_update_project_name, entry_update_year, entry_update_capacity, entry_update_customer, entry_update_totals)

        populate_list_treeview()