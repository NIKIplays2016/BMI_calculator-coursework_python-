from tkinter import Entry, Label

class Human:
    def __init__(self, height: float, weight: float, age: int, sex: str, text: dir) -> None:
        try:
            self.height = float(height)
        except:
            raise TypeError(f"{text['height']} {text['ex_num']}")
        if self.height <= 0:
           raise ValueError(f"{text['height']} {text['ex_min']}")


        try:
            self.weight = float(weight)

        except:
            raise TypeError(f"{text['weight']} {text['ex_num']}")
        if self.weight <= 0:
            raise ValueError(f"{text['weight']} {text['ex_min']}")


        try:
            self.age = int(age)
        except:
            raise TypeError(f"{text['age']} {text['ex_num']}")
        if self.age <= 0:
            raise ValueError(f"{text['age']} {text['ex_min']}")


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
