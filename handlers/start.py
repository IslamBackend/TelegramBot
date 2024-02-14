import sqlite3
from profanity_check import predict_prob
from aiogram import types, Dispatcher
from config import bot
from database.sql_commands import DataBase
from keyboards.inline_buttons import start_keyboard


async def start_button(message: types.Message):
    db = DataBase()
    print(message)
    try:
        db.sql_insert_users(
            telegram_id=message.from_user.id,
            user_name=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
    except sqlite3.IntegrityError:
        pass

    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Здравствуйте, {message.from_user.first_name} !!!",
        reply_markup=await start_keyboard()
    )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
