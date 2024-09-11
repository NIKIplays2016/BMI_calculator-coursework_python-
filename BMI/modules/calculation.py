from tkinter import Entry, Label

def layout(height_entry: Entry, weight_entry: Entry, label: Label, comment_label: Label) -> float:
    """КАКА"""
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

def calculate(height: float, weight: float) -> float:
    """
    take height(cm) and weight(kg) and calculate BMI
    height > 0, weight > 0
    """

    return weight / ((height/100) ** 2)


