import sqlite3



def take_cursor():
    connection = sqlite3.connect("data/base.db")
    return connection.cursor()

def create_table():
    cursor = take_cursor()
    cursor.execute("""
    CREATE TABLE 
    """)

def read_history()-> list:
    cursor = take_cursor()
    cursor.execute("SELECT * FROM bmi_table")
