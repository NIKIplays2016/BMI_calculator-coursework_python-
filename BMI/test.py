from modules.db_control import DBManager
from json import load


def get_language_pack():
    global language_pack
    global text
    with open("data/language_pack.json", "r", encoding="utf-8") as jsfile:
        language_pack = load(jsfile)
        text = language_pack[language_pack["language"]]

get_language_pack()

db_manager = DBManager("data/base.db", text)


for i in range(20):
    db_manager.write_data(("woman", 161, 23, 32, 23, 43))
print(db_manager.get_data())