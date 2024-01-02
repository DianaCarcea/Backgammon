import tkinter as tk


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
        self.title("Triunghiuri Sus-Jos cu Spațiu Între Ele")
        self.geometry("1100x700")
        self.draw_table()

    def draw_table(self):
        canvas = tk.Canvas(self, width=1100, height=700, bg="white")
        canvas.pack()

        triangles_coordinates = []  # Lista pentru a stoca coordonatele triunghiurilor

        # Desenează 6 triunghiuri sus cu vârf în jos
        for i in range(6):
            x = 40 + i * 40
            if i % 2:
                draw_triangle(canvas, x, 200, 40, 5, "#532a1a", direction="down")
            else:
                draw_triangle(canvas, x, 200, 40, 5, "#ddad7d", direction="down")

            triangles_coordinates.append(canvas.bbox("all"))


        space_between_groups = 280

        for i in range(6):
            x = 40 + i * 40 + space_between_groups  # Spațierea triunghiurilor
            if i % 2:
                draw_triangle(canvas, x, 200, 40, 5, "#532a1a", direction="down")
            else:
                draw_triangle(canvas, x, 200, 40, 5, "#ddad7d", direction="down")

            triangles_coordinates.append(canvas.bbox("all"))


        # Desenează 6 triunghiuri jos cu vârf în sus
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

        #  Dreptunghi drept
        small_rectangle_width = 35
        small_rectangle_height = bottom - top

        small_rect_x = right + 12  # Distanta dreptunghiuri
        small_rect_y = top

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
