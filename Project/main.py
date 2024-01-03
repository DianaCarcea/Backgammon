from Board import Board
from Game import Game
import tkinter as tk
from Interface import Interface
from TableUI import TableUI

# game = Game()
# board = Board()
# board.print_board()
# game.start_game()

if __name__ == '__main__':
    window = tk.Tk()
    window.title("Backgammon")
    interface = Interface(window)
    window.geometry("1100x700")
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    window.mainloop()

    # app = TableUI()
    # app.mainloop()