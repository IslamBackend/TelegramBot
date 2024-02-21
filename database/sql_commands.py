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
        self.connection.execute(sql_queries.CREATE_LIKE_TABLE_QUERY)

        self.connection.execute(sql_queries.CREATE_REFERRAL_TABLE_QUERY)
        try:
            self.connection.execute(sql_queries.ALTER_USER_TABLE)
            self.connection.execute(sql_queries.ALTER_USER_V2_TABLE)
        except sqlite3.OperationalError:
            pass

        self.connection.commit()

    def sql_insert_users(self, telegram_id, user_name, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, telegram_id, user_name, first_name, last_name, None, 0)
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

    def sql_select_user_form(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "nickname": row[2],
            "biography": row[3],
            "location": row[4],
            "gender": row[5],
            "age": row[6],
            "photo": row[7],
        }
        return self.cursor.execute(
            sql_queries.SELECT_USER_FORM_QUERY,
            (telegram_id,)
        ).fetchone()

    def sql_insert_like(self, owner, liker):
        self.cursor.execute(
            sql_queries.INSERT_LIKE_QUERY,
            (None, owner, liker)
        )
        self.connection.commit()

    def sql_select_all_user_form(self):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "nickname": row[2],
            "biography": row[3],
            "location": row[4],
            "gender": row[5],
            "age": row[6],
            "photo": row[7],
        }
        return self.cursor.execute(
            sql_queries.SELECT_ALL_USER_FORM_QUERY,
        ).fetchall()

    def sql_select_filter_user_form(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "nickname": row[2],
            "biography": row[3],
            "location": row[4],
            "gender": row[5],
            "age": row[6],
            "photo": row[7],
        }
        return self.cursor.execute(
            sql_queries.FILTER_LEFT_JOIN_USERFORM_LIKE_QUERY,
            (telegram_id, telegram_id,)
        ).fetchall()

    def sql_update_user_form(self, telegram_id, nickname, biography, location, gender, age, photo):
        self.cursor.execute(
            sql_queries.UPDATE_USER_FORM_TABLE_QUERY,
            (nickname, biography, location, gender, age, photo, telegram_id)
        )
        self.connection.commit()

    def sql_delete_user_form(self, telegram_id):
        self.cursor.execute(
            sql_queries.DELETE_USER_FORM_QUERY,
            (telegram_id,)
        )
        self.connection.commit()

    def sql_select_referral_menu_info(self, owner):
        self.cursor.row_factory = lambda cursor, row: {
            "balance": row[0],
            "total_referrals": row[1],
        }
        return self.cursor.execute(
            sql_queries.DOUBLE_SELECT_REFERRAL_USER_QUERY,
            (owner,)
        ).fetchone()

    def sql_select_user(self, tg_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "link": row[5],
            "balance": row[6],
        }
        return self.cursor.execute(
            sql_queries.SELECT_USER_QUERY,
            (tg_id,)
        ).fetchone()

    def sql_update_like(self, link, tg_id):
        self.cursor.execute(
            sql_queries.UPDATE_USER_LINK_QUERY,
            (link, tg_id)
        )
        self.connection.commit()

    def sql_select_user_by_link(self, link):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "link": row[5],
            "balance": row[6],
        }
        return self.cursor.execute(
            sql_queries.SELECT_USER_BY_LINK_QUERY,
            (link,)
        ).fetchone()

    def sql_insert_referral(self, owner, referral):
        self.cursor.execute(
            sql_queries.INSERT_REFERRAL_QUERY,
            (None, owner, referral)
        )
        self.connection.commit()

    def sql_update_balance(self, owner):
        self.cursor.execute(
            sql_queries.UPDATE_USER_BALANCE_QUERY,
            (owner,)
        )
