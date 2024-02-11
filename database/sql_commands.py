import sqlite3
from database import sql_queries


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect('db.sqlite3')
        self.cursor = self.connection.cursor()

    def sql_create_tables(self):
        if self.connection:
            print("База данных успешно подключена!")
        self.connection.execute(sql_queries.CREATE_USER_TABLE_QUERY)

    def sql_insert_users(self, telegram_id, user_name, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, telegram_id, user_name, first_name, last_name)
        )
        self.connection.commit()
