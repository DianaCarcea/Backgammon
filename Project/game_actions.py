"""
The file game_actions.py contains the class GameActions, which is used to handle the game logic.
"""
import time
import random
import tkinter as tk


class GameActions:
    """
    This class manages game actions and logic.

    Attributes:
    - table_ui (TableUi): The instance of the TableUi class.

    Methods:
    - roll_dice(): Simulate rolling the dice.
    - have_moves(player_color): Check if the player has possible moves.
    - move_piece(player_color, x, y): Move a piece on the board.
    - get_possible_pos(player_color, x, y): Get possible positions for a piece.
    - show_options(player_color, x, y): Show options for moving a piece.
    - moves_for_piece_home(player_color, x, y): Get possible moves for a piece inside the home.
    - show_options_removed_piece(player_color): Show options for removed pieces.
    - placing_piece(player_color, col, occupied_col): Place a piece on the board.
    - all_pieces_in_home(player_color): Check if all pieces are in the home.
    - take_out_piece(player_color, column): Take out a piece from the board.
    """

    def __init__(self, TableUi):
        """
        Initialize GameActions with the given TableUi instance.

        Parameters:
        - TableUi (object): An instance of the TableUi class.
        """
        self.table_ui = TableUi

    def roll_dice(self):
        """
        Simulate rolling the dice and handle the game state accordingly.

        This method simulates rolling two dice, updates the dice values, and manages the game state based on the outcomes.
        If the two dice show the same value, the player gets additional moves. The method updates the game log label and
        disables the roll dice button appropriately.

        Parameters:
        None

        Returns:
        None
        """
        time.sleep(0.7)

        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)

        if dice1 != dice2:
            self.table_ui.dices.append(dice1)
            self.table_ui.dices.append(dice2)
        else:
            self.table_ui.dices.append(dice1)
            self.table_ui.dices.append(dice1)
            self.table_ui.dices.append(dice1)
            self.table_ui.dices.append(dice1)

        if self.table_ui.dice_labels is not None:
            for label in self.table_ui.dice_labels:
                label.destroy()

        self.table_ui.display_dices()

        self.table_ui.roll_dice_button.config(state="disabled")
        self.table_ui.button_dice_on = False

        if self.table_ui.info_pieces[self.table_ui.current_turn][0] > 0:
            self.show_options_removed_piece(self.table_ui.current_turn)
            if len(self.table_ui.dices) == 0:
                if self.table_ui.current_turn == "white":
                    self.table_ui.current_turn = "black"
                    if self.table_ui.current_turn == "black" and self.table_ui.names["black"] == "AI":
                        print(f"nu a putut face zarurile:{self.table_ui.dices}")
                        self.table_ui.ai.turn_ai()
                else:
                    self.table_ui.current_turn = "white"

        if not self.have_moves(self.table_ui.current_turn):
            self.table_ui.roll_dice_button.config(state="normal")
            self.table_ui.button_dice_on = True
            self.table_ui.dices = []
            if self.table_ui.current_turn == "white":
                self.table_ui.current_turn = "black"
                self.table_ui.game_log_label.config(text="P2 trebuie sa dai cu zarul!")
            else:
                self.table_ui.current_turn = "white"

                self.table_ui.game_log_label.config(text="P1 trebuie sa dai cu zarul!")

        if self.table_ui.current_turn == "white" and self.table_ui.button_dice_on == False:
            self.table_ui.game_log_label.config(text="P1 alege o mutare!")

        if self.table_ui.current_turn == "black" and self.table_ui.names[
            "black"] != "AI" and self.table_ui.button_dice_on == False:
            self.table_ui.game_log_label.config(text="P2 alege o mutare!")

    def have_moves(self, player_color):
        """
        Check if the given player has available moves based on the current dice values and game state.

        Parameters:
        - player_color (str): The color of the player ("white" or "black").

        Returns:
        - bool: True if the player has available moves, False otherwise.
        """

        if player_color == "black":
            other_color = "white"
        else:
            other_color = "black"

        count_moves = 0

        if not self.all_pieces_in_home(player_color):
            if len(self.table_ui.dices) > 0:
                for dice in self.table_ui.dices:
                    for x_col in range(0, 24):
                        if len(self.table_ui.board[player_color][x_col][2]) > 0:
                            col_to = x_col - dice
                            if 0 <= col_to <= 23 and len(self.table_ui.board[other_color][23 - col_to][2]) < 2:
                                count_moves += 1
                                break
                    if count_moves != 0:
                        break
        else:
            if len(self.table_ui.dices) > 0:
                for dice in self.table_ui.dices:
                    if len(self.table_ui.board[player_color][dice - 1][2]) > 0:
                        count_moves += 1
                    else:
                        count_fix_moves = 0
                        for i in range(dice - 1, 6):
                            if len(self.table_ui.board[player_color][i][2]) == 0:
                                count_fix_moves += 1
                        if count_fix_moves == 7 - dice:
                            count_moves += 1
                    for x_col in range(0, 24):
                        if len(self.table_ui.board[player_color][x_col][2]) > 0:
                            column = x_col - dice
                            if 0 <= column < 24 and len(self.table_ui.board[other_color][23 - column][2]) < 2:
                                count_moves += 1
                                break

        if count_moves == 0:
            return False
        else:
            return True

    def move_piece(self, player_color, x, y):
        """
        Process the player's move based on the current game state.

        Parameters:
        - player_color (str): The color of the player ("white" or "black").
        - x (int): X-coordinate of the selected piece.
        - y (int): Y-coordinate of the selected piece.

        Returns:
        None
        """
        if self.table_ui.current_turn == "white" and len(self.table_ui.dices) > 0:
            if player_color == "black":
                self.table_ui.game_log_label.config(text="P2 nu este randul tau!")
            else:
                if self.table_ui.info_pieces[player_color][0] == 0:
                    self.table_ui.game_log_label.config(text="P1 alege mutarea pentru piesa aleasa!")
                    self.show_options(player_color, x, y)
                else:
                    self.table_ui.game_log_label.config(text="P1 alege mutarea pentru piesa eliminata!")

        elif self.table_ui.current_turn == "black" and len(self.table_ui.dices) > 0:
            if player_color == "white":
                self.table_ui.game_log_label.config(text="P1 nu este randul tau!")
            else:
                if self.table_ui.info_pieces[player_color][0] == 0:
                    self.table_ui.game_log_label.config(text="P2 alege mutarea pentru piesa aleasa!")
                    self.show_options(player_color, x, y)
                else:
                    self.table_ui.game_log_label.config(text="P2 alege mutarea pentru piesa eliminata!")

        else:
            if self.table_ui.current_turn == "white":
                self.table_ui.game_log_label.config(text="P1 trebuie sa dai cu zarul!")
            else:
                self.table_ui.game_log_label.config(text="P2 trebuie sa dai cu zarul!")

    def get_possible_pos(self, player_color, x, y):
        """
        Get the possible positions for a player's piece based on the current game state.

        Parameters:
        - player_color (str): The color of the player ("white" or "black").
        - x (int): X-coordinate of the selected piece.
        - y (int): Y-coordinate of the selected piece.

        Returns:
        - list: A list of possible positions where the piece can move.
        """

        possible_pos = []
        if player_color == "white":
            if len(self.table_ui.dices) == 2:
                for col_x in range(0, len(self.table_ui.dices)):
                    new_x_col = x - self.table_ui.dices[col_x]

                    if new_x_col < 12:
                        new_y = 5
                    else:
                        new_y = 415

                    new_col = 23 - new_x_col

                    if 0 <= new_col <= 23:
                        if len(self.table_ui.board["black"][new_col][2]) < 2 and new_x_col >= 0:
                            possible_pos.append([new_x_col, new_y])

            else:
                new_x_col = x - self.table_ui.dices[0]
                if new_x_col < 12:
                    new_y = 5
                else:
                    new_y = 415

                new_col = 23 - new_x_col
                if 0 <= new_col <= 23:
                    if len(self.table_ui.board["black"][new_col][2]) < 2 and new_x_col >= 0:
                        possible_pos.append([new_x_col, new_y])

        else:
            if len(self.table_ui.dices) == 2:
                for col_x in range(0, len(self.table_ui.dices)):
                    new_x_col = x - self.table_ui.dices[col_x]
                    if new_x_col < 12:
                        new_y = 415
                    else:
                        new_y = 5

                    new_col = 23 - new_x_col
                    if 0 <= new_col <= 23:
                        if len(self.table_ui.board["white"][new_col][2]) < 2 and new_x_col >= 0:
                            possible_pos.append([new_x_col, new_y])

            else:
                new_x_col = x - self.table_ui.dices[0]
                if new_x_col < 12:
                    new_y = 415
                else:
                    new_y = 5

                new_col = 23 - new_x_col
                if 0 <= new_col <= 23:
                    if len(self.table_ui.board["white"][new_col][2]) < 2 and new_x_col >= 0:
                        possible_pos.append([new_x_col, new_y])

        if len(possible_pos) == 0 and y > 0 and self.table_ui.names[player_color] != "AI":
            if self.table_ui.current_turn == "white":
                self.table_ui.game_log_label.config(text="P1 nu ai unde muta piesa!")
            else:
                self.table_ui.game_log_label.config(text="P2 nu ai unde muta piesa!")

        return possible_pos

    def show_options(self, player_color, x, y):
        """
        The method first clears any existing buttons, checks if the player has valid moves, and
        then displays directional buttons or take-out buttons based on the game state. The displayed
        buttons are associated with specific commands for placing or taking out pieces.

        Parameters:
        - player_color (str): The color of the player ("white" or "black").
        - x (int): X-coordinate of the selected piece on the board.
        - y (int): Y-coordinate of the selected piece on the board.

        Returns:
        None
        """
        if len(self.table_ui.all_buttons_pos) > 0:
            for button in self.table_ui.all_buttons_pos:
                button.destroy()
            self.table_ui.all_buttons_pos = []

        if self.have_moves(player_color):
            if len(self.table_ui.dices) > 0:

                if not self.all_pieces_in_home(player_color):

                    possible_pos = self.get_possible_pos(player_color, x, y)
                    print(possible_pos)

                    for i in range(0, len(possible_pos)):
                        if possible_pos[i][1] == 5:
                            self.table_ui.all_buttons_pos.append(
                                tk.Button(self.table_ui.board_frame, image=self.table_ui.image_up_arrow, width=20,
                                          height=20))
                            self.table_ui.all_buttons_pos[i].place(
                                x=(335 + self.table_ui.board[player_color][possible_pos[i][0]][0]), y=340)

                        else:
                            self.table_ui.all_buttons_pos.append(
                                tk.Button(self.table_ui.board_frame, image=self.table_ui.image_down_arrow, width=20,
                                          height=20))
                            self.table_ui.all_buttons_pos[i].place(
                                x=(335 + self.table_ui.board[player_color][possible_pos[i][0]][0]), y=380)

                    if len(self.table_ui.all_buttons_pos) > 0:
                        self.table_ui.all_buttons_pos[0].config(
                            command=lambda: self.placing_piece(player_color, possible_pos[0][0], x))
                        if len(self.table_ui.all_buttons_pos) == 2:
                            self.table_ui.all_buttons_pos[1].config(
                                command=lambda: self.placing_piece(player_color, possible_pos[1][0], x))

                # cu toate piesele in casa
                else:

                    possible_pos = self.moves_for_piece_home(player_color, x, y)
                    if self.have_moves(player_color):
                        if len(self.table_ui.dices) > 0:
                            for i in range(0, len(possible_pos)):
                                if possible_pos[i][1] == 5:
                                    self.table_ui.all_buttons_pos.append(
                                        tk.Button(self.table_ui.board_frame, image=self.table_ui.image_up_arrow,
                                                  width=20, height=20))
                                    self.table_ui.all_buttons_pos[i].place(
                                        x=(335 + self.table_ui.board[player_color][possible_pos[i][0]][0]),
                                        y=340)
                                elif possible_pos[i][1] == 415:
                                    self.table_ui.all_buttons_pos.append(
                                        tk.Button(self.table_ui.board_frame, image=self.table_ui.image_down_arrow,
                                                  width=20, height=20))
                                    self.table_ui.all_buttons_pos[i].place(
                                        x=(335 + self.table_ui.board[player_color][possible_pos[i][0]][0]),
                                        y=380)
                                else:
                                    self.table_ui.all_buttons_pos.append(
                                        tk.Button(self.table_ui.board_frame, text="Scoate piesa",
                                                  font=('Helvetica', 12)))
                                    if self.table_ui.current_turn == "white":
                                        self.table_ui.all_buttons_pos[i].place(x=540, y=620)
                                        self.table_ui.game_log_label.config(text="P1 poti sa scoti piesa!")
                                    else:
                                        self.table_ui.all_buttons_pos[i].place(x=540, y=620)
                                        if self.table_ui.names["black"] != "AI":
                                            self.table_ui.game_log_label.config(text="P2 poti sa scoti piesa!")

                            if len(self.table_ui.all_buttons_pos) > 0:
                                if self.table_ui.all_buttons_pos[0]["text"] == "Scoate piesa":
                                    self.table_ui.all_buttons_pos[0].config(
                                        command=lambda: self.take_out_piece(player_color, x))
                                else:
                                    self.table_ui.all_buttons_pos[0].config(
                                        command=lambda: self.placing_piece(player_color, possible_pos[0][0], x))

                                if len(self.table_ui.all_buttons_pos) == 2:
                                    if self.table_ui.all_buttons_pos[1]["text"] == "Scoate piesa":
                                        self.table_ui.all_buttons_pos[1].config(
                                            command=lambda: self.take_out_piece(player_color, x))
                                    else:
                                        self.table_ui.all_buttons_pos[1].config(
                                            command=lambda: self.placing_piece(player_color, possible_pos[1][0],
                                                                               x))
            else:
                self.table_ui.dices = []
                if self.table_ui.current_turn == "white":
                    self.table_ui.current_turn = "black"
                    if self.table_ui.current_turn == "black" and self.table_ui.names["black"] == "AI":
                        self.table_ui.ai.turn_ai()
                else:
                    self.table_ui.current_turn = "white"

                self.table_ui.roll_dice_button.config(state="normal")

                if self.table_ui.current_turn == "white":
                    self.table_ui.game_log_label.config(text="P1 trebuie sa dai cu zarul!")
                else:
                    self.table_ui.game_log_label.config(text="P2 trebuie sa dai cu zarul!")

        else:
            self.table_ui.dices = []
            if self.table_ui.current_turn == "white":
                self.table_ui.current_turn = "black"
                if self.table_ui.current_turn == "black" and self.table_ui.names["black"] == "AI":
                    self.table_ui.ai.turn_ai()
            else:
                self.table_ui.current_turn = "white"

            self.table_ui.roll_dice_button.config(state="normal")
            if self.table_ui.current_turn == "white":
                self.table_ui.game_log_label.config(text="P1 trebuie sa dai cu zarul!")
            else:
                self.table_ui.game_log_label.config(text="P2 trebuie sa dai cu zarul!")

    def moves_for_piece_home(self, player_color, x, y):
        """
        Get possible move options for a player's piece that is currently in the home area.
        The method calculates potential move positions based on the player's dice rolls and
        the current state of the board. If the piece can be moved onto the board, the valid
        position is appended to the `possible_pos` list. If the piece can be taken out (borne off),
        a special code of [-100, 0] is appended to indicate that it can be removed from the home area.

        Parameters:
        - player_color (str): The color of the player ("white" or "black").
        - x (int): X-coordinate of the selected piece on the board.
        - y (int): Y-coordinate of the selected piece on the board.

        Returns:
        - list: A list of potential move positions. Each position is represented as [new_x_col, new_y].
        """
        possible_pos = []
        if player_color == "white":
            if len(self.table_ui.dices) == 2:
                for x_col in range(0, len(self.table_ui.dices)):
                    new_x_col = x - self.table_ui.dices[x_col]

                    if new_x_col < 12:
                        new_y = 5
                    else:
                        new_y = 415

                    new_col = 23 - new_x_col

                    if 0 <= new_col <= 23:
                        if len(self.table_ui.board["black"][new_col][2]) < 2 and new_x_col >= 0:
                            possible_pos.append([new_x_col, new_y])

                    elif new_x_col < 0:
                        is_last_col = True

                        if new_x_col == -1:
                            possible_pos.append([-100, 0])

                        else:
                            for i in range(0, 6):
                                if len(self.table_ui.board[player_color][i][2]) > 0:
                                    dist = i - self.table_ui.dices[x_col]
                                    if 0 > dist > new_x_col:
                                        is_last_col = False
                                    elif dist >= 0:
                                        is_last_col = False

                            if is_last_col == True:
                                possible_pos.append([-100, 0])

            else:
                new_x_col = x - self.table_ui.dices[0]
                if new_x_col < 12:
                    new_y = 5
                else:
                    new_y = 415

                new_col = 23 - new_x_col

                if 0 <= new_col <= 23:
                    if len(self.table_ui.board["black"][new_col][2]) < 2 and new_x_col >= 0:
                        possible_pos.append([new_x_col, new_y])

                elif new_x_col < 0:
                    is_last_col = True
                    if new_x_col == -1:
                        possible_pos.append([-100, 0])
                    else:
                        for i in range(0, 6):
                            if len(self.table_ui.board[player_color][i][2]) > 0:
                                dist = i - self.table_ui.dices[0]
                                if 0 > dist > new_x_col:
                                    is_last_col = False
                                elif dist >= 0:
                                    is_last_col = False

                        if is_last_col == True:
                            possible_pos.append([-100, 0])

        else:
            if len(self.table_ui.dices) == 2:
                for x_col in range(0, len(self.table_ui.dices)):
                    new_x_col = x - self.table_ui.dices[x_col]
                    if new_x_col < 12:
                        new_y = 415
                    else:
                        new_y = 5

                    new_col = 23 - new_x_col

                    if 0 <= new_col <= 23:
                        if len(self.table_ui.board["white"][new_col][2]) < 2 and new_x_col >= 0:
                            possible_pos.append([new_x_col, new_y])

                    elif new_x_col < 0:
                        is_last_col = True
                        if new_x_col == -1:
                            possible_pos.append([-100, 0])
                        else:
                            for i in range(0, 6):
                                if len(self.table_ui.board[player_color][i][2]) > 0:
                                    dist = i - self.table_ui.dices[x_col]
                                    if 0 > dist > new_x_col:
                                        is_last_col = False
                                    elif dist >= 0:
                                        is_last_col = False

                            if is_last_col == True:
                                possible_pos.append([-100, 0])

            else:
                new_x_col = x - self.table_ui.dices[0]
                if new_x_col < 12:
                    new_y = 415
                else:
                    new_y = 5

                new_col = 23 - new_x_col
                if 0 <= new_col <= 23:
                    if len(self.table_ui.board["white"][new_col][2]) < 2 and new_x_col >= 0:
                        possible_pos.append([new_x_col, new_y])

                elif new_x_col < 0:
                    is_last_col = True
                    if new_x_col == -1:
                        possible_pos.append([-100, 0])
                    else:
                        for i in range(0, 6):
                            if len(self.table_ui.board[player_color][i][2]) > 0:
                                dist = i - self.table_ui.dices[0]
                                if 0 > dist > new_x_col:
                                    is_last_col = False
                                elif dist >= 0:
                                    is_last_col = False

                        if is_last_col == True:
                            possible_pos.append([-100, 0])

        if len(possible_pos) == 0 and y > 0 and self.table_ui.names[player_color] != "AI":
            if self.table_ui.current_turn == "white":
                self.table_ui.game_log_label.config(text="P1 nu ai unde muta piesa!")
            else:
                self.table_ui.game_log_label.config(text="P2 nu ai unde muta piesa!")

        return possible_pos

    def show_options_removed_piece(self, player_color):
        """
        Display possible move options for a player's piece that has been removed due to the opponent.
        The method checks the available dice rolls and the opponent's board to find potential positions
        where the removed piece can be placed back onto the board. It then displays arrow buttons indicating
        the possible move directions.
        If the player is controlled by the AI, it randomly selects one of the available move options.

        Parameters:
        - player_color (str): The color of the player ("white" or "black").

        Returns:
        None
        """
        if player_color == "black":
            other_player = "white"
            new_y = 5
        else:
            other_player = "black"
            new_y = 415

        possible_position = []

        if len(self.table_ui.dices) == 2:
            for dice in self.table_ui.dices:
                if len(self.table_ui.board[other_player][dice - 1][2]) < 2:
                    possible_position.append([dice - 1, new_y])
        else:
            if len(self.table_ui.board[other_player][self.table_ui.dices[0] - 1][2]) < 2:
                possible_position.append([self.table_ui.dices[0] - 1, new_y])

        if len(possible_position) == 0:
            self.table_ui.roll_dice_button.config(state="normal")
            self.table_ui.dices = []
            if self.table_ui.current_turn == "white":
                self.table_ui.current_turn = "black"
                if self.table_ui.names["black"] == "AI":
                    self.table_ui.ai.turn_ai()
                else:
                    self.table_ui.game_log_label.config(text="P2 trebuie sa dai cu zarul!")
            else:
                self.table_ui.current_turn = "white"
                self.table_ui.game_log_label.config(text="P1 trebuie sa dai cu zarul!")

        else:
            for i in range(0, len(possible_position)):
                if possible_position[i][1] == 5:
                    self.table_ui.all_buttons_pos.append(
                        tk.Button(self.table_ui.board_frame, image=self.table_ui.image_up_arrow, width=20, height=20))
                    self.table_ui.all_buttons_pos[i].place(
                        x=(335 + self.table_ui.board[player_color][possible_position[i][0]][0]), y=350)
                else:
                    self.table_ui.all_buttons_pos.append(
                        tk.Button(self.table_ui.board_frame, image=self.table_ui.image_down_arrow, width=20, height=20))
                    self.table_ui.all_buttons_pos[i].place(
                        x=(335 + self.table_ui.board[player_color][possible_position[i][0]][0]), y=350)

            if len(self.table_ui.all_buttons_pos) > 0:
                self.table_ui.all_buttons_pos[0].config(
                    command=lambda: self.placing_piece(player_color, possible_position[0][0], -100))
                if len(self.table_ui.all_buttons_pos) == 2:
                    self.table_ui.all_buttons_pos[1].config(
                        command=lambda: self.placing_piece(player_color, possible_position[1][0], -100))

            if self.table_ui.names[player_color] == "AI":
                ai_move = random.randrange(0, len(self.table_ui.all_buttons_pos))
                self.table_ui.all_buttons_pos[ai_move].invoke()

    def placing_piece(self, player_color, col, occupied_col):
        """
        Handle the placement of a player's piece on the game board.
        The method updates the game board to reflect the placement of the player's piece. If the piece is moved from a valid
        position (not borne off), it adjusts the dice values and the player's piece count. If there are remaining dice and
        pieces, it displays options for placing removed pieces.

        If all dice have been used, it updates the turn, enables the roll dice button, and updates the game log label.

        Parameters:
        - player_color (str): The color of the player ("white" or "black").
        - col (int): The column on the board where the piece will be placed.
        - occupied_col (int): The column where the piece is currently located or a special code (-100) if it's off the board.

        Returns:
        None
        """

        for button in self.table_ui.all_buttons_pos:
            button.destroy()
        self.table_ui.all_buttons_pos = []

        self.table_ui.update_board_game(player_color, occupied_col, col)

        if occupied_col != -100:
            dice = occupied_col - col
            self.table_ui.dices.remove(dice)
        else:
            dice = col + 1
            self.table_ui.dices.remove(dice)
            self.table_ui.info_pieces[player_color][0] -= 1
            self.table_ui.update_label(self.table_ui.current_turn)
            if self.table_ui.info_pieces[player_color][0] > 0 and len(self.table_ui.dices) > 0:
                self.table_ui.game_actions.show_options_removed_piece(player_color)

        if len(self.table_ui.dices) == 0:
            if self.table_ui.current_turn == "white":
                self.table_ui.current_turn = "black"
                if self.table_ui.current_turn == "black" and self.table_ui.names["black"] == "AI":
                    self.table_ui.ai.turn_ai()
            else:
                self.table_ui.current_turn = "white"

            self.table_ui.roll_dice_button.config(state="normal")
            if self.table_ui.current_turn == "white":
                self.table_ui.game_log_label.config(text="P1 trebuie sa dai cu zarul!")
            else:
                self.table_ui.game_log_label.config(text="P2 trebuie sa dai cu zarul!")

    def all_pieces_in_home(self, player_color):
        """
        Check if all pieces of a player are in their home board.
        The method counts the number of pieces of the player outside their home board.
        If the player has no pieces outside, it returns True, indicating that all pieces are in the home board.
        Otherwise, it returns False.

        Parameters:
        - player_color (str): The color of the player ("white" or "black").

        Returns:
        bool: True if all pieces are in the home board, False otherwise.
        """

        nr_piece_outside = 0

        if self.table_ui.info_pieces[player_color][0] == 0:
            for col in range(6, 24):
                nr_piece_outside += len(self.table_ui.board[player_color][col][2])

        if nr_piece_outside == 0:
            return True
        else:
            return False

    def take_out_piece(self, player_color, column):
        """
        Remove a piece from the specified column of the player's board.
        This method removes the top piece from the specified column of the player's board,
        increments the count of removed pieces, and updates the dice values if a matching dice value is found.
        It also clears any displayed buttons, updates the game label, and checks for a winner.
        If the game is ongoing, it enables the roll dice button for the next turn.

        Parameters:
        - player_color (str): The color of the player ("white" or "black").
        - column (int): The column from which to remove a piece.

        Returns:
        None
        """
        self.table_ui.board[player_color][column][2][-1].destroy()
        self.table_ui.board[player_color][column][2].pop()
        self.table_ui.info_pieces[player_color][1] += 1

        is_removed = False
        for col_x in range(0, len(self.table_ui.dices)):
            if column + 1 == self.table_ui.dices[col_x]:
                self.table_ui.dices.remove(column + 1)
                is_removed = True
                break

        if is_removed == False:
            it_happens_once = False
            for i in range(1, 7):
                if it_happens_once == False:
                    for col_x in range(0, len(self.table_ui.dices)):
                        if i + column == self.table_ui.dices[col_x]:
                            self.table_ui.dices.remove(self.table_ui.dices[col_x])
                            it_happens_once = True
                            break

        for col_x in self.table_ui.all_buttons_pos:
            col_x.destroy()
        for col_x in range(0, len(self.table_ui.all_buttons_pos)):
            self.table_ui.all_buttons_pos.pop()

        self.table_ui.update_label(player_color)

        if self.table_ui.who_won() == 100:
            if len(self.table_ui.dices) == 0:

                self.table_ui.roll_dice_button.config(state="normal")
                if player_color == "white":
                    self.table_ui.game_log_label.config(text="P2 trebuie sa dai cu zarul!")
                else:
                    self.table_ui.game_log_label.config(text="P1 trebuie sa dai cu zarul!")

                if player_color == "white":
                    self.table_ui.current_turn = "black"
                    if self.table_ui.current_turn == "black" and self.table_ui.names["black"] == "AI":
                        self.table_ui.ai.turn_ai()
                else:
                    self.table_ui.current_turn = "white"
