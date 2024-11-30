from tkinter import Entry, Label

class Human:
    def __init__(self, height: float, weight: float, age: int, sex: str) -> None:
        try:
            self.height = float(height)
        except:
            raise TypeError("Рост должен быть числом")
        if self.height <= 0:
           raise ValueError("Рост должен быть более 0 см")


        try:
            self.weight = float(weight)

        except:
            raise TypeError("Вес должен быть числом")
        if self.weight <= 0:
            raise ValueError("Вес должен быть более 0 кг")


        try:
            self.age = int(age)
        except:
            raise TypeError("Возраст должен быть числом")
        if self.age <= 0:
            raise ValueError("Возраст должен быть более 0 лет")


        if sex == "man" or sex == "woman":
            self.sex = sex
        else:
            raise ValueError("Error in class human with 'sex'")

        self.bmr = self.__calculate_bmr()
        self.bmi = self.__calculate_bmi()
        self.ideal_weight = self.__calculate_ideal_weight()

    def __calculate_bmr(self):
        if self.sex == "man":
            bmr = 88.36 + (13.4 * self.weight) + (4.8 * self.height) - (5.7 * self.age)
        else:
            bmr = 447.6 + (9.2 * self.weight) + (3.1 * self.height) - (4.3 * self.age)
        return round(bmr, 2)

    def __calculate_bmi(self):
        return round(self.weight / ((self.height/100)**2), 2)

    def __calculate_ideal_weight(self):
        if self.sex == "man":
            return round(0.9 * (self.height - 100) + (self.age / 10), 1)
        else:
            return round(0.9 * (self.height - 100) + (self.age / 10) * 0.9, 1)

    def __str__(self):
        return f"sex: {self.sex}, height: {self.height}, weight: {self.weight}, age: {self.age}, BMI:{self.bmi}, BMR: {self.bmr}"

    def get_data(self):
        return (self.sex, self.height, self.weight, self.age, self.bmi, self.bmr)

"""
def layout(height_entry: Entry, weight_entry: Entry, label: Label, comment_label: Label) -> float:
    global height
    try:
        height = float(height_entry.get())
        if height <= 0:
            raise ValueError
    except (TypeError, ValueError) as e:
        if isinstance(e, TypeError):
            return 0
        else:
            return 0

    try:
        weight = float(weight_entry.get())
        if weight <= 0:
            raise ValueError
    except (TypeError, ValueError) as e:
        if isinstance(e, TypeError):
            return 0
        else:
            return 0

    label.config(text=f"BMI: {round(calculate(height, weight),2)}")
    comment_label.config(text="GOOD, bib bob pop lop top bop")

def calculate(height: float, weight: float, age: int, sex: str) -> float:
    
    

    if sex == "m":
        bmr = 88.36 + (13.4 * weight) + (4.8*height) - (5.7 * age)
    elif sex == "w":
        bmr = 0
    else:
        raise ValueError()


    return weight / ((height/100) ** 2)

"""
