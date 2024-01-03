import os
import tkinter as tk
from random import randint

from PIL import Image, ImageTk


def draw_triangle(canvas, x, y, small_side, scale_factor, color, direction="up"):
    x1, y1 = x, y
    if direction == "up":
        x2, y2 = x - small_side/2, y + small_side * scale_factor
        x3, y3 = x + small_side/2, y + small_side * scale_factor
    else:
        x2, y2 = x - small_side/2, y - small_side * scale_factor
        x3, y3 = x + small_side/2, y - small_side * scale_factor

    canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline="black")


def centering_table(canvas, left, top, right, bottom):
    center_x = (canvas.winfo_reqwidth() - (right - left)) / 2
    center_y = (canvas.winfo_reqheight() - (bottom - top)) / 2

    canvas.move("all", center_x - left, center_y - top)
    canvas.update_idletasks()


class TableUI(tk.Frame):
    def __init__(self, master=None, back_callback=None, play_ai=False):
        super().__init__(master)

        self.play_ai = play_ai
        self.dice_images = None
        self.left, self.top, self.right, self.bottom = 0, 0, 0, 0
        self.back_callback = back_callback
        self.draw_table()
        self.create_back_button()

    def create_back_button(self):
        button_back = tk.Button(self, text="Înapoi la pagina principală", command=self.on_back_button_click,bg="white", fg="black",
                           font=("Arial", 10), padx=10, pady=5, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        button_back.place(x=self.left + 10, y=self.top + 30)

    def on_back_button_click(self):
        if self.back_callback:
            self.back_callback()
        self.destroy()

    def create_dice_button(self, top, bottom):
        button = tk.Button(self, text="Arunca zaruri", command=self.roll_dice, bg="#482618", fg="white",
                           font=("Arial", 12), padx=10, pady=5, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        button.place(x=self.left + 60, y=top + (bottom - top) // 1.8, anchor='w')

    def load_dice_images(self):
        original_images = [Image.open(os.path.join("zaruri", f"{i}.png")) for i in range(1, 7)]
        self.dice_images = [ImageTk.PhotoImage(image=image.resize((50, 50))) for image in original_images]

    def roll_dice(self):
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)

        dice_image1 = self.dice_images[dice1 - 1]
        dice_label1 = tk.Label(self, image=dice_image1)
        dice_label1.image = dice_image1
        dice_label1.place(x=self.left + 50, y=self.top + (self.bottom - self.top) // 1.5)

        dice_image2 = self.dice_images[dice2 - 1]
        dice_label2 = tk.Label(self, image=dice_image2)
        dice_label2.image = dice_image2
        dice_label2.place(x=self.left + 50 + 80, y=self.top + (self.bottom - self.top) // 1.5)

    def draw_table(self):
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

        rect_id = canvas.create_rectangle(self.left, self.top, self.right, self.bottom, outline="#482618", width=10, fill='#995536')
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
        centering_table(canvas, self.left, self.top, self.right, self.bottom)
