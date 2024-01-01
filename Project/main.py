import tkinter as tk
from Interface import Interface

if __name__ == '__main__':
    window = tk.Tk()
    interface = Interface(window)
    window.geometry("1100x700")
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    window.mainloop()

