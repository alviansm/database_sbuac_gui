import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import font
from turtle import width
from database.database import Database
from PIL import ImageTk, Image

db = Database("./database/sbu_projects.db")

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
            "2023",
        ]

        # Input variables
        self.search_year = tk.StringVar()
        self.search_year.set(self.Y_OPTIONS[0]) # "2022"
        self.search_name = tk.StringVar()
        self.search_bomcode = tk.StringVar()
        self.search_cb_project_val = tk.IntVar(value=1)
        self.search_cb_component_val = tk.IntVar(value=1)

        self.result_name = tk.StringVar()

        # Create menu bar
        self.app_menu = tk.Menu(self.master, font=("Arial", 11))
        master.config(menu=self.app_menu)
        self.create_menu_items()
        
        # Initiate widgets
        self.create_widgets()

    def create_widgets(self):
        self.group_title()
        self.group_search_by_year()
        self.group_data_update()
        self.group_loading_bar()
        self.group_list_result()

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
        self.app_menu.add_cascade(label="Ekspor Hasil", menu=self.export_menu)
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
        self.frame_title = tk.Frame(self.master).grid(row=0, column=0)
        self.label_titile = tk.Label(self.frame_title, text="Database Proyek", font=("Verdana", 14)).grid(row=0, column=0)

    def group_search_by_year(self):
        self.frame_search_by_year = tk.LabelFrame(self.master, text="Cari", pady=5, padx=5, font=("Verdana Bold", 9))
        self.frame_search_by_year.grid(row=1, column=0, sticky=tk.W, pady=5, padx=17)

        self.label_year = tk.Label(self.frame_search_by_year, text="Tahun : ")
        self.label_year.grid(row=0, column=0)
        self.search_year_entry = ttk.OptionMenu(self.frame_search_by_year, self.search_year, *self.Y_OPTIONS)
        self.search_year_entry.grid(row=0, column=1)

        self.label_name = tk.Label(self.frame_search_by_year, text="Nama : ")
        self.label_name.grid(row=0, column=2)
        self.entry_name = tk.Entry(self.frame_search_by_year, textvariable=self.search_name, font=("Arial", 11), width=16)
        self.entry_name.grid(row=0, column=3)

        self.label_bomcode = tk.Label(self.frame_search_by_year, text="Kode : ")
        self.label_bomcode.grid(row=0, column=4, padx= 12, sticky=tk.E)
        self.entry_bomcode = tk.Entry(self.frame_search_by_year, textvariable=self.search_bomcode, font=("Arial", 11), width=16)
        self.entry_bomcode.grid(row=0, column=5)          

        self.button_year_search = ttk.Button(self.frame_search_by_year, text="Cari", width=8, padding=1)
        self.button_year_search.grid(row=0, column=6, pady=5, padx=12)

        # Checkbox -> Proyek / Component option
        self.search_cb_project = tk.Checkbutton(self.frame_search_by_year, text="Proyek", variable=self.search_cb_project_val).grid(row=1, column=0)
        self.search_cb_project
        self.search_cb_component = tk.Checkbutton(self.frame_search_by_year, text="Komponen", variable=self.search_cb_component_val).grid(row=1, column=1)

    def group_data_update(self):
        pass

    def group_loading_bar(self):
        self.progress_bar = ttk.Progressbar(self.master, orient=HORIZONTAL, length=520, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=2, pady=5)

    def group_list_result(self):
        self.list_result = tk.Listbox(self.master, height=8, width=82, border=1)
        self.list_result.grid(row=4, column=0, pady=5)
        
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=4, column=0, padx=13, sticky=tk.E)
        self.list_result.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.list_result.yview)

    def show_popup_about(self):
        self.about_us = tk.Toplevel(self.master)
        self.about_us.title("Tentang Kami")
        self.about_us.geometry("720x312")
        self.about_us.resizable(False, False)
        self.about_us.iconbitmap("./favicon.ico")

        self.image_ims = ImageTk.PhotoImage(Image.open("./images/logo-ims.png"))
        self.image_ims_label = tk.Label(self.about_us, image=self.image_ims).pack(pady=10)
        self.image_msib = ImageTk.PhotoImage(Image.open("./images/logo-msib.png"))
        self.image_msib_label = tk.Label(self.about_us, image=self.image_msib).pack(pady=10)

        self.aboutus_titile = tk.Label(self.about_us, text="Tentang Kami", font=("Verdana bold", 14)).pack()
        self.aboutus_version = tk.Label(self.about_us, text="Versi 0.9 (Beta)", font=("Arial", 11)).pack()
        self.aboutus_description = tk.Label(self.about_us, text="Program ini dikembangkan untuk mempermudah pengelolaan ", font=("Arial", 11)).pack()
        self.aboutus_description2 = tk.Label(self.about_us, text="data proyek yang ada di SBU AC PT IMS, secara open source di github", font=("Arial", 11)).pack()
        self.aboutus_description2 = tk.Label(self.about_us, text="oleh peserta MSIB Batch 3 2022. Terima kasih!", font=("Arial", 11)).pack()

