from tkinter import *
from tkinter import ttk

import sqlite3
from json import load, dump
from PIL import Image, ImageTk

from modules.calculation import Human
from modules.themes import get_themes_settings, change_themes

def get_language_pack():
    global language_pack
    global text
    with open("data/language_pack.json", "r", encoding="utf-8") as jsfile:
        language_pack = load(jsfile)
        text = language_pack[language_pack["language"]]

get_language_pack()

def save_language_pack(lang_pack):
    with open("data/language_pack.json", "w", encoding="utf-8") as jsfile:
        dump(lang_pack, jsfile, indent=4)

def change_bmr_label(height: str, weight: str, age: str, sex: str, bmr_label: Label, bmi_label:Label, bmi_comment_label: Label) -> None:
    sex = text[sex]
    human = Human(height, weight, age, sex)
    bmr_label.config(text=f"BMR: {human.bmr}")
    bmi_label.config(text=f"BMI: {human.bmi}")
    for i in text['bmi_comment']:
        if human.bmi <= i[0]:
            bmi_comment_label.config(text=i[1])
            break


class MainTab():
    def __init__(self, tab: Tk, font: dict) -> None:
        """
        Initialization main frame,
        """
        self.tab = tab

        self.font = font

        self.__create_item()

    def __create_item(self):
        self.label_arr = []       #Список для сбора всех Label
        self.label_place_arr = [] #Список для сбора расположения Label

        self.label_arr.append(Label(self.tab, text="BMI", font=self.font["h1"]))
        self.label_place_arr.append([220, 30])


        self.label_arr.append(Label(self.tab, text=text["height:"], font=self.font["p"]))
        self.label_place_arr.append([100, 130])
        self.height_entry = Entry(self.tab, width=8)

        self.label_arr.append(Label(self.tab, text=text["age:"], font=self.font["p"]))
        self.label_place_arr.append([260,130])
        self.age_entry = Entry(self.tab, width=5)


        self.label_arr.append(Label(self.tab, text=text["weight:"], font=self.font["p"]))
        self.label_place_arr.append([100, 200])
        self.weight_entry = Entry(self.tab, width=8)

        self.label_arr.append(Label(self.tab, text=text["sex:"], font=self.font["p"]))
        self.label_place_arr.append([260, 200])
        self.sex_combobox = ttk.Combobox(self.tab, values=[text["man"], text["woman"]], state="readonly", width=5)

        self.bmr_label = Label(self.tab, font=self.font["h3"])
        self.bmi_label = Label(self.tab, font=self.font["h3"])
        self.bmi_comment_label = Label(self.tab, font=self.font["h4"])

        self.error_label = Label(self.tab)


        self.calculate_button = Button(
            self.tab,
            height=2,
            width=12,
            background="#98FB98",
            text=text["calculate"],
            command=lambda: change_bmr_label(
                self.height_entry.get(), self.weight_entry.get(),
                self.age_entry.get(), self.sex_combobox.get(),
                self.bmr_label, self.bmi_label, self.bmi_comment_label
            )
        )

    def show_items(self):
        for i, item in enumerate(self.label_arr):
            item.place(x=self.label_place_arr[i][0], y=self.label_place_arr[i][1])

        self.height_entry.place(x=170, y=130)
        self.age_entry.place(x=340, y=130)
        self.weight_entry.place(x=170, y=200)
        self.sex_combobox.place(x=320,y=200)

        self.bmr_label.place(x=190, y=243)
        self.bmi_label.place(x=190, y=283)
        self.bmi_comment_label.place(x=150, y=310)

        self.calculate_button.place(x=190, y=360)
        self.error_label.place(x=150, y=400)



class SettingsTab():
    def __init__(self, tab: Tk, font: dict, main_app) -> None:
        """
        Initialization settings frame
        """
        self.main_app = main_app
        self.tab = tab
        self.font = font

        light_img = Image.open("image/light_ico.png").convert("RGBA")
        dark_img = Image.open("image/dark_ico.png").convert("RGBA")
        lagoon_img = Image.open("image/lagoon_ico.png").convert("RGBA")

        light_img_resized = light_img.resize((40, 40), Image.Resampling.LANCZOS)
        dark_img_resized = dark_img.resize((40, 40), Image.Resampling.LANCZOS)
        lagoon_img_resized = lagoon_img.resize((40, 40), Image.Resampling.LANCZOS)

        self.light_img = ImageTk.PhotoImage(light_img_resized)
        self.dark_img = ImageTk.PhotoImage(dark_img_resized)
        self.lagoon_img = ImageTk.PhotoImage(lagoon_img_resized)

        self.__create_item()

    def __create_item(self) -> None:
        self.label_arr = [
            Label(self.tab, text=text["change theme:"], font=self.font['h3']),
            Label(self.tab, text=text["light"], font=self.font['p']),
            Label(self.tab, text=text["dark"], font=self.font['p']),
            Label(self.tab, text=text["lagoon"], font=self.font['p']),
            Label(self.tab, text=text["change language"], font=self.font["h3"])
        ]
        self.label_arr_place = [[160, 30], [160, 100], [160, 150], [160, 200], [160, 300]]

        self.button_arr = [
            Button(
                self.tab,
                image=self.light_img,
                command=lambda: change_themes('light', self.tab)
            ),
            Button(
                self.tab,
                image=self.dark_img,
                command=lambda: change_themes('dark', self.tab)
            ),
            Button(
                self.tab,
                image=self.lagoon_img,
                command=lambda: change_themes('lagoon', self.tab)
            )
        ]

        self.button_arr_place = [[250, 90], [250, 140], [250, 190]]

        self.language_combobox = ttk.Combobox(self.tab, values=language_pack["language_list"], state="readonly", width=10)
        self.language_combobox.set(language_pack["language"])
        self.language_combobox.bind("<<ComboboxSelected>>", self.chenge_language)


    def chenge_language(self, event=None):
        lang = self.language_combobox.get()
        language_pack["language"] = lang
        save_language_pack(language_pack)
        self.main_app.reboot()

    def show_items(self):
        for i, item in enumerate(self.label_arr):
            item.place(x=self.label_arr_place[i][0], y=self.label_arr_place[i][1])

        for i, item in enumerate(self.button_arr):
            item.place(x=self.button_arr_place[i][0], y=self.button_arr_place[i][1])

        self.language_combobox.place(x=160, y=350)

##
#######
class MainApp():
    def __init__(self):
        self.window = Tk()
        self.window.geometry("500x700")
        self.window.resizable(False, False)
        self.window.title("BMI")

        self.themes_settings = get_themes_settings()
        self.font = self.themes_settings['font']


        calculator_img = Image.open("image/calculator.png").convert("RGBA")
        settings_img = Image.open("image/settings.png").convert("RGBA")

        calculator_img_resized = calculator_img.resize((35, 35), Image.Resampling.LANCZOS)
        settings_img_resized = settings_img.resize((35, 35), Image.Resampling.LANCZOS)

        image_calculator = ImageTk.PhotoImage(calculator_img_resized)
        image_settings = ImageTk.PhotoImage(settings_img_resized)


        self.font = get_themes_settings()['font']


        self.bool_check_app = True
        self.bool_dict_image = {
            True: image_settings,
            False: image_calculator
        }
        self.main_tab = MainTab(self.window, self.font)
        self.setting_tab = SettingsTab(self.window, self.font, self)

        self.main_tab.show_items()
        self.create_main_app()
        self.show_main_app()

        change_themes(self.themes_settings['now_mode'], self.window)

    def create_main_app(self):
        self.button_change_app = Button(
            self.window,
            image=self.bool_dict_image[True],
            command= self.change_app
        )

    def update_themes_settings(self):
        self.themes_settings = get_themes_settings()

    def reboot(self):
        self.hide_widgets()
        del self.main_tab
        del self.setting_tab
        get_language_pack()
        self.main_tab = MainTab(self.window, self.font)
        self.setting_tab = SettingsTab(self.window, self.font, self)
        self.setting_tab.show_items()
        self.show_main_app()
        self.update_themes_settings()
        change_themes(self.themes_settings['now_mode'], self.window)

    def show_main_app(self):
        self.button_change_app.place(x=430, y=30)

    def loop(self):
        self.window.mainloop()


    def hide_widgets(self):
        # Скрываем все виджеты в окне
        for widget in self.window.winfo_children():
            widget.place_forget()

    def change_app(self):
        self.hide_widgets()
        self.show_main_app()
        if self.bool_check_app:
            self.setting_tab.show_items()
            self.bool_check_app = False
            self.button_change_app.config(image=self.bool_dict_image[self.bool_check_app])
        else:
            self.main_tab.show_items()
            self.bool_check_app = True
            self.button_change_app.config(image=self.bool_dict_image[self.bool_check_app])


main_app = MainApp()
main_app.loop()
