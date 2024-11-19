import sqlite3


class DBManager:
    def __init__(self, url: str, language_pack: dir):
        self.conn = sqlite3.connect(url)
        self.cursor = self.conn.cursor()
        self.__init_db()
        self.text = language_pack
        self.max_index = 0

    def __init_db(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS health_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sex TEXT NOT NULL,
            height INTEGER NOT NULL,
            weight INTEGER NOT NULL,
            age INTEGER NOT NULL,
            BMI REAL,
            BMR REAL
        );
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def set_language_pack(self, language_pack: dir):
        self.text = language_pack

    def get_data(self) -> tuple:
        self.cursor.execute("SELECT sex, height, weight, age, BMI, BMR FROM health_data")
        data = self.cursor.fetchall()
        return data

    def write_data(self, data: tuple) -> None:
        insert_query = """
        INSERT INTO health_data (sex, height, weight, age, BMI, BMR)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        self.cursor.execute(insert_query, data)
        self.conn.commit()


    def __str__(self):
        data = self.get_data()

        string = "id  " + self.text['sex'].ljust(6)[:6] + self.text['height'].ljust(7)[:7]
        string += self.text['weight'].ljust(7)[:7] + self.text['age'].ljust(8)[:8] + "BMI".ljust(8) + "BMR" + "\n"
        self.max_index= len(data) + 1
        for indx, row in enumerate(reversed(data)):
            string += str(self.max_index - indx).ljust(4)

            string += row[0].ljust(9)[:9]
            string += str(row[1]).ljust(6)
            string += str(row[2]).ljust(6)
            string += str(row[3]).ljust(6)
            string += str(round(row[4],2)).ljust(8)
            string += str(round(row[5],2)).ljust(6)
            """for i in row:
                try:
                    string += str(round(i,2)).ljust(6)[:7]
                except TypeError:
                    string += i.ljust(7)[:7]"""

            string += "\n"


        return string


    def delete_data(self) -> None:
        delete_query = "DELETE FROM health_data;"
        self.cursor.execute(delete_query)
        self.__init_db()


    def get_last_record(self) -> str:
        self.cursor.execute("SELECT sex, height, weight, age, BMI, BMR FROM health_data ORDER BY id DESC LIMIT 1;")
        row = self.cursor.fetchone()

        string = ""
        string += str(self.max_index + 1).ljust(4)
        string += row[0].ljust(9)[:9]
        string += str(row[1]).ljust(6)
        string += str(row[2]).ljust(6)
        string += str(row[3]).ljust(6)
        string += str(round(row[4], 2)).ljust(8)
        string += str(round(row[5], 2)).ljust(6)
        string += "\n"
        self.max_index += 1
        return string



