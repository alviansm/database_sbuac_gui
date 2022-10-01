import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import font
from tkinter import messagebox
from turtle import bgcolor, width
from database.database import Database
from PIL import ImageTk, Image

db = Database("./database/sbu_projects.db")
# db.insert("Kereta Ukur HST", 2022, "40000", "PT KAI", 35, "./images/9q02ejo.png")

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('SBU AC Projects')
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
        ]
        self.U_OPTIONS = [
            "meter",
        ]

        # INPUT VARIABLES
        # Search Group
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
        self.populate_list()

    def create_widgets(self):
        self.group_title()
        self.group_search_by_year()
        self.group_data_update()
        self.group_loading_bar()
        self.group_list_result()
        self.group_messages(0)

    # Menu commands
    def menu_commands(self):
        pass

    def create_menu_items(self):
        # File
        self.file_menu = tk.Menu(self.app_menu, tearoff=False, font=("Arial", 11))
        self.app_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Preferensi", command=self.menu_commands)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Backup database", command=self.menu_commands)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Pilih database", command=self.menu_commands)        
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Keluar", command=self.master.quit)

        # Tambah
        self.tambah_menu = tk.Menu(self.app_menu, tearoff=False, font=("Arial", 11))
        self.app_menu.add_cascade(label="Tambah", menu=self.tambah_menu)
        self.tambah_menu.add_command(label="Proyek Baru", command=self.menu_commands)
        self.tambah_menu.add_command(label="Edit BOM", command=self.menu_commands)
        self.tambah_menu.add_command(label="Edit SPP", command=self.menu_commands)

        # Ekspor
        self.export_menu = tk.Menu(self.app_menu, tearoff=False, font=("Arial", 11))
        self.app_menu.add_cascade(label="Ekspor", menu=self.export_menu)
        self.export_menu.add_command(label="Sebagai Excel", command=self.menu_commands)
        self.export_menu.add_command(label="Sebagai CSV", command=self.menu_commands)
        self.export_menu.add_command(label="Sebaga PDF", command=self.menu_commands)

        # Bantuan
        self.bantuan_menu = tk.Menu(self.app_menu, font=("Arial", 11), tearoff=False)
        self.app_menu.add_cascade(label="Bantuan", menu=self.bantuan_menu)
        self.bantuan_menu.add_command(label="Cara Penggunaan", command=self.menu_commands)
        self.bantuan_menu.add_separator()
        self.bantuan_menu.add_command(label="Tentang Kami", command=self.show_popup_about)

    def group_title(self):
        # Judul
        self.frame_title = tk.Frame(self.master).grid(row=0, column=0)
        self.label_tittle = tk.Label(self.frame_title, text="Database Proyek", font=("Verdana", 14)).grid(row=0, column=0)

    def group_search_by_year(self):
        # Frame pencarian
        self.frame_search_by_year = tk.LabelFrame(self.master, text="Cari", pady=5, padx=5, font=("Verdana Bold", 9))
        self.frame_search_by_year.grid(row=1, column=0, sticky=tk.W, pady=5, padx=17)

        # Pilih tahun
        self.label_year = tk.Label(self.frame_search_by_year, text="Tahun : ")
        self.label_year.grid(row=1, column=0)
        self.search_year_entry = ttk.OptionMenu(self.frame_search_by_year, self.search_year, *self.Y_OPTIONS)
        self.search_year_entry.grid(row=1, column=1)

        # Entry nama
        self.label_name = tk.Label(self.frame_search_by_year, text="Nama Proyek : ")
        self.label_name.grid(row=0, column=0)
        self.entry_name = tk.Entry(self.frame_search_by_year, textvariable=self.search_name, font=("Arial", 11), width=16)
        self.entry_name.grid(row=0, column=1)         

        # Entry project code
        self.label_bom_code = tk.Label(self.frame_search_by_year, text="Kode Proyek : ")
        self.label_bom_code.grid(row=0, column=2, padx=12, sticky=tk.E)
        self.entry_project_code = tk.Entry(self.frame_search_by_year, textvariable=self.search_name, font=("Arial", 11), width=16)
        self.entry_project_code.grid(row=0, column=3)  

        # Tombol cari
        self.button_year_search = ttk.Button(self.frame_search_by_year, text="Cari", width=8, padding=1)
        self.button_year_search.grid(row=0, column=6, padx=1, sticky=tk.E)

        # Checkbox -> Proyek / Component option
        self.search_cb_project = tk.Checkbutton(self.frame_search_by_year, text="Proyek", variable=self.search_cb_project_val).grid(row=0, column=4, sticky=tk.W)
        self.search_cb_project
        self.search_cb_component = tk.Checkbutton(self.frame_search_by_year, text="Komponen", variable=self.search_cb_component_val).grid(row=1, column=4)

    def group_data_update(self):
        # Frame update project
        self.frame_data_update = tk.LabelFrame(self.master, text="Update", pady=5, padx=5, font=("Verdana Bold", 9))
        self.frame_data_update.grid(row=2, column=0, sticky=tk.W, pady=5, padx=17)

        # Entry nama proyek
        self.label_project_name = tk.Label(self.frame_data_update, text="Nama Proyek : ")
        self.label_project_name.grid(row=0, column=0)
        self.entry_project_name = tk.Entry(self.frame_data_update, textvariable=self.update_nama, font=("Arial", 11), width=16)
        self.entry_project_name.grid(row=0, column=1)

        # Entry tahun proyek
        self.label_project_year = tk.Label(self.frame_data_update, text="Tahun : ")
        self.label_project_year.grid(row=1, column=0, sticky=tk.W)
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

        # Tombol -> Bersihkan
        self.button_clear_selection = ttk.Button(self.frame_data_update, text="Bersihkan", command=self.fn_clear_selection)
        self.button_clear_selection.grid(row=1, column=5, sticky=tk.E)

        # Tombol -> Lebih lanjut & Update
        self.button_more = ttk.Button(self.frame_data_update, text="Lebih Lanjut", command=self.show_more_bom)
        self.button_more.grid(row=2, column=1, sticky=tk.W)
        self.button_submit_update = ttk.Button(self.frame_data_update, text="Update", command=self.fn_update_project)
        self.button_submit_update.grid(row=2, column=0)

        # Tombol tampilkan gambar
        self.button_show_image = ttk.Button(self.frame_data_update, text="Gambar", command=self.display_image)
        self.button_show_image.grid(row=2, column=5)

    def group_loading_bar(self):
        self.progress_bar = ttk.Progressbar(self.master, orient=HORIZONTAL, length=520, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=2, pady=5)

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

    # Display messages (ToDos)
    def group_messages(self, code):
        self.MESSAGES = [
            "Database berhasil dipilih",
            "Berhasil menambahkan proyek baru",
            "Berhasil mengupdate data proyek",
            "Pencarian ditemukan",
            "Pencarian tidak ditemukan"
        ]
        self.msg_selection = self.MESSAGES[0]

        # Label -> messages
        self.label_message = tk.Label(self.master, text=self.MESSAGES[1], fg="red", font=("Arial", 9))
        self.label_message.grid(row=5, column=0)

    # Functions 
    def show_popup_about(self):
        # Window -> about us configuration
        self.about_us = tk.Toplevel(self.master)
        self.about_us.title("Tentang Kami")
        self.about_us.geometry("720x312")
        self.about_us.resizable(False, False)
        self.about_us.iconbitmap("./favicon.ico")

        # Images -> PT IMS & Kampus Merdeka
        self.image_ims = ImageTk.PhotoImage(Image.open("./images/logo-ims.png"))
        self.image_ims_label = tk.Label(self.about_us, image=self.image_ims).pack(pady=10)
        self.image_msib = ImageTk.PhotoImage(Image.open("./images/logo-msib.png"))
        self.image_msib_label = tk.Label(self.about_us, image=self.image_msib).pack(pady=10)

        # Keterangan
        self.aboutus_titile = tk.Label(self.about_us, text="Tentang Kami", font=("Verdana bold", 14)).pack()
        self.aboutus_version = tk.Label(self.about_us, text="Versi 0.1.0 (Beta)", font=("Arial bold", 11)).pack()
        self.aboutus_description = tk.Label(self.about_us, text="Program ini dikembangkan untuk mempermudah pengelolaan ", font=("Arial", 11)).pack()
        self.aboutus_description2 = tk.Label(self.about_us, text="data proyek yang ada di SBU AC PT IMS, secara open source di github", font=("Arial", 11)).pack()
        self.aboutus_description2 = tk.Label(self.about_us, text="oleh peserta MSIB Batch 3 2022. Terima kasih!", font=("Arial", 11)).pack()

    def show_more_bom(self):
        # Window -> Konfigurasi edit BOM
        self.window_bom = tk.Toplevel(self.master)
        self.window_bom.title("Edit BOM")
        self.window_bom.geometry("720x520")
        self.window_bom.resizable(False, False)
        self.window_bom.iconbitmap("./favicon.ico")

        # Judul
        self.title_window_bom = tk.Label(self.window_bom, text="Edit BOM", font=("Verdana", 14))
        self.title_window_bom.grid(row=0, column=0)

        # Frame entry
        self.frame_edit_bom = tk.LabelFrame(self.window_bom, text="Update", pady=5, padx=5, font=("Verdana Bold", 9))
        self.frame_edit_bom.grid(row=1, column=0)

        # Entry kode BOM
        self.label_bom_code = tk.Label(self.frame_edit_bom, text="Kode :", font=("Arial", 11))
        self.label_bom_code.grid(row=0, column=0)

        # Tombol -> Update, hapus, tambah, clear
        # List BOM

    def display_image(self):
        pass

    # Populate database to list_result widget
    def populate_list(self):
        self.list_result.delete(0, tk.END)
        for row in db.fetch():
            self.list_result.insert(tk.END, row)

    # Used in new window -> tambah proyek
    def project_add(self):
        if (self.update_nama.get() == "" and self.update_tahun.get() < 1900 and self.update_kapasitas.get() < 0 and self.update_customer.get() == "" and self.update_jumlah.get() <= 0):
            messagebox.showerror('Semua Entry Harus Diisi', 'Tolong isi semua entry yang tersedia')
            return
        db.insert(self.update_nama.get(), self.update_tahun.get(), self.update_kapasitas.get(), self.update_customer.get(), self.update_jumlah.get(), "")
        self.list_result.delete(0, tk.END)
        self.list_result.insert(END, (self.update_nama.get(), self.update_tahun.get(), self.update_kapasitas.get(), self.update_customer.get(), self.update_jumlah.get()))
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
        except IndexError:
            pass

    def remove_project(self):
        db.remove(self.selected_project[0])
        populate_list()

    def fn_update_project(self):
        pass

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
