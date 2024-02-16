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
        self.connection.execute(sql_queries.CREATE_ANSWER_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_BAN_USER_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_USER_FORM_TABLE_QUERY)

        self.connection.commit()

    def sql_insert_users(self, telegram_id, user_name, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, telegram_id, user_name, first_name, last_name)
        )
        self.connection.commit()

    def sql_insert_answers(self, telegram_id, answer):
        self.cursor.execute(
            sql_queries.INSERT_ANSWER_QUERY,
            (telegram_id, answer)
        )
        self.connection.commit()

    def sql_insert_ban_user(self, telegram_id):
        self.cursor.execute(
            sql_queries.INSERT_BAN_USER_TABLE_QUERY,
            (None, telegram_id, 1)
        )
        self.connection.commit()

    def sql_select_ban_user(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "count_warnings": row[2]
        }
        return self.cursor.execute(
            sql_queries.SELECT_BAN_USER_TABLE_QUERY, (telegram_id,)
        ).fetchone()

    def sql_update_ban_user_count(self, telegram_id):
        self.cursor.execute(
            sql_queries.UPDATE_BAN_USER_COUNT_QUERY,
            (telegram_id,)
        )
        self.connection.commit()

    def sql_insert_user_form_registration(self, telegram_id, nickname, biography, location, gender, age, photo):
        self.cursor.execute(
            sql_queries.INSERT_USER_FORM_TABLE_QUERY,
            (None, telegram_id, nickname, biography, location, gender, age, photo)
        )
        self.connection.commit()
