import sqlite3


class db_manager:
    def __init__(self, url: str):
        self.conn = sqlite3.connect(url)
        self.cursor = self.conn.cursor()
        self.__init_db()

    def __init_db(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS health_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sex TEXT NOT NULL,
            height REAL NOT NULL,
            weight REAL NOT NULL,
            age INTEGER NOT NULL,
            BMI REAL,
            BMR REAL
        );
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()


    def get_data(self) -> tuple:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM health_data")
        data = cursor.fetchall()
        return data

    def write_data(self, data: tuple) -> None:
        cursor = self.conn.cursor()
        insert_query = """
        INSERT INTO health_data (sex, height, weight, age, BMI, BMR)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        cursor.execute(insert_query, data)

    def __list__(self):
        data = self.get_data()
        data_str_list = []
        for row in data:
            pass



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
