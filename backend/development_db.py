import datetime
import sqlite3
from threading import Lock


class Singleton(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DevSQLite(metaclass=Singleton):
    """
    Класс, в который инкапсулированы и/или определены необходимые поля и
    методы для разработки web-приложения
    с перспективой дальнейшего перехода на PostgreSQL.
    """

    def __init__(self, name_db: str) -> None:
        self.name_db = name_db

    def create_table(self):
        connection = sqlite3.connect(self.name_db)
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                track_name TEXT NOT NULL,
                description TEXT,
                author TEXT,
                type TEXT NOT NULL,
                start_point TEXT NOT NULL,
                end_point TEXT NOT NULL,
                route_distance TEXT,
                speed TEXT,
                time TEXT
            )"""
        )
        cursor.close()
        connection.close()

    def create_record(self):
        connection = sqlite3.connect(self.name_db)
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO test_table (
                username, email, age
            ) VALUES (?, ?, ?)""",
            ('newuser', 'newuser@example.com', 28)
        )
        cursor.close()
        connection.commit()
        connection.close()

    def get_record(self):
        connection = sqlite3.connect(self.name_db)
        cursor = connection.cursor()
        cursor.execute("""SELECT * from test_table;""")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return users


def test():
    db = DevSQLite(name_db="test.db")
    db2 = DevSQLite(name_db="test2.db")
    assert id(db) == id(db2), "DB instance uqual failed"

    print(datetime.datetime.now())
    db.create_table()
    print(datetime.datetime.now())


if __name__ == "__main__":
    test()
