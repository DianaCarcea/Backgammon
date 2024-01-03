import os
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

from TableUI import TableUI


class Interface:
    def __init__(self, master):
        self.master = master
        self.table_ui = None
        self.image_original_page1 = None
        self.image_ratio_page1 = None

        #  First page
        self.canvas_page1 = tk.Canvas(master, bd=0, highlightthickness=0, relief='ridge')
        self.canvas_page1.grid(column=0, columnspan=3, row=0, sticky='nsew')
        self.canvas_page1.bind('<Configure>', self.responsive_page)

        self.title_text_id = None
        self.select_text_id = None
        self.button1 = None
        self.button2 = None
        self.image_button1 = None
        self.image_button2 = None
        self.photo_button1 = None
        self.photo_button2 = None
        self.button1_window = None
        self.button2_window = None

        self.play_ai = False
        self.init_page_content()

    def init_page_content(self):

        self.image_original_page1 = Image.open(os.path.join("images", "fundal.png"))
        self.image_ratio_page1 = self.image_original_page1.size[0] / self.image_original_page1.size[1]

        self.title_text_id = self.canvas_page1.create_text(self.canvas_page1.winfo_reqwidth() // 2, 120,
                                                           text="Jocul de table", fill="#cbc9c7",
                                                           font=("Comic Sans MS", 30, "bold"), anchor='center')
        self.init_buttons()

    def init_buttons(self):
        self.image_button1 = Image.open(os.path.join("images", "HH.png"))
        self.image_button2 = Image.open(os.path.join("images", "HA.png"))

        self.photo_button1 = ImageTk.PhotoImage(self.image_button1)
        self.photo_button2 = ImageTk.PhotoImage(self.image_button2)

        self.button1 = tk.Button(self.canvas_page1, image=self.photo_button1, command=self.on_button1_click, bd=1)
        self.button1_window = self.canvas_page1.create_window(120, 250, window=self.button1, anchor='nw')

        self.button2 = tk.Button(self.canvas_page1, image=self.photo_button2, command=self.on_button2_click, bd=1)
        self.button2_window = self.canvas_page1.create_window(120, 450, window=self.button2, anchor='nw')

        button_x = int(self.canvas_page1.winfo_reqwidth() / 6)
        button_y1 = 250
        button_width = int(self.canvas_page1.winfo_reqwidth() / 6)
        button_height = int(button_width * (self.image_button1.size[1] / self.image_button1.size[0]))
        text_font_size = int(20 * (button_width / self.image_button1.size[0]))
        dist_text = int(0.15 * button_height)
        dist_text_and_button = int(0.4 * button_height)

        self.select_text_id = self.canvas_page1.create_text(button_x + dist_text, button_y1 - dist_text_and_button,
                                                            text="Selectare mod:", fill="#cbc9c7",
                                                            font=("Comic Sans MS", text_font_size, "bold"), anchor='nw')

        button_y2 = button_y1 + button_height + 50

        self.canvas_page1.coords(self.button1_window, button_x, button_y1)
        self.canvas_page1.coords(self.button2_window, button_x, button_y2)

    def responsive_page(self, event):
        global resized_tk
        canvas_ratio = event.width / event.height

        if canvas_ratio > self.image_ratio_page1:
            width = int(event.width)
            height = int(event.width / self.image_ratio_page1)
        else:
            height = int(event.height)
            width = int(height * self.image_ratio_page1)

        resized_image = self.image_original_page1.resize((width, height))
        resized_tk = ImageTk.PhotoImage(resized_image)
        self.canvas_page1.create_image(int(event.width / 2), int(event.height / 2), image=resized_tk, anchor='center')

        self.title_text_id = self.canvas_page1.create_text(event.width // 2, 120, text="Jocul de table", fill="#cbc9c7",
                                                           font=("Comic Sans MS", 30, "bold"), anchor='center')

        button_x = int(event.width / 6)
        button_y1 = 250

        button_width = int(event.width / 6)
        button_height = int(button_width * (self.image_button1.size[1] / self.image_button1.size[0]))

        text_font_size = int(20 * (button_width / self.image_button1.size[0]))
        dist_text = int(0.15 * button_height)
        dist_text_and_button = int(0.4 * button_height)

        self.select_text_id = self.canvas_page1.create_text(button_x + dist_text, button_y1 - dist_text_and_button,
                                                            text="Selectare mod:", fill="#cbc9c7",
                                                            font=("Comic Sans MS", text_font_size, "bold"), anchor='nw')

        self.photo_button1 = ImageTk.PhotoImage(self.image_button1.resize((button_width, button_height)))
        self.photo_button2 = ImageTk.PhotoImage(self.image_button2.resize((button_width, button_height)))

        self.button1.config(image=self.photo_button1)
        self.button2.config(image=self.photo_button2)

        button_y2 = button_y1 + button_height + 50

        self.canvas_page1.coords(self.button1_window, button_x, button_y1)
        self.canvas_page1.coords(self.button2_window, button_x, button_y2)

    def on_button1_click(self):
        self.play_ai = False
        self.table_ui = TableUI(self.master, back_callback=self.show_first_page, play_ai=self.play_ai)
        self.table_ui.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_first_page(self):
        self.canvas_page1.place(relx=0, rely=0, relwidth=1, relheight=1)

    def on_button2_click(self):
        self.play_ai = True
        self.table_ui = TableUI(self.master, back_callback=self.show_first_page, play_ai=self.play_ai)
        self.table_ui.place(relx=0, rely=0, relwidth=1, relheight=1)

