import random
import copy

PLAYER_A = 'A'
PLAYER_N = 'N'

WINNER = None


class Game:

    def __init__(self):
        self.board = [
            ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', 'Col_N', 'Scos'],
            ['A', '_', '_', '_', 'N', '_', 'N', '_', '_', '_', '_', 'A', '_', '_'],
            ['A', '_', '_', '_', 'N', '_', 'N', '_', '_', '_', '_', 'A', '_', '_'],
            ['A', '_', '_', '_', 'N', '_', 'N', '_', '_', '_', '_', '_', '_', '_'],
            ['A', '_', '_', '_', '_', '_', 'N', '_', '_', '_', '_', '_', '_', '_'],
            ['A', '_', '_', '_', '_', '_', 'N', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],

            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'],
            ['N', '_', '_', '_', '_', '_', 'A', '_', '_', '_', '_', '_', '_', '_'],
            ['N', '_', '_', '_', '_', '_', 'A', '_', '_', '_', '_', '_', '_', '_'],
            ['N', '_', '_', '_', 'A', '_', 'A', '_', '_', '_', '_', '_', '_', '_'],
            ['N', '_', '_', '_', 'A', '_', 'A', '_', '_', '_', '_', 'N', '_', '_'],
            ['N', '_', '_', '_', 'A', '_', 'A', '_', '_', '_', '_', 'N', '_', '_'],
            ['12', '11', '10', '09', '08', '07', '06', '05', '04', '03', '02', '01', 'Col_A', 'Scos']
        ]

        self.current_player = 'N'

    def print_board(self, board):
        for i, row in enumerate(board):
            if i == 0 or i == len(board) - 1:
                separator = ' '
                print(separator.join(row[:6]) + ' || ' + separator.join(row[6:]))
            else:
                separator = '  '
                print(separator.join(row[:6]) + '  || ' + separator.join(row[6:]))

    def roll_dice(self):
        zar1 = random.randint(1, 6)
        zar2 = random.randint(1, 6)
        return zar1, zar2

    def get_first_player(self):
        dice_player_A = self.roll_dice()
        dice_player_N = self.roll_dice()
        print(f"Player A: {dice_player_A}")
        print(f"Player B: {dice_player_N}")

        if sum(dice_player_A) > sum(dice_player_N):
            return PLAYER_A
        elif sum(dice_player_A) < sum(dice_player_N):
            return PLAYER_N
        else:
            print("Egalitate. Reluati aruncarea zarurilor.")
            return self.get_first_player()

    def get_position_pieces(self, player, board):
        upper_cols = board[1][:-2]
        bottom_cols = board[30][:-2]

        disponible_pieces_up = []
        disponible_pieces_bottom = []

        for i, col in enumerate(upper_cols):
            if col == player:
                disponible_pieces_up.append(i)

        for i, col in enumerate(bottom_cols):
            if col == player:
                disponible_pieces_bottom.append(i)

        return disponible_pieces_up, disponible_pieces_bottom

    def eliminate_invalid_pieces_player_A(self, player, current_move, board, selected_dice, is_up):

        upper_cols = board[1][:-2]
        bottom_cols = board[30][:-2]

        # FOR PLAYER A
        if player == PLAYER_A:

            # when UP
            if is_up == "UP":
                next_move = current_move - selected_dice

                copy_board = copy.deepcopy(board)

                # cand suntem sus
                if next_move > 0:
                    if upper_cols[next_move] == "_" or upper_cols[next_move] == PLAYER_A:
                        nr_pieces_current = self.get_nr_pieces_on_col(current_move, "top")
                        nr_pieces_next = self.get_nr_pieces_on_col(next_move, "top") + 1

                        copy_board[nr_pieces_next][next_move] = player
                        copy_board[nr_pieces_current][current_move] = '_'

                        self.print_board(copy_board)
                        return copy_board

                    elif upper_cols[next_move] == PLAYER_N:
                        nr_pieces_current = self.get_nr_pieces_on_col(current_move, "top")
                        nr_pieces_next = self.get_nr_pieces_on_col(next_move, "top") + 1

                        if nr_pieces_next == 1:
                            copy_board[nr_pieces_next][next_move] = player
                            copy_board[nr_pieces_current][current_move] = '_'

                            self.print_board(copy_board)
                            return copy_board

                # cand ne mutam suntem jos
                if next_move <= 0:
                    move_down_abs = abs(next_move) - 1
                    if bottom_cols[move_down_abs] == "_" or bottom_cols[move_down_abs] == PLAYER_A:
                        nr_pieces_current = self.get_nr_pieces_on_col(current_move, "bottom")
                        nr_pieces_next = self.get_nr_pieces_on_col(move_down_abs, "bottom") + 1

                        copy_board[31 - nr_pieces_next][move_down_abs] = player
                        copy_board[nr_pieces_current][current_move] = '_'

                        self.print_board(copy_board)
                        return copy_board
                    elif bottom_cols[move_down_abs] == PLAYER_N:
                        nr_pieces_current = self.get_nr_pieces_on_col(current_move, "bottom")
                        nr_pieces_next = self.get_nr_pieces_on_col(next_move, "bottom") + 1

                        if nr_pieces_next == 1:
                            copy_board[31 - nr_pieces_next][move_down_abs] = player
                            copy_board[nr_pieces_current][current_move] = '_'

                            self.print_board(copy_board)
                            return copy_board

            # when down
            if is_up == "DOWN":
                next_move = current_move + selected_dice

                if next_move < 11:
                    if bottom_cols[next_move] == "_" or bottom_cols[next_move] == PLAYER_A:
                        copy_board = copy.deepcopy(board)

                        nr_pieces_current = self.get_nr_pieces_on_col(current_move, "bottom")
                        nr_pieces_next = self.get_nr_pieces_on_col(next_move, "bottom") + 1

                        copy_board[31 - nr_pieces_next][next_move] = player
                        copy_board[31 - nr_pieces_current][current_move] = '_'

                        self.print_board(copy_board)
                        return copy_board
                    elif bottom_cols[next_move] == PLAYER_N:
                        copy_board = copy.deepcopy(board)

                        nr_pieces_current = self.get_nr_pieces_on_col(current_move, "bottom")
                        nr_pieces_next = self.get_nr_pieces_on_col(next_move, "bottom") + 1

                        if nr_pieces_next == 1:
                            copy_board[31 - nr_pieces_next][next_move] = player
                            copy_board[31 - nr_pieces_current][current_move] = '_'

                        self.print_board(copy_board)
                        return copy_board

    def get_nr_pieces_on_col(self, col, top_bottom_pos):
        total_pieces = 0

        if top_bottom_pos == "top":
            for i in range(1, 16):
                if self.board[i][col] != '_':
                    total_pieces += 1

            return total_pieces

        else:
            for i in range(30, 15, -1):
                if self.board[i][col] != '_':
                    total_pieces += 1

            return total_pieces

    def can_play_both_dice_player_A(self, current_pieces_top, current_pieces_bottom, selected_dice, other_dice):
        remaining_pieces_up = []
        remaining_pieces_down = []

        for current_move in current_pieces_top:
            current_board = self.eliminate_invalid_pieces_player_A(self.current_player, current_move, self.board,
                                                                   selected_dice,
                                                                   "UP")
            if current_board is not None:
                copy_board = copy.deepcopy(current_board)
                current_board = self.eliminate_invalid_pieces_player_A(self.current_player, current_move, copy_board,
                                                                       other_dice, "UP")
                if current_board is not None:
                    remaining_pieces_up.append(current_move)

        for current_move in current_pieces_bottom:
            current_board = self.eliminate_invalid_pieces_player_A(self.current_player, current_move, self.board,
                                                                   selected_dice,
                                                                   "DOWN")
            if current_board is not None:
                copy_board = copy.deepcopy(current_board)
                current_board = self.eliminate_invalid_pieces_player_A(self.current_player, current_move, copy_board,
                                                                       other_dice, "DOWN")
                if current_board is not None:
                    remaining_pieces_down.append(current_move)

        return remaining_pieces_up, remaining_pieces_down

    def start_game(self):
        self.print_board(self.board)

        print("Settling the first player...\n")
        self.current_player = self.get_first_player()

        print(f"Curent player: {self.current_player}")

        dice1, dice2 = self.roll_dice()
        dice1, dice2 = 1, 5
        print(dice1, dice2)
        print("Select which dice...\n")

        nr_dice = int(input())

        if nr_dice == 1:
            selected_dice = dice1
            other_dice = dice2
        else:
            selected_dice = dice2
            other_dice = dice1

        if self.current_player == PLAYER_A:
            current_pieces_top, current_pieces_bottom = self.get_position_pieces(self.current_player, self.board)

            remaining_pieces_up, remaining_pieces_down = self.can_play_both_dice_player_A(current_pieces_top,
                                                                                          current_pieces_bottom,
                                                                                          selected_dice, other_dice)
            print(remaining_pieces_up, remaining_pieces_down)
