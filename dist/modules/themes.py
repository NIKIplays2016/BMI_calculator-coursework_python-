import json
from tkinter import *
from tkinter import Label
from json import load, dump

def get_themes_settings() -> dict:
    with open("data/themes.json", "r") as jsfile:
        themes_settings = load(jsfile)
    return themes_settings

def save_themes_settings(settings: dict) -> None:
    with open("data/themes.json", "w") as jsfile:
        dump(settings, jsfile, indent=4)


def change_themes(mode: str, window: Tk) -> None:
    themes_settings = get_themes_settings()

    text_color = themes_settings['mode'][mode]['text-color']
    window_color = themes_settings['mode'][mode]['window-color']

    for widget in window.winfo_children():
        if isinstance(widget, Label):
            widget.config(fg=text_color, bg=window_color)

    window.config(bg=window_color)
    themes_settings['now_mode'] = mode
    save_themes_settings(themes_settings)