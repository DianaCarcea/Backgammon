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


class TableUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.dice_images = None
        self.zar_button = None
        self.zar_frame = None
        self.zar_text = None
        self.zar_images = [Image.open(f"zaruri/{i}.png") for i in range(1, 7)]
        self.title("Triunghiuri Sus-Jos cu Spațiu Între Ele")
        self.geometry("1100x700")
        self.draw_table()

    def roll_dice(self):
        for widget in self.zar_frame.winfo_children():
            widget.destroy()

        results = [randint(1, 6) for _ in range(2)]

        for i in range(2):
            self.dice_images[i] = ImageTk.PhotoImage(self.zar_images[results[i] - 1].resize((50, 50), Image.BICUBIC))
            tk.Label(self.zar_frame, image=self.dice_images[i]).pack(side=tk.LEFT, padx=5)

    def draw_table(self):
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

        left = min(coord[0] for coord in triangles_coordinates)
        top = min(coord[1] for coord in triangles_coordinates)
        right = max(coord[2] for coord in triangles_coordinates)
        bottom = max(coord[3] for coord in triangles_coordinates)

        rect_id = canvas.create_rectangle(left, top, right, bottom, outline="#482618", width=10, fill='#995536')
        canvas.tag_lower(rect_id)

        self.zar_frame = tk.Frame(self, bg='brown')
        self.zar_frame.place(x=left+50, y=top + (bottom - top) // 1.5)
        self.zar_button = tk.Button(self, text="Aruncă Zarurile", command=self.roll_dice)
        self.zar_button.place(x=left+50, y=top + (bottom - top) // 1.8)

        self.dice_images = [None, None]

        for i in range(2):
            self.dice_images[i] = ImageTk.PhotoImage(self.zar_images[0].resize((50, 50), Image.BICUBIC))
            tk.Label(self.zar_frame, image=self.dice_images[i]).pack(side=tk.LEFT, padx=5)

        #  Dreptunghi drept sus
        small_rectangle_width1 = 35
        small_rectangle_height1 = (bottom - top) // 2

        small_rect_x = right + 12  # Distanta dreptunghiuri
        small_rect_y = top

        canvas.create_rectangle(small_rect_x, small_rect_y, small_rect_x + small_rectangle_width1,
                                small_rect_y + small_rectangle_height1, outline="#482618", width=10, fill='#995536')

        #  Dreptunghi drept jos
        small_rectangle_width = 35
        small_rectangle_height = (bottom - top) // 2

        small_rect_x = right + 12  # Distanta dreptunghiuri
        small_rect_y = top + small_rectangle_height1

        canvas.create_rectangle(small_rect_x, small_rect_y, small_rect_x + small_rectangle_width,
                                small_rect_y + small_rectangle_height, outline="#482618", width=10, fill='#995536')

        #  Dreptunghi mijloic
        rect_x = 7 * 40 - 15
        rect_y = top
        rect_width = 30
        rect_height = bottom - top

        canvas.create_rectangle(rect_x, rect_y, rect_x + rect_width,
                                rect_y + rect_height, outline="#482618", width=0, fill='#482618')

        centering_table(canvas, left, top, right, bottom)
