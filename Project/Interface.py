import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk


class Interface:
    def __init__(self, window):
        self.image_original = Image.open("fundal.png")
        self.image_ratio = self.image_original.size[0] / self.image_original.size[1]

        self.canvas = tk.Canvas(window, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid(column=0, columnspan=3, row=0, sticky='nsew')
        self.canvas.bind('<Configure>', self.responsive_page)

        self.title_text_id = None

        self.select_text_id = None

        self.image_button1 = Image.open("HH.png")
        self.image_button2 = Image.open("HA.png")

        self.photo_button1 = ImageTk.PhotoImage(self.image_button1)
        self.photo_button2 = ImageTk.PhotoImage(self.image_button2)

        self.button1 = tk.Button(self.canvas, image=self.photo_button1, command=self.on_button1_click, bd=1)
        self.button1_window = self.canvas.create_window(120, 250, window=self.button1, anchor='nw')

        self.button2 = tk.Button(self.canvas, image=self.photo_button2, command=self.on_button2_click, bd=1)
        self.button2_window = self.canvas.create_window(120, 450, window=self.button2, anchor='nw')

        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

    def responsive_page(self, event):
        global resized_tk
        canvas_ratio = event.width/event.height

        if canvas_ratio > self.image_ratio:
            width = int(event.width)
            height = int(event.width/self.image_ratio)
        else:
            height = int(event.height)
            width = int(height * self.image_ratio)

        resized_image = self.image_original.resize((width, height))
        resized_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(int(event.width/2), int(event.height/2), image=resized_tk, anchor='center')

        self.title_text_id = self.canvas.create_text(event.width // 2, 120, text="Jocul de table", fill="#cbc9c7",
                                                     font=("Comic Sans MS", 30, "bold"), anchor='center')

        button_x = int(event.width / 6)
        button_y1 = 250

        button_width = int(event.width / 6)
        button_height = int(button_width * (self.image_button1.size[1] / self.image_button1.size[0]))

        text_font_size = int(20 * (button_width / self.image_button1.size[0]))
        dist_text = int(0.15 * button_height)
        dist_text_and_button = int(0.4 * button_height)

        self.select_text_id = self.canvas.create_text(button_x+dist_text, button_y1-dist_text_and_button, text="Selectare mod:", fill="#cbc9c7",
                                font=("Comic Sans MS", text_font_size, "bold"), anchor='nw')

        self.photo_button1 = ImageTk.PhotoImage(self.image_button1.resize((button_width, button_height)))
        self.photo_button2 = ImageTk.PhotoImage(self.image_button2.resize((button_width, button_height)))

        self.button1.config(image=self.photo_button1)
        self.button2.config(image=self.photo_button2)

        button_y2 = button_y1 + button_height + 50

        self.canvas.coords(self.button1_window, button_x, button_y1)
        self.canvas.coords(self.button2_window, button_x, button_y2)

    def on_button1_click(self):
        print("Buton 1 apăsat!")

    def on_button2_click(self):
        print("Buton 2 apăsat!")



