"""
This file contains the AI class which is used to make the moves for the AI player.
"""

import random
import tkinter as tk
import sys


class NoWarnings:
    def write(self, msg):
        pass


class AI:
    """
    This class is used to make the moves for the AI player.

    Attributes:
    - table_ui (TableUi): The instance of the TableUi class.

     Methods:
    - turn_ai(): Initiates the AI player's turn, including dice rolling, move execution, and UI updates.
    - move_ai(): Implements the logic for AI moves based on the current game state.
    """

    def __init__(self, TableUi):
        """
        Initialize the AI with the given TableUi instance.

        Parameters:
        - TableUi (object): An instance of the TableUi class.
        """

        sys.stderr = NoWarnings()
        self.table_ui = TableUi

    def turn_ai(self):
        """
        Perform the AI's turn, including rolling dice, making moves, and updating the UI.

        Parameters:
        None

        Returns:
        None
        """

        self.table_ui.dices = []
        self.table_ui.game_actions.roll_dice()
        self.move_ai()
        self.table_ui.dices = []
        self.table_ui.roll_dice_button.config(state="normal")
        self.table_ui.current_turn = "white"

    def move_ai(self):
        """
        Implement the logic for AI moves based on the current game state.

        Parameters:
        None

        Returns:
        None
        """

        if self.table_ui.current_turn == "black" and self.table_ui.names[self.table_ui.current_turn] == 'AI' and len(
                self.table_ui.dices) > 0:
            if self.table_ui.info_pieces["black"][0] == 0:
                if self.table_ui.game_actions.have_moves("black"):
                    if len(self.table_ui.all_buttons_pos) > 0:
                        for button in self.table_ui.all_buttons_pos:
                            button.destroy()
                        self.table_ui.all_buttons_pos = []

                    possible_col = []
                    for i in range(0, 24):
                        if len(self.table_ui.board["black"][i][2]) > 0:
                            possible_col.append(i)

                    move = random.randrange(0, len(possible_col))
                    x = possible_col[move]
                    while len(self.table_ui.board["white"][23 - x][2]) > 1 or len(
                            self.table_ui.board["black"][x][2]) == 0 or x < 0 or x > 23:
                        move = random.randrange(0, len(possible_col))
                        x = possible_col[move]

                    if x <= 11:
                        y = 415
                    else:
                        y = 5

                    if not self.table_ui.game_actions.all_pieces_in_home("black"):
                        possible_pos = self.table_ui.game_actions.get_possible_pos("black", x, y)
                        for i in range(0, len(possible_pos)):
                            if possible_pos[i][1] == 5:
                                self.table_ui.all_buttons_pos.append(
                                    tk.Button(self.table_ui.board_frame, image=self.table_ui.image_up_arrow, width=20,
                                              height=20))
                                self.table_ui.all_buttons_pos[i].place(
                                    x=(335 + self.table_ui.board["black"][possible_pos[i][0]][0]), y=350)

                            else:
                                self.table_ui.all_buttons_pos.append(
                                    tk.Button(self.table_ui.board_frame, image=self.table_ui.image_down_arrow, width=20,
                                              height=20))
                                self.table_ui.all_buttons_pos[i].place(
                                    x=(335 + self.table_ui.board["black"][possible_pos[i][0]][0]), y=400)

                        if len(self.table_ui.all_buttons_pos) > 0:
                            self.table_ui.all_buttons_pos[0].config(
                                command=lambda: self.table_ui.game_actions.placing_piece("black", possible_pos[0][0],
                                                                                         x))
                            if len(self.table_ui.all_buttons_pos) == 2:
                                self.table_ui.all_buttons_pos[1].config(
                                    command=lambda: self.table_ui.game_actions.placing_piece("black",
                                                                                             possible_pos[1][0], x))

                            if self.table_ui.names["black"] == "AI":
                                move = random.randrange(0, len(self.table_ui.all_buttons_pos))
                                self.table_ui.all_buttons_pos[move].invoke()

                    else:
                        possible_pos = self.table_ui.game_actions.moves_for_piece_home("black", x, y)
                        for i in range(0, len(possible_pos)):
                            if possible_pos[i][1] == 5:
                                self.table_ui.all_buttons_pos.append(
                                    tk.Button(self.table_ui.board_frame, image=self.table_ui.image_up_arrow, width=20,
                                              height=20))
                                self.table_ui.all_buttons_pos[i].place(
                                    x=(335 + self.table_ui.board["black"][possible_pos[i][0]][0]), y=350)

                            elif possible_pos[i][1] == 415:
                                self.table_ui.all_buttons_pos.append(
                                    tk.Button(self.table_ui.board_frame, image=self.table_ui.image_down_arrow, width=20,
                                              height=20))
                                self.table_ui.all_buttons_pos[i].place(
                                    x=(335 + self.table_ui.board["black"][possible_pos[i][0]][0]), y=400)
                            else:
                                self.table_ui.all_buttons_pos.append(
                                    tk.Button(self.table_ui.board_frame, text="Scoate piesa", font=('Helvetica', 12)))
                                if self.table_ui.current_turn == "white":
                                    self.table_ui.all_buttons_pos[i].place(x=540, y=620)
                                    self.table_ui.game_log_label.config(text="P1 poti sa scoti piesa!")
                                else:
                                    self.table_ui.all_buttons_pos[i].place(x=540, y=620)

                        if len(self.table_ui.all_buttons_pos) > 0:
                            if self.table_ui.all_buttons_pos[0]["text"] == "Scoate piesa":
                                self.table_ui.all_buttons_pos[0].config(
                                    command=lambda: self.table_ui.game_actions.take_out_piece("black", x))
                            else:
                                self.table_ui.all_buttons_pos[0].config(
                                    command=lambda: self.table_ui.game_actions.placing_piece("black",
                                                                                             possible_pos[0][0], x))

                            if len(self.table_ui.all_buttons_pos) == 2:
                                if self.table_ui.all_buttons_pos[1]["text"] == "Scoate piesa":
                                    self.table_ui.all_buttons_pos[1].config(
                                        command=lambda: self.table_ui.game_actions.take_out_piece("black", x))
                                else:
                                    self.table_ui.all_buttons_pos[1].config(
                                        command=lambda: self.table_ui.game_actions.placing_piece("black",
                                                                                                 possible_pos[1][0], x))

                            if self.table_ui.names["black"] == "AI":
                                move = random.randrange(0, len(self.table_ui.all_buttons_pos))
                                self.table_ui.all_buttons_pos[move].invoke()

                else:
                    self.table_ui.current_turn = "white"
                    self.table_ui.dices = []
                    self.table_ui.roll_dice_button.config(state="normal")
                    self.table_ui.game_log_label.config(text="P1 trebuie sa dai cu zarul!")

        if len(self.table_ui.dices) > 0:
            self.move_ai()
        elif not self.table_ui.game_actions.have_moves("black"):
            self.table_ui.dices = []
            self.move_ai()
        else:
            self.table_ui.dices = []
            self.table_ui.roll_dice_button.config(state="normal")
            self.table_ui.current_turn = "white"
