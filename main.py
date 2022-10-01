import tkinter as tk
from gui.gui import Application

def initiate_app():
    # Initiate GUI
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    initiate_app()
