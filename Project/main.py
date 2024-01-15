import tkinter as tk
from interface import Interface




if __name__ == '__main__':

    window = tk.Tk()
    window.title("Backgammon")

    window.geometry("1100x700")

    window.resizable(False, False)

    interface = Interface(window)

    window.mainloop()
