"""
This file contains the class that creates the board interface.

The board interface is the main interface of the game. It contains the board, the pieces, the dices and the buttons.
The board interface is created after the title screen interface.
"""

import tkinter as tk
import os
from PIL import Image, ImageTk

from objects import draw_triangle
from ai_methods import AI
from game_actions import GameActions


def load_dice_images():
    """
    This function loads the dice images from the folder "zaruri" and returns them.

    Parameters:
    None

    Returns:
    list: List of ImageTk.PhotoImage objects for each dice face.
    """

    original_images = [Image.open(os.path.join("zaruri", f"{i}.png")) for i in range(1, 7)]
    dice_images = [ImageTk.PhotoImage(image=image.resize((50, 50))) for image in original_images]

    return dice_images


class TableUi:
    """
    Class representing the user interface for the backgammon game board.

    Attributes:
    - ai (AI): Instance of the AI class for managing AI actions.
    - game_actions (GameActions): Instance of the GameActions class for managing game actions.
    - window (tk.Tk): The main window of the application.
    - board_frame (tk.Frame): Frame for containing the backgammon board UI.
    - canvas (tk.Canvas): Canvas for drawing the backgammon board.
    - interface_title_screen (Interface): Instance of the Interface class for managing the title screen.
    - mode (str): Game mode ("human" or "AI").
    - names (dict): Dictionary containing player names for "white" and "black".
    - info_pieces (dict): Dictionary containing the count of eliminated and free pieces for "black" and "white".
    - button_dice_on (bool): Flag indicating whether the roll dice button is active.
    - background_image (tk.PhotoImage): Image for the background of the winner frame.
    - label_free_p1 (tk.Label): Label displaying the count of free pieces for player 1.
    - label_eliminate_p1 (tk.Label): Label displaying the count of eliminated pieces for player 1.
    - label_free_p2 (tk.Label): Label displaying the count of free pieces for player 2.
    - label_eliminate_p2 (tk.Label): Label displaying the count of eliminated pieces for player 2.
    - game_log_label (tk.Label): Label for displaying game log messages.
    - dice_images (list): List of ImageTk.PhotoImage objects for dice faces.
    - roll_dice_button (tk.Button): Button for rolling the dice.
    - image_piece_black (ImageTk.PhotoImage): Image for the black game piece.
    - image_piece_white (ImageTk.PhotoImage): Image for the white game piece.
    - image_up_arrow (ImageTk.PhotoImage): Image for the up arrow.
    - image_down_arrow (ImageTk.PhotoImage): Image for the down arrow.
    - dice_labels (list): List of labels for displaying dice images.
    - all_buttons_pos (list): List to store positions of all buttons.
    - board (dict): Dictionary representing the backgammon board layout.
    - board_columns_black (list): List of columns representing the black player's side of the board.
    - board_columns_white (list): List of columns representing the white player's side of the board.
    - dices (list): List to store the dice values.
    - current_turn (str): Current player's turn ("white" or "black").

    Methods:
    - __init__(self, interface_title_screen): Initializes the TableUi object.
    - init_board_ui(self, mode): Initializes the board UI based on the selected game mode.
    - create_back_button(self): Creates a button for returning to the title screen.
    - create_status_players(self): Creates player status displays.
    - create_table(self): Creates the visual representation of the backgammon board.
    - create_pieces_buttons(self, player_color): Creates the buttons for player pieces on the board.
    - create_button_roll_dice(self): Creates the button for rolling the dice.
    - display_dices(self): Displays the current dice values.
    - on_back_button_click(self): Handles the back button click event.
    - config_pieces_on_board(self, column_piece, column_from, overlap): Configures the position of pieces on the board.
    - update_board_game(self, player_color, column_from, column_to): Updates the board based on player moves.
    - update_label(self, player_color): Updates the player status labels.
    - who_won(self): Checks if a player has won the game.
    - init_frame_winner(self, winner): Initializes the winner frame.
    - set_background_image(self, winner): Sets the background image based on the winner.
    """

    def __init__(self, interface_title_screen):
        """
        Initializes the TableUi object.

        Parameters:
        - interface_title_screen (Interface): Instance of the Interface class for managing the title screen.
        """

        self.ai = AI(self)
        self.game_actions = GameActions(self)

        self.window = interface_title_screen.window
        self.board_frame = None
        self.canvas = None

        self.interface_title_screen = interface_title_screen

        self.mode = None
        self.names = {}
        self.info_pieces = {"black": [0, 0], "white": [0, 0]}

        self.button_dice_on = True
        self.background_image = None

        self.label_free_p1 = None
        self.label_eliminate_p1 = None

        self.label_free_p2 = None
        self.label_eliminate_p2 = None

        self.game_log_label = None

        self.dice_images = load_dice_images()
        self.roll_dice_button = None

        self.image_piece_black = None
        self.image_piece_white = None

        image_up_arrow = Image.open(os.path.join("images", "up_arrow.png"))
        self.image_up_arrow = ImageTk.PhotoImage(image_up_arrow)

        image_down_arrow = Image.open(os.path.join("images", "down_arrow.png"))
        self.image_down_arrow = ImageTk.PhotoImage(image_down_arrow)

        self.dice_labels = []
        self.all_buttons_pos = []
        self.board = None
        self.board_columns_black = []
        self.board_columns_white = []
        self.dices = []
        self.current_turn = "white"

    def init_board_ui(self, mode):
        """
        Initializes the board UI based on the selected game mode.

        Parameters:
        - mode (str): Game mode ("human" or "AI").

        Returns:
        None
        """

        self.mode = mode
        if self.mode == 'human':
            self.names = {"white": "white", "black": "black"}
        else:
            self.names = {"white": "white", "black": "AI"}

        self.board_frame = tk.Frame(self.window, bd=0, highlightthickness=0, bg="brown", relief='ridge')
        self.board_frame.pack(fill=tk.BOTH, expand=True)
        self.game_log_label = tk.Label(self.board_frame, text="P1 arunca zarurile!", bg="white", fg="black",
                                       font=("Arial", 14))
        self.game_log_label.place(x=510, y=50)

        self.create_back_button()
        self.create_status_players()
        self.create_button_roll_dice()
        self.create_table()

        board_columns_black = self.create_pieces_buttons("black")
        board_columns_white = self.create_pieces_buttons("white")

        self.board = {"white": board_columns_white, "black": board_columns_black}

    def create_back_button(self):
        """
        Creates a button for returning to the title screen.

        Parameters:
        None

        Returns:
        None
        """

        button_back = tk.Button(self.board_frame, text="Înapoi la pagina principală",
                                command=self.on_back_button_click, bg="white",
                                fg="black",
                                font=("Arial", 10), padx=10, pady=5, relief=tk.FLAT, borderwidth=0,
                                highlightthickness=0)

        button_back.pack(side=tk.TOP, anchor=tk.NW, padx=20, pady=20)

    def create_status_players(self):
        """
        Creates player status displays.

        Parameters:
        None

        Returns:
        None
        """

        canvas_p1 = tk.Canvas(self.board_frame, width=80, height=450, bg="#995536")
        canvas_p1.place(x=240, y=140)

        canvas_p1.create_text(45, 40, text="P1", font=("Arial", 20), fill="black")
        canvas_p1.create_oval(18, 70, 68, 120, fill="white", outline="black")

        canvas_p1.create_text(45, 200, text="Piese\nscoase:", font=("Arial", 12), fill="black")
        canvas_p1.create_text(45, 350, text="Piese\neliminate:", font=("Arial", 12), fill="black")

        self.label_free_p1 = tk.Label(canvas_p1, text="0", bg="#995536", fg="white", font=("Arial", 18))
        self.label_free_p1.place(x=35, y=220)

        self.label_eliminate_p1 = tk.Label(canvas_p1, text="0", bg="#995536", fg="white", font=("Arial", 18))
        self.label_eliminate_p1.place(x=35, y=370)

        canvas_p2 = tk.Canvas(self.board_frame, width=80, height=450, bg="#995536")
        canvas_p2.place(x=865, y=140)

        canvas_p2.create_text(45, 40, text="P2", font=("Arial", 20), fill="black")
        canvas_p2.create_oval(18, 70, 68, 120, fill="black", outline="white")

        canvas_p2.create_text(45, 200, text="Piese\nscoase:", font=("Arial", 12), fill="black")
        canvas_p2.create_text(45, 350, text="Piese\neliminate:", font=("Arial", 12), fill="black")

        self.label_free_p2 = tk.Label(canvas_p2, text="0", bg="#995536", fg="black", font=("Arial", 18))
        self.label_free_p2.place(x=35, y=220)

        self.label_eliminate_p2 = tk.Label(canvas_p2, text="0", bg="#995536", fg="black", font=("Arial", 18))
        self.label_eliminate_p2.place(x=35, y=370)

    def create_table(self):
        """
        Creates the visual representation of the backgammon board.

        Parameters:
        None

        Returns:
        None
        """

        self.canvas = tk.Canvas(self.board_frame, bd=5, highlightthickness=1, relief='ridge', bg="#995536",
                                highlightbackground="#482618")
        self.canvas.place(relx=0.3, rely=0.2, relwidth=0.483, relheight=0.65)

        rect_x = 277
        rect_y = 0
        rect_width = 253
        rect_height = 450

        self.canvas.create_rectangle(rect_x, rect_y, rect_width, rect_height, outline="#5c3320", width=2,
                                     fill='#d7aa9b')

        for i in range(6):
            x = 25 + i * 40
            if i % 2:
                draw_triangle(self.canvas, x, 200, 40, 5, "#532a1a", direction="down")
            else:
                draw_triangle(self.canvas, x, 200, 40, 5, "#ddad7d", direction="down")

        space_between_groups = 280

        for i in range(6):
            x = 25 + i * 40 + space_between_groups
            if i % 2:
                draw_triangle(self.canvas, x, 200, 40, 5, "#532a1a", direction="down")
            else:
                draw_triangle(self.canvas, x, 200, 40, 5, "#ddad7d", direction="down")

        for i in range(6):
            x = 25 + i * 40
            if i % 2:
                draw_triangle(self.canvas, x, 250, 40, 5, "#ddad7d", direction="up")
            else:
                draw_triangle(self.canvas, x, 250, 40, 5, "#532a1a", direction="up")

        for i in range(6):
            x = 25 + i * 40 + space_between_groups
            if i % 2:
                draw_triangle(self.canvas, x, 250, 40, 5, "#ddad7d", direction="up")
            else:
                draw_triangle(self.canvas, x, 250, 40, 5, "#532a1a", direction="up")

    def create_pieces_buttons(self, player_color):
        """
        Creates the buttons for player pieces on the board.

        Parameters:
        - player_color (str): Color of the player ("black" or "white").

        Returns:
        - list: List of columns representing the player's side of the board.
        """

        if player_color == "black":
            image_piece = Image.open(os.path.join("images", "black_circle.png"))
            self.image_piece_black = ImageTk.PhotoImage(image_piece)

        else:
            image_piece = Image.open(os.path.join("images", "white_circle.png"))
            self.image_piece_white = ImageTk.PhotoImage(image_piece)

        if player_color == "white":
            y_top = 5
            y_bottom = 415
        else:
            y_top = 415
            y_bottom = 5

        start = 8
        distance = 40

        # top left
        board_column1 = [start, y_top, []]
        board_column2 = [start + distance * 1, y_top, []]
        board_column3 = [start + distance * 2, y_top, []]
        board_column4 = [start + distance * 3, y_top, []]
        board_column5 = [start + distance * 4, y_top, []]
        board_column6 = [start + distance * 5, y_top, []]

        start = 48
        # top right
        board_column7 = [start + distance * 6, y_top, []]
        board_column8 = [start + distance * 7, y_top, []]
        board_column9 = [start + distance * 8, y_top, []]
        board_column10 = [start + distance * 9, y_top, []]
        board_column11 = [start + distance * 10, y_top, []]
        board_column12 = [start + distance * 11, y_top, []]

        start = 8
        # bottom left
        board_column13 = [start, y_bottom, []]
        board_column14 = [start + distance * 1, y_bottom, []]
        board_column15 = [start + distance * 2, y_bottom, []]
        board_column16 = [start + distance * 3, y_bottom, []]
        board_column17 = [start + distance * 4, y_bottom, []]
        board_column18 = [start + distance * 5, y_bottom, []]

        start = 48
        # bottom right
        board_column19 = [start + distance * 6, y_bottom, []]
        board_column20 = [start + distance * 7, y_bottom, []]
        board_column21 = [start + distance * 8, y_bottom, []]
        board_column22 = [start + distance * 9, y_bottom, []]
        board_column23 = [start + distance * 10, y_bottom, []]
        board_column24 = [start + distance * 11, y_bottom, []]

        board_columns = [board_column12, board_column11, board_column10, board_column9, board_column8, board_column7,
                         board_column6, board_column5, board_column4, board_column3, board_column2, board_column1,
                         board_column13, board_column14, board_column15, board_column16, board_column17, board_column18,
                         board_column19, board_column20, board_column21, board_column22, board_column23, board_column24
                         ]

        # pieces for black
        if player_color == "black":
            for i in range(0, 5):
                board_columns[5][2].append(tk.Button(self.canvas, image=self.image_piece_black, width=30, height=30,
                                                     command=lambda: self.game_actions.move_piece("black", 5, i)))

            for i in range(0, 3):
                board_columns[7][2].append(tk.Button(self.canvas, image=self.image_piece_black, width=30, height=30,
                                                     command=lambda: self.game_actions.move_piece("black", 7, i)))

            for i in range(0, 5):
                board_columns[12][2].append(tk.Button(self.canvas, image=self.image_piece_black, width=30, height=30,
                                                      command=lambda: self.game_actions.move_piece("black", 12, i)))

            for i in range(0, 2):
                board_columns[23][2].append(tk.Button(self.canvas, image=self.image_piece_black, width=30, height=30,
                                                      command=lambda: self.game_actions.move_piece("black", 23, i)))


        # pieces for white
        else:
            for i in range(0, 5):
                board_columns[5][2].append(tk.Button(self.canvas, image=self.image_piece_white, width=30, height=30,
                                                     command=lambda: self.game_actions.move_piece("white", 5, i)))

            for i in range(0, 3):
                board_columns[7][2].append(tk.Button(self.canvas, image=self.image_piece_white, width=30, height=30,
                                                     command=lambda: self.game_actions.move_piece("white", 7, i)))

            for i in range(0, 5):
                board_columns[12][2].append(tk.Button(self.canvas, image=self.image_piece_white, width=30, height=30,
                                                      command=lambda: self.game_actions.move_piece("white", 12, i)))

            for i in range(0, 2):
                board_columns[23][2].append(tk.Button(self.canvas, image=self.image_piece_white, width=30, height=30,
                                                      command=lambda: self.game_actions.move_piece("white", 23, i)))

        for i in range(0, len(board_columns)):
            for j in range(0, len(board_columns[i][2])):
                if player_color == "white":
                    if i >= 12:
                        board_columns[i][2][j].place(x=board_columns[i][0], y=board_columns[i][1] - j * 35)
                    else:
                        board_columns[i][2][j].place(x=board_columns[i][0], y=board_columns[i][1] + j * 35)
                else:
                    if i < 12:
                        board_columns[i][2][j].place(x=board_columns[i][0], y=board_columns[i][1] - j * 35)
                    else:
                        board_columns[i][2][j].place(x=board_columns[i][0], y=board_columns[i][1] + j * 35)

        return board_columns

    def create_button_roll_dice(self):
        """
        Creates the "Arunca zaruri" button.

        Parameters:
        None

        Returns:
        None
        """

        self.roll_dice_button = tk.Button(self.board_frame, text="Arunca zaruri",
                                          command=lambda: self.game_actions.roll_dice(), bg="#482618", fg="white",
                                          font=("Arial", 12), padx=10, pady=5, relief=tk.FLAT, borderwidth=0,
                                          highlightthickness=0)
        self.roll_dice_button.pack(side=tk.TOP, anchor=tk.NW, padx=(80, 0), pady=(200, 0))

    def display_dices(self):
        """
        Displays the rolled dice images on the board.

        Parameters:
        None

        Returns:
        None
        """

        for i, dice in enumerate(self.dices[:2]):
            label = tk.Label(self.board_frame, image=self.dice_images[dice - 1])
            self.dice_labels.append(label)
            label.place(x=80 + i * 60, y=350)

        if len(self.dices) > 2:
            for i, dice in enumerate(self.dices[2:]):
                label = tk.Label(self.board_frame, image=self.dice_images[dice - 1])
                self.dice_labels.append(label)
                label.place(x=80 + i * 60, y=410)

    def on_back_button_click(self):
        """
        Handles the "Back" button click event.
        Destroys the current board frame and initializes the title screen frame.

        Parameters:
        None

        Returns:
        None
        """

        self.board_frame.destroy()
        self.interface_title_screen.init_title_screen_frame()

    def config_pieces_on_board(self, column_piece, column_from, overlap):
        """
        Configures the position of pieces on the board after a move.

        Parameters:
        - column_piece (list): Information about the column to configure.
        - column_from (int): Index of the column from which the piece is moved.
        - overlap (int): Flag indicating whether pieces overlap.

        Returns:
        None
        """

        if overlap == 0:
            if self.current_turn == "black":
                adjust_poz = [-1, 1]
            else:
                adjust_poz = [1, -1]

            dist = 160 / len(column_piece[2])

            adjust_poz[0] *= dist
            adjust_poz[1] *= dist

            for col_x in range(0, len(column_piece[2])):
                if column_from <= 11:
                    column_piece[2][col_x].place(x=column_piece[0], y=(column_piece[1] + adjust_poz[0] * col_x))
                elif column_from > 11:
                    column_piece[2][col_x].place(x=column_piece[0], y=(column_piece[1] + adjust_poz[1] * col_x))

        elif overlap == 1:
            if self.current_turn == "black":
                adjust_poz = [-35, 35]
            else:
                adjust_poz = [35, -35]

            for col_x in range(0, len(column_piece[2])):
                if column_from <= 11:
                    column_piece[2][col_x].place(x=column_piece[0], y=(column_piece[1] + adjust_poz[0] * col_x))
                elif column_from > 11:
                    column_piece[2][col_x].place(x=column_piece[0], y=(column_piece[1] + adjust_poz[1] * col_x))

    def update_board_game(self, player_color, column_from, column_to):
        """
        Update the game board based on the move made by the player.

        Parameters:
        - player_color (str): The color of the player making the move.
        - column_from (int): The column index from which the piece is moved.
                          Set to -100 if the move is a piece entering from the bar.
        - column_to (int): The column index to which the piece is moved.

        Returns:
        None
        """

        if player_color == "black":
            other_color = "white"
            adjust_poz = [-35, 35]
        else:
            other_color = "black"
            adjust_poz = [35, -35]

        if column_from != -100:
            self.board[player_color][column_from][2][-1].destroy()
            self.board[player_color][column_from][2].pop()

            if len(self.board[player_color][column_from][2]) > 5:
                self.config_pieces_on_board(self.board[player_color][column_from], column_from, 0)
            else:
                self.config_pieces_on_board(self.board[player_color][column_from], column_from, 1)

            player_position = len(self.board[player_color][column_to][2]) + 1

            if player_color == "white":
                self.board[player_color][column_to][2].append(
                    tk.Button(self.canvas, image=self.image_piece_white, width=30, height=30,
                              command=lambda: self.game_actions.move_piece(player_color, column_to,
                                                                           player_position)))
            else:
                self.board[player_color][column_to][2].append(
                    tk.Button(self.canvas, image=self.image_piece_black, width=30, height=30,
                              command=lambda: self.game_actions.move_piece(player_color, column_to,
                                                                           player_position)))

            if column_to <= 11:
                self.board[player_color][column_to][2][-1].place(x=self.board[player_color][column_to][0],
                                                                 y=(self.board[player_color][column_to][1] + adjust_poz[
                                                                     0] * (
                                                                            len(self.board[player_color][column_to][
                                                                                    2]) - 1)))
                if len(self.board[player_color][column_to][2]) > 5:
                    self.config_pieces_on_board(self.board[player_color][column_to], column_to, 0)
                else:
                    self.config_pieces_on_board(self.board[player_color][column_to], column_to, 1)

            elif column_to > 11:
                self.board[player_color][column_to][2][-1].place(x=self.board[player_color][column_to][0],
                                                                 y=(self.board[player_color][column_to][1] + adjust_poz[
                                                                     1] * (
                                                                            len(self.board[player_color][column_to][
                                                                                    2]) - 1)))
                if len(self.board[player_color][column_to][2]) > 5:
                    self.config_pieces_on_board(self.board[player_color][column_to], column_to, 0)
                else:
                    self.config_pieces_on_board(self.board[player_color][column_to], column_to, 1)

            col_other_player = 23 - column_to

        else:
            player_position = len(self.board[player_color][23 - column_to][2]) + 1
            if player_color == "white":
                self.board[player_color][23 - column_to][2].append(
                    tk.Button(self.canvas, image=self.image_piece_white, width=30, height=30,
                              command=lambda: self.game_actions.move_piece(player_color, 23 - column_to,
                                                                           player_position)))
            else:
                self.board[player_color][23 - column_to][2].append(
                    tk.Button(self.canvas, image=self.image_piece_black, width=30, height=30,
                              command=lambda: self.game_actions.move_piece(player_color, 23 - column_to,
                                                                           player_position)))

            if column_to <= 11:
                self.board[player_color][23 - column_to][2][-1].place(x=self.board[player_color][23 - column_to][0],
                                                                      y=(self.board[player_color][23 - column_to][1] +
                                                                         adjust_poz[0] * (-1) * (len(
                                                                                  self.board[player_color][
                                                                                      23 - column_to][2]) - 1)))
                if len(self.board[player_color][23 - column_to][2]) > 5:
                    self.config_pieces_on_board(self.board[player_color][23 - column_to], 23 - column_to, 0)
                else:
                    self.config_pieces_on_board(self.board[player_color][23 - column_to], 23 - column_to, 1)

            col_other_player = column_to

        if 0 <= col_other_player <= 23 and len(self.board[other_color][col_other_player][2]) == 1:
            self.board[other_color][col_other_player][2][-1].destroy()
            self.board[other_color][col_other_player][2].pop()
            self.info_pieces[other_color][0] += 1
            self.update_label(other_color)

    def update_label(self, player_color):
        """
        Update the labels displaying the number of eliminated and free pieces for a player.

        Parameters:
        - player_color (str): The color of the player whose labels need to be updated.

        Returns:
        None
        """

        if player_color == "white":
            self.label_eliminate_p1.config(text=f"{self.info_pieces[player_color][0]}")
            self.label_free_p1.config(text=f"{self.info_pieces[player_color][1]}")
        else:
            self.label_eliminate_p2.config(text=f"{self.info_pieces[player_color][0]}")
            self.label_free_p2.config(text=f"{self.info_pieces[player_color][1]}")

    def who_won(self):
        """
        Check if a player has won the game. If yes, initialize the winner frame.

        Parameters:
        None

        Returns:
        int: 100 if no winner yet, else None
        """

        if self.info_pieces["white"][1] == 15:
            print("A castigat P1")
            self.init_frame_winner("white")
            return
        if self.names["black"] == "AI" and self.info_pieces["black"][1] == 15:
            print("A castigat AI")
            self.init_frame_winner("ai")
            return
        if self.names["black"] == "black" and self.info_pieces["black"][1] == 15:
            print("A castigat P2")
            self.init_frame_winner("black")
            return
        return 100

    def init_frame_winner(self, winner):
        """
        Initialize the frame that displays the winner of the game.

        Parameters:
        - winner (str): The color or player that won the game.

        Returns:
        None
        """

        self.board_frame.destroy()
        self.board_frame = tk.Frame(self.window, bd=0, highlightthickness=0, bg="brown", relief='ridge')
        self.board_frame.pack(fill=tk.BOTH, expand=True)
        self.set_background_image(winner)
        self.create_back_button()

    def set_background_image(self, winner):
        """
        Set the background image for the winner frame based on the winner.

        Parameters:
        - winner (str): The color or entity that won the game.

        Returns:
        None
        """

        if winner == "white":
            self.background_image = tk.PhotoImage(file="images/fundal_alb_win.png")
        elif winner == "black":
            self.background_image = tk.PhotoImage(file="images/fundal_negru_win.png")
        elif winner == "ai":
            self.background_image = tk.PhotoImage(file="images/fundal_ai_win.png")

        background_label = tk.Label(self.board_frame, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        background_label.image = self.background_image
