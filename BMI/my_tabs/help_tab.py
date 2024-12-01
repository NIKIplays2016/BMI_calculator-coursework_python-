from tkinter import *
from customtkinter import CTkButton
from PIL import Image, ImageTk


class HelpTab:
    def __init__(self, tab: Tk, font: dict, lp, main_app):
        self.tab = tab
        self.font = font
        self.main_app = main_app

        self.lp = lp

        img = Image.open("image/help.jpg").convert("RGBA")

        percent = 50
        width, height = img.size
        new_width = int(width * percent / 100)
        new_height = int(height * percent / 100)

        # Изменяем размер изображения
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        self.help_photo = ImageTk.PhotoImage(resized_img)
        self.__create_item()

    def __create_item(self):

        self.help_photo_label = Label(image=self.help_photo)

        self.labels = [
            Label(
                self.tab,
                text=self.lp["bmi"],
                font=self.font["h2"]
            ),
            Label(
                self.tab,
                text=self.lp["program_allows"]+":",
                font=self.font["h2"]
            ),
            Label(
                self.tab,
                text=self.lp["allows1"],
                font=self.font["h3"]
            ),
            Label(
                self.tab,
                text=self.lp["allows2"],
                font=self.font["h3"]
            ),
            Label(
                self.tab,
                text=self.lp["allows3"],
                font=self.font["h3"]
            ),
            Label(
                self.tab,
                text=self.lp["allows4"],
                font=self.font["h3"]
            )
        ]
        self.places = [
            (20, 20),
            (20, 300),
            (20, 350),
            (20, 375),
            (20, 400),
            (20, 425)
        ]

        self.calculator_tab_button = CTkButton(
            self.tab,
            width=70,
            height=50,
            text=self.lp["back"],
            command=lambda: self.main_app.choese_tab("main"),
            corner_radius=6,
            font=("Courier", 13, "bold")
        )

    def show_items(self):
        self.help_photo_label.place(x=20, y=70)
        for i, label in enumerate(self.labels):
            label.place(x=self.places[i][0], y=self.places[i][1])
        self.calculator_tab_button.place(x=185, y=560)