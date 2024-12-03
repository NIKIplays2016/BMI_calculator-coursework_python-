from tkinter import *
from customtkinter import CTkButton
from PIL import Image, ImageTk
import sys


class TitleTab:
    def __init__(self, tab: Tk, font: dict, main_app):
        self.tab = tab
        self.font = font
        self.main_app = main_app
        self.inactivity_time = 60000  # 60 секунд
        self.inactivity_timer = None
        self.reset_inactivity_timer()

        # Отслеживание активности пользователя
        self.tab.bind_all("<Any-KeyPress>", self.reset_inactivity_timer)
        self.tab.bind_all("<Motion>", self.reset_inactivity_timer)

        img = Image.open("image/logo.png").convert("RGBA")

        percent = 30
        width, height = img.size
        new_width = int(width * percent / 100)
        new_height = int(height * percent / 100)

        # Изменяем размер изображения
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        self.logo_photo = ImageTk.PhotoImage(resized_img)

        self.__create_item()

    def __create_item(self):
        self.plases = [[10, 30], [15, 50], [10, 70], [150, 170], [70, 200], [85, 230], [5, 480], [5, 500], [5, 530],
                       [5, 550], [200, 600]]
        self.labels = [Label(
            self.tab,
            text="Белорусский Национальный Технический Университет",
            font=("Courier", 11, "bold")
        ),

            Label(
                self.tab,
                text="Факультет информационных технологий и робототехники",
                font=("Courier", 10, "bold")
            ),

            Label(
                self.tab,
                text="Кафедра программного обеспечения информационных систем и технологий",
                font=("Courier", 8, "bold")
            ),

            Label(
                self.tab,
                text="Курсовая работа",
                font=("Courier", 13, "bold")
            ),

            Label(
                self.tab,
                text="по дисциплине 'Языки программирования'",
                font=("Courier", 11, "bold")
            ),
            Label(
                self.tab,
                text="Калькулятор индекса массы тела",
                font=("Courier", 12, "bold")
            ),

            Label(
                self.tab,
                text="Выполнил: студент группы 10701323",
                font=("Courier", 11, "bold")
            ),

            Label(
                self.tab,
                text="Шаплавский Никита Сергеевич",
                font=("Courier", 11, "bold")
            ),

            Label(
                self.tab,
                text="Преподаватель: к.ф.-м.н., доц.",
                font=("Courier", 11, "bold")
            ),

            Label(
                self.tab,
                text="Сидорик Валерий Владимирович",
                font=("Courier", 11, "bold")
            ),

            Label(
                self.tab,
                text="Минск 2024",
                font=("Courier", 11, "bold")
            )]
        self.logo_photo_label = Label(image=self.logo_photo)
        self.calculator_tab_button = CTkButton(
            self.tab,
            width=70,
            height=50,
            text="Перейти в калькулятор",
            command=lambda: self.main_app.choese_tab("main"),
            corner_radius=6,
            font=("Courier", 13, "bold")
        )

        self.exit_button = CTkButton(
            self.tab,
            width=70,
            height=50,
            text="Выйти",
            command=self.close_app_due_to_inactivity,
            corner_radius=6,
            font=("Courier", 13, "bold")
        )

    def show_items(self):
        for i,label in enumerate(self.labels):
            label.place(x=self.plases[i][0], y=self.plases[i][1])

        self.calculator_tab_button.place(x=220, y=550)
        self.exit_button.place(x=50, y=550)
        self.reset_inactivity_timer()
        self.logo_photo_label.place(x=180, y=270)

    def reset_inactivity_timer(self, event=None):
        if self.inactivity_timer:
            self.tab.after_cancel(self.inactivity_timer)
        self.inactivity_timer = self.tab.after(self.inactivity_time, self.close_app_due_to_inactivity)

    def close_app_due_to_inactivity(self):
        if self.main_app.check_tittle:  # Проверка, что активен title tab
            sys.exit()

