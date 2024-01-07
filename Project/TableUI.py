import os
import tkinter as tk
from random import randint
from Board import Board

from PIL import Image, ImageTk


def draw_triangle(canvas, x, y, small_side, scale_factor, color, direction="up"):
    x1, y1 = x, y
    if direction == "up":
        x2, y2 = x - small_side / 2, y + small_side * scale_factor
        x3, y3 = x + small_side / 2, y + small_side * scale_factor
    else:
        x2, y2 = x - small_side / 2, y - small_side * scale_factor
        x3, y3 = x + small_side / 2, y - small_side * scale_factor

    canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline="black")


def centering_table(canvas, left, top, right, bottom):
    center_x = (canvas.winfo_reqwidth() - (right - left)) / 2
    center_y = (canvas.winfo_reqheight() - (bottom - top)) / 2

    canvas.move("all", center_x - left, center_y - top)
    canvas.update_idletasks()


class TableUI(tk.Frame):
    def __init__(self, master=None, back_callback=None, play_ai=False):
        super().__init__(master)
        self.selected_label = None
        self.is_bordura_groasa = False
        self.play_ai = play_ai
        self.dice_images = None
        self.left, self.top, self.right, self.bottom = 0, 0, 0, 0
        self.back_callback = back_callback

        self.dice_p1 = None
        self.current_player = "P1"
        self.draw = True

        board = Board()
        self.log_label = None
        self.create_label()
        self.change_text_label("Se decide cine face primul mutarea: P1 arunca zarurile")

        self.initial_board = board.board

        self.draw_table(self.initial_board)

        self.create_back_button()

    def create_back_button(self):
        button_back = tk.Button(self, text="Înapoi la pagina principală", command=self.on_back_button_click, bg="white",
                                fg="black",
                                font=("Arial", 10), padx=10, pady=5, relief=tk.FLAT, borderwidth=0,
                                highlightthickness=0)
        button_back.place(x=self.left + 10, y=self.top + 30)

    def on_back_button_click(self):
        if self.back_callback:
            self.back_callback()
        self.destroy()

    def create_dice_button(self, top, bottom):
        button = tk.Button(self, text="Arunca zaruri", command=lambda: self.roll_dice(self.current_player), bg="#482618", fg="white",
                           font=("Arial", 12), padx=10, pady=5, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        button.place(x=self.left + 60, y=top + (bottom - top) // 1.8, anchor='w')

    def load_dice_images(self):
        original_images = [Image.open(os.path.join("zaruri", f"{i}.png")) for i in range(1, 7)]
        self.dice_images = [ImageTk.PhotoImage(image=image.resize((50, 50))) for image in original_images]

    def roll_dice(self, player):
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)

        dice_image1 = self.dice_images[dice1 - 1]
        dice_label1 = tk.Label(self, image=dice_image1, bd=1, relief="solid")
        dice_label1.image = dice_image1
        dice_label1.place(x=self.left + 50, y=self.top + (self.bottom - self.top) // 1.5)

        dice_image2 = self.dice_images[dice2 - 1]
        dice_label2 = tk.Label(self, image=dice_image2, bd=1, relief="solid")
        dice_label2.image = dice_image2
        dice_label2.place(x=self.left + 50 + 80, y=self.top + (self.bottom - self.top) // 1.5)

        dice_label1.bind("<Button-1>", lambda event, label=dice_label1: self.afiseaza_mesaj(event, label, dice1))
        dice_label2.bind("<Button-1>", lambda event, label=dice_label2: self.afiseaza_mesaj(event, label, dice2))

        if self.draw == True:
            if self.current_player == "P1":
                self.change_text_label(f" P1 a aruncat {dice1} {dice2}\n P2 arunca zarurile")
                self.dice_p1 = dice1, dice2
            else:
                dice1_p1, dice2_p1 = self.dice_p1

                if dice1_p1 + dice1_p1 > dice1 + dice2:
                    self.change_text_label(f" P2 a aruncat {dice1} {dice2}\n P1 a aruncat {dice1_p1} {dice1_p1}\n P1 muta primul\n P1 arunca zarurile")
                    self.draw = False
                elif dice1_p1 + dice1_p1 < dice1 + dice2:
                    self.change_text_label(f" P2 a aruncat {dice1} {dice2}\n P1 a aruncat {dice1_p1} {dice1_p1}\n P2 muta primul\n P2 arunca zarurile")
                    self.draw = False
                else:
                    self.change_text_label(f" P2 a aruncat {dice1} {dice2}\n P1 a aruncat {dice1_p1} {dice1_p1}\n Egalitate\n P1 arunca zarurile")
        else:
            if self.current_player == "P1":
                self.change_text_label(f"P1 ai aruncat {dice1} {dice2}\n muta piesele")
            else:
                self.change_text_label(f"P2 ai aruncat {dice1} {dice2}\n muta piesele")

        if self.current_player == "P1":
            self.current_player = "P2"
        else:
            self.current_player = "P1"

    def afiseaza_mesaj(self, event, label, dice):
        if self.selected_label is not None and self.selected_label == label:
            label.config(bd=1)
            self.selected_label = None
            self.change_text_label(f"Numarul zarului este: {dice}")
        else:
            if self.selected_label is not None:
                self.selected_label.config(bd=1)
            label.config(bd=5)
            self.selected_label = label
            self.change_text_label(f"Numarul zarului este: {dice}")

        if self.selected_label is None:
            print("Niciun zar nu este selectat.")
            self.change_text_label(f"Trebuie să selectezi un zar!")
        else:
            print(f"Zarul selectat are eticheta {label} și numărul {dice}.")

    def create_label(self):
        self.log_label = tk.Label(self, text="", font=14)
        self.log_label.pack(side="top", pady=(30, 0), anchor="s")

    def change_text_label(self, text):
        self.log_label.config(text=text)

    def draw_table(self, board):
        self.load_dice_images()
        self.configure(bg="brown")
        canvas = tk.Canvas(self, width=1100, height=700, bg="brown", bd=0, highlightthickness=0, relief='ridge')
        canvas.pack()

        triangles_coordinates = []

        for i in range(6):
            x = 40 + i * 40
            if i % 2:
                draw_triangle(canvas, x, 200, 40, 5, "#532a1a", direction="down")
            else:
                draw_triangle(canvas, x, 200, 40, 5, "#ddad7d", direction="down")

            triangles_coordinates.append(canvas.bbox("all"))

        space_between_groups = 280

        for i in range(6):
            x = 40 + i * 40 + space_between_groups
            if i % 2:
                draw_triangle(canvas, x, 200, 40, 5, "#532a1a", direction="down")
            else:
                draw_triangle(canvas, x, 200, 40, 5, "#ddad7d", direction="down")

            triangles_coordinates.append(canvas.bbox("all"))

        for i in range(6):
            x = 40 + i * 40
            if i % 2:
                draw_triangle(canvas, x, 250, 40, 5, "#ddad7d", direction="up")
            else:
                draw_triangle(canvas, x, 250, 40, 5, "#532a1a", direction="up")

            triangles_coordinates.append(canvas.bbox("all"))

        for i in range(6):
            x = 40 + i * 40 + space_between_groups
            if i % 2:
                draw_triangle(canvas, x, 250, 40, 5, "#ddad7d", direction="up")
            else:
                draw_triangle(canvas, x, 250, 40, 5, "#532a1a", direction="up")

            triangles_coordinates.append(canvas.bbox("all"))

        self.left = min(coord[0] for coord in triangles_coordinates)
        self.top = min(coord[1] for coord in triangles_coordinates)
        self.right = max(coord[2] for coord in triangles_coordinates)
        self.bottom = max(coord[3] for coord in triangles_coordinates)

        self.create_dice_button(self.top, self.bottom)

        rect_id = canvas.create_rectangle(self.left, self.top, self.right, self.bottom, outline="#482618", width=10,
                                          fill='#995536')
        canvas.tag_lower(rect_id)

        #  Dreptunghi drept sus
        small_rectangle_width1 = 35
        small_rectangle_height1 = (self.bottom - self.top) // 2

        small_rect_x = self.right + 12  # Distanta dreptunghiuri
        small_rect_y = self.top

        canvas.create_rectangle(small_rect_x, small_rect_y, small_rect_x + small_rectangle_width1,
                                small_rect_y + small_rectangle_height1, outline="#482618", width=10, fill='#995536')

        #  Poza player 2
        if not self.play_ai:
            image_original2 = Image.open(os.path.join("images", "player2.png"))
            image_resized2 = image_original2.resize((100, 100))
            image_tk2 = ImageTk.PhotoImage(image_resized2)

            canvas.create_image(small_rect_x + small_rectangle_width1 / 2 + 100,
                                small_rect_y + small_rectangle_height1 / 2,
                                image=image_tk2)
        else:
            image_original2 = Image.open(os.path.join("images", "ai_player.png"))
            image_resized2 = image_original2.resize((60, 80))
            image_tk2 = ImageTk.PhotoImage(image_resized2)

            canvas.create_image(small_rect_x + small_rectangle_width1 / 2 + 82,
                                small_rect_y + small_rectangle_height1 / 2,
                                image=image_tk2)

        canvas.image_tk2 = image_tk2

        #  Dreptunghi drept jos
        small_rectangle_width2 = 35
        small_rectangle_height2 = (self.bottom - self.top) // 2

        small_rect_x = self.right + 12  # Distanta dreptunghiuri
        small_rect_y = self.top + small_rectangle_height1

        canvas.create_rectangle(small_rect_x, small_rect_y, small_rect_x + small_rectangle_width2,
                                small_rect_y + small_rectangle_height2, outline="#482618", width=10, fill='#995536')

        #  Poza player 1
        if not self.play_ai:
            image_original1 = Image.open(os.path.join("images", "player1.png"))
            image_resized = image_original1.resize((100, 100))
            image_tk1 = ImageTk.PhotoImage(image_resized)

            canvas.create_image(small_rect_x + small_rectangle_width2 / 2 + 100,
                                small_rect_y + small_rectangle_height2 / 2,
                                image=image_tk1)
        else:
            image_original1 = Image.open(os.path.join("images", "h_player.png"))
            image_resized = image_original1.resize((65, 80))
            image_tk1 = ImageTk.PhotoImage(image_resized)

            canvas.create_image(small_rect_x + small_rectangle_width2 / 2 + 82,
                                small_rect_y + small_rectangle_height2 / 2,
                                image=image_tk1)

        canvas.image_tk1 = image_tk1

        #  Dreptunghi mijloc
        rect_x = 7 * 40 - 15
        rect_y = self.top
        rect_width = 30
        rect_height = self.bottom - self.top

        canvas.create_rectangle(rect_x, rect_y, rect_x + rect_width,
                                rect_y + rect_height, outline="#482618", width=0, fill='#482618')

        #  Centrare tabla
        self.draw_pieces_for_board(canvas, board)

        centering_table(canvas, self.left, self.top, self.right, self.bottom)

    def change_color(self, event, canvas, oval_id):
        canvas.itemconfig(oval_id, fill="grey")

    def draw_pieces_for_board(self, canvas, board):
        print(board)

        min_x1 = 57
        min_y1 = 35
        min_x2 = 22
        min_y2 = 0

        for col in range(0, 12):
            max_i = None

            for i in range(0, 15):
                color = None

                if board[i + 1][col] == 'A':
                    color = 'white'
                    color_text = 'black'
                elif board[i + 1][col] == 'N':
                    color = 'black'
                    color_text = 'white'

                if color is not None:
                    if i + 1 >= 6:
                        max_i = i + 1
                    else:
                        if col >= 6:
                            canvas.create_oval(min_x1 + (col + 1) * 40, min_y1 + i * 35, min_x2 + (col + 1) * 40,
                                               min_y2 + i * 35, outline="#482618", width=1, fill=color)
                        else:
                            oval_id = canvas.create_oval(min_x1 + col * 40, min_y1 + i * 35, min_x2 + col * 40, min_y2 + i * 35,
                                               outline="#482618", width=1, fill=color)
                            canvas.tag_bind(oval_id, "<Button-1>",
                                                 lambda event, oval_id=oval_id: self.change_color(event, canvas, oval_id))

            if max_i is not None:
                canvas.create_text(min_x1 - 18 + col*40, min_y1 + 4 * 35 - 18, text=f"{max_i}", font=("Arial", 12),
                                   fill=color_text, tags="text")

        max_x1 = 57
        max_y1 = 450
        max_x2 = 22
        max_y2 = 450 - 35

        for col in range(0, 12):
            max_i = None

            for i in range(0, 15):
                color = None

                if board[30 - i][col] == 'A':
                    color = 'white'
                    color_text = 'black'
                elif board[30 - i][col] == 'N':
                    color = 'black'
                    color_text = 'white'

                if color is not None:
                    if 30 - i <= 25:
                        max_i = i + 1
                    else:
                        if col >= 6:
                            canvas.create_oval(max_x1 + (col + 1) * 40, max_y1 - i * 35, max_x2 + (col + 1) * 40,
                                               max_y2 - i * 35, outline="#482618", width=1, fill=color)
                        else:
                            canvas.create_oval(max_x1 + col * 40, max_y1 - i * 35, max_x2 + col * 40, max_y2 - i * 35,
                                               outline="#482618", width=1, fill=color)

            if max_i is not None:
                canvas.create_text(max_x1 - 18 + col*40, max_y1 - 4 * 35 - 18, text=f"{max_i}", font=("Arial", 12),
                                   fill=color_text, tags="text")
