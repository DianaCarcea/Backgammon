"""
This module contains the interface of the game.

It contains the title screen and the board.
The title screen contains two buttons: one for human vs human and one for human vs AI.
"""

import os
import tkinter as tk
from PIL import Image, ImageTk
from board_interface import TableUi


class Interface:
    """
    Class representing the main interface of the backgammon application.

    Attributes:
    - window (tk.Tk): the main window of the game.
    - table_ui (TableUi): the board of the game.
    - title_screen_canvas (tk.Canvas): the canvas of the title screen.
    - image_button_human (ImageTk.PhotoImage): the image of the human vs human button.
    - image_button_ai (ImageTk.PhotoImage): the image of the human vs AI button.

    Methods:
    - __init__(self, window): Initializes the Interface object.
    - init_title_screen_frame(self): Initializes the title screen frame with background image and text.
    - init_buttons(self): Initializes the buttons for selecting the game mode.
    - on_button_click(self, mode): Handles button clicks and initializes the game board UI.
    """
    def __init__(self, window):
        """
        Initializes the Interface object.

        Parameters:
        - window (tk.Tk): the main window of the game.
        - table_ui (TableUi): the board of the game.
        - title_screen_canvas (tk.Canvas): the canvas of the title screen.
        - image_button_human (ImageTk.PhotoImage): the image of the human vs human button.
        - image_button_ai (ImageTk.PhotoImage): the image of the human vs AI button.
        """
        self.window = window
        self.table_ui = TableUi(self)

        self.title_screen_canvas = None

        self.image_button_human = None
        self.image_button_ai = None

        self.init_title_screen_frame()

    def init_title_screen_frame(self):
        """
        Initializes the title screen frame with background image and text.

        Parameters:
        None

        Returns:
        None
        """

        self.title_screen_canvas = tk.Canvas(self.window, bd=0, highlightthickness=0, relief='ridge')
        self.title_screen_canvas.pack(fill=tk.BOTH, expand=True)

        image = Image.open(os.path.join("images", "fundal.png"))
        photo = ImageTk.PhotoImage(image)

        self.title_screen_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.title_screen_canvas.image = photo

        self.title_screen_canvas.create_text(550, 120,
                                             text="Jocul de table", fill="#cbc9c7",
                                             font=("Comic Sans MS", 30, "bold"), anchor='center')

        self.init_buttons()

    def init_buttons(self):
        """
        Initializes the buttons for selecting the game mode.

        Parameters:
        None

        Returns:
        None
        """

        self.title_screen_canvas.create_text(130, 180,
                                             text="Selectare mod:", fill="#cbc9c7",
                                             font=("Comic Sans MS", 20, "bold"), anchor='nw')

        image_button_human = Image.open(os.path.join("images", "HH.png"))
        image_button_ai = Image.open(os.path.join("images", "HA.png"))

        self.image_button_human = ImageTk.PhotoImage(image_button_human)
        self.image_button_ai = ImageTk.PhotoImage(image_button_ai)

        button1 = tk.Button(self.title_screen_canvas, image=self.image_button_human,
                            command=lambda: self.on_button_click("human"), bd=1)
        self.title_screen_canvas.create_window(120, 250, window=button1, anchor='nw')

        button2 = tk.Button(self.title_screen_canvas, image=self.image_button_ai,
                            command=lambda: self.on_button_click("AI"), bd=1)
        self.title_screen_canvas.create_window(120, 450, window=button2, anchor='nw')

    def on_button_click(self, mode):
        """
        Handles button clicks and initializes the game board UI.

        Parameters:
        - mode (str): the game mode

        Returns:
        None
        """

        self.title_screen_canvas.destroy()
        self.table_ui = TableUi(self)
        self.table_ui.init_board_ui(mode)