import tkinter as tk
from tkinter import ttk

def fn_window_authentication(parent):
    window_authentication = tk.Toplevel(parent)
    window_authentication.title("Masuk Sebagai Admin")
    window_authentication.geometry("296x128")
    window_authentication.resizable(False, False)
    window_authentication.iconbitmap("./favicon.ico")

    group_input = tk.LabelFrame(window_authentication, text="Silahkan input data", font=("Verdana bold", 9))
    group_input.grid(row=0, column=0, padx=12, pady=3)

    # Username
    label_username = tk.Label(group_input, text="Username :", font=("Arial", 11))
    label_username.grid(row=0, column=0, pady=3, padx=6, sticky=tk.E)
    entry_username = tk.Entry(group_input, font=("Arial", 11))
    entry_username.grid(row=0, column=1, padx=6, sticky=tk.W)

    # Password
    label_password = tk.Label(group_input, text="Password :", font=("Arial", 11))
    label_password.grid(row=1, column=0, pady=3, padx=6, sticky=tk.E)
    entry_password = tk.Entry(group_input, font=("Arial", 11), show="*")
    entry_password.grid(row=1, column=1, padx=6, sticky=tk.W)

    group_button = tk.Frame(window_authentication)
    group_button.grid(row=1, column=0, pady=6)

    button_login = ttk.Button(group_button, text="Login", width=14)
    button_login.grid(row=0, column=1, padx=6, sticky=tk.E)
    button_register = ttk.Button(group_button, text="Buat Akun", width=14)
    button_register.grid(row=0, column=0, padx=6, sticky=tk.W)