from tkinter import *
from customtkinter import CTkButton
from PIL import Image, ImageTk


class AboutTab:
    def __init__(self, tab: Tk, font: dict, lp, main_app):
        self.tab = tab
        self.font = font
        self.main_app = main_app

        self.lp = lp

        img = Image.open("image/me.jpg").convert("RGBA")

        percent = 35
        width, height = img.size
        new_width = int(width * percent / 100)
        new_height = int(height * percent / 100)

        # Изменяем размер изображения
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        self.my_photo = ImageTk.PhotoImage(resized_img)
        self.__create_item()

    def __create_item(self):
        self.calculator_tab_button = CTkButton(
            self.tab,
            width=70,
            height=50,
            text=self.lp["back"],
            command=lambda: self.main_app.choese_tab("main"),
            corner_radius=6,
            font=("Courier", 13, "bold")
        )
        self.my_photo_label = Label(image=self.my_photo)

        self.labels = [
            Label(
                self.tab,
                text=self.lp["author"],
                font=self.font["h2"]
            ),
            Label(
                self.tab,
                text=self.lp["group"],
                font=self.font["h3"]
            ),
            Label(
                self.tab,
                text=self.lp["name"],
                font=self.font["h3"]
            ),
            Label(
                self.tab,
                text="gmail: Nikikikiplays2016@gmail.com",
                font=self.font["h3"]
            ),
            Label(
                self.tab,
                text="tg: @picard_off",
                font=self.font["h3"]
            )
        ]
        self.places = [[218, 460], [40, 490], [40, 520], [40, 550], [40, 580]]
    def show_items(self):
        self.my_photo_label.place(x=80, y=2)
        self.calculator_tab_button.place(x=185, y=560)

        for i,lab in enumerate(self.labels):
            lab.place(x=self.places[i][0], y=self.places[i][1])

