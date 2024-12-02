from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

from customtkinter import CTkButton

from sys import exit
import sqlite3
from json import load, dump
import os
from PIL import Image, ImageTk
import ctypes

from modules.calculation import Human
from modules.themes import get_themes_settings, change_themes
from modules.db_control import DBManager

from my_tabs.tittle_tab import TitleTab
from my_tabs.help_tab import HelpTab
from my_tabs.about_tab import AboutTab



# Установка фиксированного DPI для приложения
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # DPI_AWARENESS_CONTEXT_SYSTEM_AWARE
except Exception:
    pass

def get_language_pack():
    global language_pack
    global text
    with open("data/language_pack.json", "r", encoding="utf-8") as jsfile:
        language_pack = load(jsfile)
        text = language_pack[language_pack["language"]]

get_language_pack()

db_manager = DBManager("data/base.db", text)


def save_language_pack(lang_pack):
    with open("data/language_pack.json", "w", encoding="utf-8") as jsfile:
        dump(lang_pack, jsfile, indent=4)

def change_bmr_label(height: str, weight: str, age: str, sex: str, bmr_label: Label,
                     bmi_label:Label, bmi_comment_label: Label, error_label: Label,
                     text_box: Text, ideal_weight_label: Label):
    bmi_label.config(text="")
    bmr_label.config(text="")
    bmi_comment_label.config(text="")
    error_label.config(text="")
    ideal_weight_label.config(text="")
    try:
        sex = text[sex]
    except KeyError:
        error_label.config(text=text["ex_empty"])
        return 0

    try:
        human = Human(height, weight, age, sex, text)
        bmr_label.config(text=f"BMR:{human.bmr}")
        bmi_label.config(text=f"BMI:{human.bmi}")
        check = True
        for i in text['bmi_comment']:
            if human.bmi <= i[0]:
                bmi_comment_label.config(text=i[1].rjust(15))
                check = False
                break
        if check:
            bmi_comment_label.config(text=(text['bmi_comment'][6][1]).rjust(15))

        ideal_weight_label.config(text=f"{(text['ideal_weight']).rjust(12)}:{human.ideal_weight}")
    except ValueError as ex:
        error_label.config(text=ex)
        return 0
    except TypeError as ex:
        error_label.config(text=ex)
        return 0
    db_manager.write_data((sex, height, weight, age, human.bmi, human.bmr))
    text_box.insert('3.0', db_manager.get_last_record())
    #text_box.delete("2.0", "3.0")
    """
    first_line = text_box.get("1.0", "2.0").strip()  

   
    
    text_box.insert("1.0", first_line + "\n")
    
    text_box.insert("2.0", text + "\n")"""

class MainTab():
    def __init__(self, tab: Tk, font: dict) -> None:
        """
        Initialization main frame,
        """
        self.tab = tab
        self.font = font
        self.tooltip = None

        self.__create_item()

    def __create_item(self):
        self.label_arr = []       #Список для сбора всех Label
        self.label_place_arr = [] #Список для сбора расположения Label

        self.label_arr.append(Label(self.tab, text="BMI", font=self.font["h1"]))
        self.label_place_arr.append([220, 30])


        self.label_arr.append(Label(self.tab, text=(text["height"])[:6], font=self.font["p"]))
        self.label_place_arr.append([136, 100])
        self.height_entry = Entry(self.tab, width=8)
        self.height_entry.bind("<Enter>", lambda e: self.show_tooltip(e, text["cm_help"]))
        self.height_entry.bind("<Leave>", lambda e: self.hide_tooltip())

        self.label_arr.append(Label(self.tab, text=(text["age"])[:7], font=self.font["p"]))
        self.label_place_arr.append([293,100])
        self.age_entry = Entry(self.tab, width=9)
        self.age_entry.bind("<Enter>", lambda e: self.show_tooltip(e, text["age_help"]))
        self.age_entry.bind("<Leave>", lambda e: self.hide_tooltip())


        self.label_arr.append(Label(self.tab, text=(text["weight"])[:6], font=self.font["p"]))
        self.label_place_arr.append([136, 170])
        self.weight_entry = Entry(self.tab, width=8)
        self.weight_entry.bind("<Enter>", lambda e: self.show_tooltip(e, text["kg_help"]))
        self.weight_entry.bind("<Leave>", lambda e: self.hide_tooltip())

        self.label_arr.append(Label(self.tab, text=(text["sex"])[:6], font=self.font["p"]))
        self.label_place_arr.append([293, 170])
        self.sex_combobox = ttk.Combobox(self.tab, values=[text["man"], text["woman"]], state="readonly", width=7)

        self.bmr_label = Label(self.tab, font=self.font["h3"])
        self.bmi_label = Label(self.tab, font=self.font["h3"])
        self.bmi_comment_label = Label(self.tab, font=self.font["h4"])
        self.ideal_weight_label = Label(self.tab, font=self.font["h3"])

        self.error_label = Label(self.tab, font=self.font["h3"])

        self.calculate_button = CTkButton(
            self.tab,
            height=40,
            width=120,
            #fg_color="#dcdcdc",
            text=text["calculate"],
            command=lambda: change_bmr_label(
                self.height_entry.get(), self.weight_entry.get(),
                self.age_entry.get(), self.sex_combobox.get(),
                self.bmr_label, self.bmi_label, self.bmi_comment_label,
                self.error_label, self.text_box, self.ideal_weight_label
            ),
            corner_radius=6
        )


        self.label_arr.append(Label(self.tab, text=text["History"], font=self.font["h3"]))
        self.label_place_arr.append([18, 400])

        self.scrollbar = Scrollbar(self.tab, width=18, orient=VERTICAL)
        self.text_box = Text(self.tab, font=self.font["h4"], width=44, height=12, yscrollcommand=self.scrollbar.set)
        self.text_box.pack_propagate(False)

        self.clear_text_box_button = CTkButton(
            self.tab,
            height=20,
            width=60,
            #background="#cb8787",
            text=text["Clear"],
            command=self.clear_text_box_button,
            corner_radius=6
        )

        self.scrollbar.config(command=self.text_box.yview)



        self.text_box.insert('1.0', str(db_manager))

    def show_tooltip(self, event, text):
        self.tooltip = Toplevel(self.tab)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        label = Label(self.tooltip, text=text, relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def show_items(self):
        for i, item in enumerate(self.label_arr):
            item.place(x=self.label_place_arr[i][0], y=self.label_place_arr[i][1])

        self.height_entry.place(x=140, y=130)
        self.age_entry.place(x=297, y=130)
        self.weight_entry.place(x=140, y=200)
        self.sex_combobox.place(x=297,y=200)

        self.bmr_label.place(x=180, y=283)
        self.bmi_label.place(x=180, y=313)
        self.bmi_comment_label.place(x=140, y=340)
        self.ideal_weight_label.place(x=140, y=370)

        self.error_label.place(x=140, y=285)
        self.calculate_button.place(x=160,y=205)#(x=200, y=380)

        #self.scrollbar.place(x=483, y=440.1)
        self.clear_text_box_button.place(x=354, y=355)
        self.text_box.place(x=6, y=435)

    def clear_text_box_button(self):
        self.text_box.delete("1.0", END)
        db_manager.delete_data()
        self.text_box.insert('1.0', str(db_manager))


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


#######
class MainApp:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("500x700")
        self.window.resizable(False, False)
        self.window.title("BMI")

        self.themes_settings = get_themes_settings()
        self.font = self.themes_settings['font']

        self.check_tittle = True

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

        self.title_tab = TitleTab(self.window, self.font, self)
        self.about_tab = AboutTab(self.window, self.font, text, self)
        self.help_tab = HelpTab(self.window, self.font, text, self)

        #self.main_tab.show_items()
        self.title_tab.show_items()
        self.create_main_app()

        change_themes(self.themes_settings['now_mode'], self.window)

    def create_main_app(self):
        self.button_change_app = Button(
            self.window,
            image=self.bool_dict_image[True],
            command=self.change_app
        )
        self.title_button = CTkButton(
            self.window,
            height=10,
            width=45,
            text=text["menu"],
            command=self.open_title,
            corner_radius=0,
            font=tuple(self.font["h4"])
        )
        self.about_autor_button = CTkButton(
            self.window,
            height=10,
            width=45,
            text=text["about"],
            command=self.open_about,
            corner_radius=0,
            font=tuple(self.font["h4"])
        )
        self.help_button = CTkButton(
            self.window,
            height=10,
            width=45,
            text=text["help"],
            command=self.open_help,
            corner_radius=0,
            font=tuple(self.font["h4"])
        )

    def update_themes_settings(self):
        self.themes_settings = get_themes_settings()

    def reboot(self):
        self.hide_widgets()
        del self.main_tab
        del self.setting_tab
        del self.about_tab
        del self.help_tab


        get_language_pack()
        db_manager.set_language_pack(text)
        self.main_tab = MainTab(self.window, self.font)
        self.setting_tab = SettingsTab(self.window, self.font, self)
        self.title_tab = TitleTab(self.window, self.font, self)
        self.about_tab = AboutTab(self.window, self.font, text, self)
        self.help_tab = HelpTab(self.window, self.font, text, self)

        self.create_main_app()

        self.setting_tab.show_items()
        self.show_main_app()
        self.update_themes_settings()
        change_themes(self.themes_settings['now_mode'], self.window)

    def show_main_app(self):
        self.button_change_app.place(x=430, y=30)

        self.title_button.place(x=0,y=0)
        self.about_autor_button.place(x=47, y=0)
        self.help_button.place(x=94, y=0)

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

    def choese_tab(self, tab_name: str) -> None:
        self.hide_widgets()
        self.show_main_app()
        self.show_main_app()
        self.check_tittle = False
        if tab_name == "main":
            self.main_tab.show_items()
            self.bool_check_app = True
            self.button_change_app.config(image=self.bool_dict_image[self.bool_check_app])
        elif tab_name == "settings":
            self.setting_tab.show_items()
            self.bool_check_app = False
            self.button_change_app.config(image=self.bool_dict_image[self.bool_check_app])
        else:
            raise NameError

    def open_title(self):
        self.check_tittle = True
        self.hide_widgets()
        self.title_tab.show_items()

    def open_about(self):
        self.hide_widgets()
        self.about_tab.show_items()

    def open_help(self):
        self.hide_widgets()
        self.help_tab.show_items()

    def loop(self):
        self.window.mainloop()

main_app = MainApp()
main_app.loop()
