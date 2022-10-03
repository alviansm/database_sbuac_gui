import tkinter as tk

def group_messages(parent_widget, row_number, column_number, code):
    MESSAGES = [
        "Database berhasil dipilih",
        "Berhasil menambahkan proyek baru",
        "Berhasil mengupdate data proyek",
        "Pencarian ditemukan",
        "Pencarian tidak ditemukan",
        "Database masih kosong"
    ]
    msg_selection = MESSAGES[code]

    # Label -> messages
    label_message = tk.Label(parent_widget, text=MESSAGES[code], fg="red", font=("Arial", 9))
    label_message.grid(row=row_number, column=column_number)