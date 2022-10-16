import tkinter as tk
from tkinter import CENTER, ttk
from tkinter import font
from tkinter import messagebox
from turtle import width
from PIL import ImageTk, Image
import subprocess, os, platform

from database.database import Database
import gui.new_windows.new_project as np
import gui.new_windows.auth as auth
import gui.commands.commands as command
import gui.commands.convert_to_list as ctl
import gui.new_windows.lihat_bom as lb

db = Database("sbu_projects.db")

# bom
# db.insert_bom("c", "CXY41", "Kompresor Super", "Emerson C41", 20, "unit", 2, 0)
# spp
# db.insert_spp("SBUAC/2021/OK", 20, "unit", 0, 1, 2)
# po
# db.insert_po("SBUAC/MNTP/", 20, "unit", "ZXCRUST", "20/12/2022", 1, 2)

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('PYKonektor (Beta)')
        master.geometry("720x520")
        master.resizable(False, False)
        master.iconbitmap("./favicon.ico")
        
        # Preference -> Font
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Arial", size=11, weight=font.NORMAL)

        # Year dropdown options
        self.Y_OPTIONS = [
            "2022",
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",            
            "2023",
            "SEMUA"
        ]
        self.U_OPTIONS = [
            "meter",
        ]

        # INPUT VARIABLES
        # Search Group
        # id
        self.selected_project_id = 0
        # tahun
        self.search_year = tk.StringVar()
        self.search_year.set(self.Y_OPTIONS[0]) # "2022"
        # nama
        self.search_name = tk.StringVar()
        # kode
        self.search_bomcode = tk.StringVar()
        # tipe pencarian
        self.search_cb_project_val = tk.IntVar(value=1)
        self.search_cb_component_val = tk.IntVar(value=0)
        # Update Group
        # nama proyek
        self.update_nama = tk.StringVar()
        # tahun proyek (integer)
        self.update_tahun = tk.IntVar()
        # kapasitas ac (integer)
        self.update_kapasitas = tk.IntVar()
        # customer
        self.update_customer = tk.StringVar()
        # jumlah (integer)
        self.update_jumlah = tk.IntVar()

        # Selected Item
        self.selected_project = ""

        # Create menu bar
        self.app_menu = tk.Menu(self.master, font=("Arial", 11))
        master.config(menu=self.app_menu)
        self.create_menu_items()
        
        # Initiate widgets
        self.create_widgets()

        # Pupulate List
        # self.populate_list()
        self.populate_list_treeview()
        
    def create_widgets(self):
        self.group_title()
        self.group_search_by_year()
        self.group_data_update()
        # self.group_list_result()
        self.treeview_list_result()
        self.fn_clear_selection()
        self.fn_group_button_options()

    # Menu commands
    def menu_commands(self):
        pass

    def create_menu_items(self):
        # File
        self.file_menu = tk.Menu(self.app_menu, tearoff=False, font=("Arial", 11))
        self.app_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Impor dari Excel", command=lambda: ctl.fn_window_import_excel(self.master))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Ekspor database", command=self.menu_commands)
        self.file_menu.add_command(label="Backup database", command=self.menu_commands)
        self.file_menu.add_command(label="Pilih database", command=self.menu_commands) 
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Preferensi", command=self.menu_commands)               
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Keluar", command=self.master.quit)

        # Edit
        self.tambah_menu = tk.Menu(self.app_menu, tearoff=False, font=("Arial", 11))
        self.app_menu.add_cascade(label="Edit", menu=self.tambah_menu)
        self.tambah_menu.add_command(label="Proyek Baru", command=lambda: np.window_new_project(self.master))
        # self.tambah_menu.add_command(label="Edit BOM", command=self.menu_commands)
        # self.tambah_menu.add_command(label="Edit SPP", command=self.menu_commands)
        # self.tambah_menu.add_command(label="Edit PO", command=self.menu_commands)

        # Ekspor
        self.export_menu = tk.Menu(self.app_menu, tearoff=False, font=("Arial", 11))
        self.app_menu.add_cascade(label="Ekspor", menu=self.export_menu)
        self.export_menu.add_command(label="Sebagai Excel", command=self.menu_commands)
        self.export_menu.add_command(label="Sebagai CSV", command=self.menu_commands)
        self.export_menu.add_command(label="Sebaga PDF", command=self.menu_commands)

        # Autentikasi
        # self.auth_menu = tk.Menu(self.app_menu, tearoff=False, font=("Arial", 11))
        # self.app_menu.add_cascade(label="Autentikasi", menu=self.auth_menu)
        # self.auth_menu.add_command(label="Login", command=lambda: auth.fn_window_authentication(self.master))
        # self.auth_menu.add_command(label="Buat Akun", command=self.menu_commands)
        # self.auth_menu.add_separator()
        # self.auth_menu.add_command(label="Pengaturan Akun", command=self.menu_commands)
        # self.auth_menu.add_separator()
        # self.auth_menu.add_command(label="Sign Out", command=self.menu_commands)

        # Petunjuk
        self.bantuan_menu = tk.Menu(self.app_menu, font=("Arial", 11), tearoff=False)
        self.app_menu.add_cascade(label="Petunjuk", menu=self.bantuan_menu)
        self.bantuan_menu.add_command(label="Cara Penggunaan", command=self.menu_commands)
        # self.bantuan_menu.add_command(label="Petunjuk membagikan database", command=self.menu_commands)
        self.bantuan_menu.add_separator()
        self.bantuan_menu.add_command(label="Tentang Kami", command=self.show_popup_about)

    def group_title(self):
        # Judul
        self.frame_title = tk.Frame(self.master).grid(row=0, column=0)
        self.label_tittle = tk.Label(self.frame_title, text="Database Proyek", font=("Verdana", 14)).grid(row=0, column=0, pady=6)

    def group_search_by_year(self):
        # Frame pencarian
        self.frame_search_by_year = tk.LabelFrame(self.master, text="Cari", pady=5, padx=5, font=("Verdana Bold", 9))
        self.frame_search_by_year.grid(row=1, column=0, sticky=tk.W, pady=5, padx=17)

        # Pilih tahun
        self.label_year = tk.Label(self.frame_search_by_year, text="Tahun : ")
        self.label_year.grid(row=1, column=0, sticky=tk.E)
        self.search_year_entry = ttk.OptionMenu(self.frame_search_by_year, self.search_year, *self.Y_OPTIONS)
        self.search_year_entry.grid(row=1, column=1, sticky=tk.E)

        # Entry nama
        self.label_name = tk.Label(self.frame_search_by_year, text="Nama Proyek : ")
        self.label_name.grid(row=0, column=0)
        self.entry_name = tk.Entry(self.frame_search_by_year, textvariable=self.search_name, font=("Arial", 11), width=16)
        self.entry_name.grid(row=0, column=1)         

        # Entry project code
        self.label_bom_code = tk.Label(self.frame_search_by_year, text="Kode Proyek : ")
        self.label_bom_code.grid(row=0, column=2, padx=12, sticky=tk.E)
        self.entry_project_code = tk.Entry(self.frame_search_by_year, textvariable=self.search_bomcode, font=("Arial", 11), width=16)
        self.entry_project_code.grid(row=0, column=3)  

        # Tombol cari
        self.button_year_search = ttk.Button(self.frame_search_by_year, text="Cari", width=8, padding=1, command=lambda: self.fn_search_treeview_by(self.search_year.get(), self.search_name.get(), self.search_bomcode.get()))
        self.button_year_search.grid(row=0, column=6, padx=1, sticky=tk.E)

        # Checkbox -> Proyek / Component option
        self.search_cb_project = tk.Checkbutton(self.frame_search_by_year, text="Proyek", variable=self.search_cb_project_val).grid(row=0, column=4, sticky=tk.W)
        self.search_cb_project
        self.search_cb_component = tk.Checkbutton(self.frame_search_by_year, text="Komponen", variable=self.search_cb_component_val).grid(row=1, column=4)

    def group_data_update(self):
        # Frame update project
        self.frame_data_update = tk.LabelFrame(self.master, text="Preview", pady=5, padx=5, font=("Verdana Bold", 9))
        self.frame_data_update.grid(row=2, column=0, sticky=tk.W, pady=5, padx=17)

        # Entry nama proyek
        self.label_project_name = tk.Label(self.frame_data_update, text="Nama Proyek : ")
        self.label_project_name.grid(row=0, column=0)
        self.entry_project_name = tk.Entry(self.frame_data_update, textvariable=self.update_nama, font=("Arial", 11), width=16)
        self.entry_project_name.grid(row=0, column=1)

        # Entry tahun proyek
        self.label_project_year = tk.Label(self.frame_data_update, text="Tahun : ")
        self.label_project_year.grid(row=1, column=0, sticky=tk.E)
        self.entry_project_year = tk.Entry(self.frame_data_update, textvariable=self.update_tahun, font=("Arial", 11), width=16)
        self.entry_project_year.grid(row=1, column=1, pady=7)

        # Entry kapasitas AC
        self.label_project_capacity = tk.Label(self.frame_data_update, text="Kapasitas AC : ")
        self.label_project_capacity.grid(row=0, column=2, sticky=tk.E, padx=12)
        self.entry_project_capacity = tk.Entry(self.frame_data_update, textvariable=self.update_kapasitas, font=("Arial", 11), width=16)
        self.entry_project_capacity.grid(row=0, column=3, sticky=tk.E)

        # Entry customer
        self.label_project_customer = tk.Label(self.frame_data_update, text="Customer : ")
        self.label_project_customer.grid(row=1, column=2, sticky=tk.E, padx=12)
        self.entry_project_customer = tk.Entry(self.frame_data_update, textvariable=self.update_customer, font=("Arial", 11), width=16)
        self.entry_project_customer.grid(row=1, column=3, pady=7, sticky=tk.E)

        # Entry jumlah unit AC
        self.label_project_units = tk.Label(self.frame_data_update, text="Jumlah : ")
        self.label_project_units.grid(row=0, column=4, padx=3)
        self.entry_project_units = tk.Entry(self.frame_data_update, textvariable=self.update_jumlah, font=("Arial", 11), width=12)
        self.entry_project_units.grid(row=0, column=5, pady=7)

    def fn_group_button_options(self):
        self.group_button_options = tk.Frame(self.master)
        self.group_button_options.grid(row=3, column=0, padx=20, pady=5, sticky=tk.W)

        self.button_clear = ttk.Button(self.group_button_options, text="Data Sheet", command=lambda: self.preview_file(self.selected_project_id))
        self.button_clear.grid(row=0, column=0, sticky=tk.W)
        self.button_show_bom = ttk.Button(self.group_button_options, text="Lihat BOM", command=lambda: lb.window_lihat_bom(self.master, project_id=self.selected_project_id, project_name=self.update_nama))
        self.button_show_bom.grid(row=0, column=1, padx=12)
        self.button_show_image = ttk.Button(self.group_button_options, text="Clear", command=lambda: command.fn_clear_entries(self.entry_project_name, self.entry_project_year, self.entry_project_capacity, self.entry_project_customer, self.entry_project_units))
        self.button_show_image.grid(row=0, column=2, sticky=tk.E)
        self.button_show_image = ttk.Button(self.group_button_options, text="Refresh", command=self.populate_list_treeview)
        self.button_show_image.grid(row=0, column=3, padx=12, sticky=tk.E)

    def group_list_result(self):
        # Widget -> List (Untuk hasil fetch database)
        self.list_result = tk.Listbox(self.master, height=8, width=82, border=1)
        self.list_result.grid(row=4, column=0, pady=5)
        
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=4, column=0, padx=13, sticky=tk.E)
        self.list_result.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.list_result.yview)

        # Bind selection
        self.list_result.bind('<<ListboxSelect>>', self.select_item)
    
    def treeview_list_result(self):
        self.treeview_result = ttk.Treeview(self.master, height=8)
        self.treeview_result.grid(row=4, column=0, pady=5)

        # Column declaration
        self.treeview_result['columns'] = ("ID", "Nama Proyek", "Tahun", "Kapasitas", "Customer", "Jumlah Unit")
        self.treeview_result.column("#0", anchor=CENTER, width=0)
        self.treeview_result.column("ID", anchor=CENTER, width=45)        
        self.treeview_result.column("Nama Proyek", anchor=CENTER, width=125)
        self.treeview_result.column("Tahun", anchor=CENTER, width=125)
        self.treeview_result.column("Kapasitas", anchor=CENTER, width=125)
        self.treeview_result.column("Customer", anchor=CENTER, width=125)
        self.treeview_result.column("Jumlah Unit", anchor=CENTER, width=125)
        # Heading declaration
        self.treeview_result.heading("#0", text="", anchor=CENTER)
        self.treeview_result.heading("ID", text="ID", anchor=CENTER)
        self.treeview_result.heading("Nama Proyek", text="Nama Proyek", anchor=CENTER)
        self.treeview_result.heading("Tahun", text="Tahun", anchor=CENTER)
        self.treeview_result.heading("Kapasitas", text="Kapasitas", anchor=CENTER)
        self.treeview_result.heading("Customer", text="Customer", anchor=CENTER)
        self.treeview_result.heading("Jumlah Unit", text="Jumlah Unit", anchor=CENTER)
        # Change variable
        self.treeview_result.bind("<<TreeviewSelect>>", self.clicker)
        # Strip configuration
        self.treeview_result.tag_configure("oddrow", background="white")
        self.treeview_result.tag_configure("evenrow", background="lightgray")

    # Treeview select event handler
    def clicker(self, event):        
        try:            
            selected = self.treeview_result.selection()[0]
            values = self.treeview_result.item(selected, 'values')
            self.update_nama = values[1]
            self.update_tahun = values[2]
            self.update_kapasitas = values[3]
            self.update_customer = values[4]
            self.update_jumlah = values[5]
            # nama proyek
            self.entry_project_name.delete(0, tk.END)
            self.entry_project_name.insert(tk.END, self.update_nama)
            # tahun
            self.entry_project_year.delete(0, tk.END)
            self.entry_project_year.insert(tk.END, self.update_tahun)
            # kapasitas
            self.entry_project_capacity.delete(0, tk.END)
            self.entry_project_capacity.insert(tk.END, self.update_kapasitas)
            # customer
            self.entry_project_customer.delete(0, tk.END)
            self.entry_project_customer.insert(tk.END, self.update_customer)
            # jumlah
            self.entry_project_units.delete(0, tk.END)
            self.entry_project_units.insert(tk.END, self.update_jumlah)
            # project id
            self.selected_project_id = values[0]
            self.update_nama = self.entry_project_name.get()
        except IndexError:
            pass

    # Populate database to treeview
    def populate_list_treeview(self):
        self.clear_treeview_data()
        count = 0
        for row in db.fetch():
            if count % 2 == 0:
                self.treeview_result.insert(parent="", index=count, iid=count, values=row, tags=("evenrow",))
            else:
                self.treeview_result.insert(parent="", index=count, iid=count, values=row, tags=("oddrow",))
            count += 1

    # Clear data in treeview
    def clear_treeview_data(self):
        for record in self.treeview_result.get_children():
            self.treeview_result.delete(record)

    # Populate database to list_result widget
    def populate_list(self):
        self.list_result.delete(0, tk.END)
        for row in db.fetch():
            self.list_result.insert(tk.END, row)

    def fn_search_by(self, param_year, param_name, param_id):
        self.list_result.delete(0, tk.END)
        for row in db.search_by_year(param_year, param_name, param_id):
            self.list_result.insert(tk.END, row)
    
    def fn_search_treeview_by(self, param_year, param_name, param_id):
        self.clear_treeview_data()
        for row in db.search_by_year(param_year, param_name, param_id):
            self.treeview_result.insert(parent="", index=row[0], iid=row[0], values=row)

    # Used in new window -> tambah proyek
    def project_add(self):
        if (self.update_nama.get() == "" and self.update_tahun.get() < 1900 and self.update_kapasitas.get() < 0 and self.update_customer.get() == "" and self.update_jumlah.get() <= 0):
            messagebox.showerror('Semua Entry Harus Diisi', 'Tolong isi semua entry yang tersedia')
            return
        db.insert(self.update_nama.get(), self.update_tahun.get(), self.update_kapasitas.get(), self.update_customer.get(), self.update_jumlah.get(), "")
        self.list_result.delete(0, tk.END)
        self.list_result.insert(tk.END, (self.update_nama.get(), self.update_tahun.get(), self.update_kapasitas.get(), self.update_customer.get(), self.update_jumlah.get()))
        self.fn_clear_selection()
        self.populate_list()

    def select_item(self, event):
        try:
            index = self.list_result.curselection()[0]
            self.selected_project = self.list_result.get(index)            
            # nama proyek
            self.entry_project_name.delete(0, tk.END)
            self.entry_project_name.insert(tk.END, self.selected_project[1])
            # tahun
            self.entry_project_year.delete(0, tk.END)
            self.entry_project_year.insert(tk.END, self.selected_project[2])
            # kapasitas
            self.entry_project_capacity.delete(0, tk.END)
            self.entry_project_capacity.insert(tk.END, self.selected_project[3])
            # customer
            self.entry_project_customer.delete(0, tk.END)
            self.entry_project_customer.insert(tk.END, self.selected_project[4])
            # jumlah
            self.entry_project_units.delete(0, tk.END)
            self.entry_project_units.insert(tk.END, self.selected_project[5])
            # project id
            self.selected_project_id = self.selected_project[0]
            self.update_nama = self.entry_project_name.get()
        except IndexError:
            pass

    def remove_project(self):
        db.remove(self.selected_project[0])
        self.fn_clear_selection()
        self.populate_list()

    def preview_file(self, project_id):
        self.filepath = db.select_project_image(project_id)
        if platform.system() == "Darwin":
            subprocess.call(('open', self.filepath[0][0]))
        elif platform.system() == "Windows":
            os.startfile(self.filepath[0][0])
        else:
            subprocess.call(('xdg-open', self.filepath[0][0]))

    def fn_update_project(self):
        db.update(self.selected_project[0], self.update_nama.get(), self.update_tahun.get(), self.update_kapasitas.get(), self.update_customer.get(), self.update_jumlah.get())
        self.fn_clear_selection()
        self.populate_list()

    def fn_clear_selection(self):
        # nama proyek
        self.entry_project_name.delete(0, tk.END)
        # tahun
        self.entry_project_year.delete(0, tk.END)
        # kapasitas
        self.entry_project_capacity.delete(0, tk.END)
        # customer
        self.entry_project_customer.delete(0, tk.END)
        # jumlah
        self.entry_project_units.delete(0, tk.END)

    def show_popup_about(self):
        # Window -> about us configuration
        self.about_us = tk.Toplevel(self.master)
        self.about_us.title("Tentang Kami")
        self.about_us.geometry("720x312")
        self.about_us.resizable(False, False)
        self.about_us.iconbitmap("./favicon.ico")

        # Images -> PT IMS & Kampus Merdeka
        self.image_ims = ImageTk.PhotoImage(Image.open("./assets/images/logo-ims.png"))
        self.image_ims_label = tk.Label(self.about_us, image=self.image_ims).pack(pady=10)
        self.image_msib = ImageTk.PhotoImage(Image.open("./assets/images/logo-msib.png"))
        self.image_msib_label = tk.Label(self.about_us, image=self.image_msib).pack(pady=10)

        # Keterangan
        self.aboutus_titile = tk.Label(self.about_us, text="Tentang Kami", font=("Verdana bold", 14)).pack()
        self.aboutus_version = tk.Label(self.about_us, text="Versi 0.1.0 (Beta)", font=("Arial bold", 11)).pack()
        self.aboutus_description = tk.Label(self.about_us, text="Program ini dikembangkan untuk mempermudah pengelolaan ", font=("Arial", 11)).pack()
        self.aboutus_description2 = tk.Label(self.about_us, text="data proyek yang ada di SBU AC PT IMS, secara open source di github", font=("Arial", 11)).pack()
        self.aboutus_description2 = tk.Label(self.about_us, text="oleh peserta MSIB Batch 3 2022. Terima kasih!", font=("Arial", 11)).pack()