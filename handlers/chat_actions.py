import datetime

from config import bot
from aiogram import types, Dispatcher
from profanity_check import predict_prob
from database.sql_commands import DataBase


async def chat_messages(message: types.Message):
    db = DataBase()
    print(message)

    if message.chat.id == -4114445207:
        users_word = predict_prob([message.text])
        if users_word >= 0.1:
            await message.delete()

            user = db.sql_select_ban_user(
                telegram_id=message.from_user.id
            )

            await bot.send_message(
                message.chat.id,
                text=f'User: {message.from_user.first_name} watch your words.\n'
                     f'You may get banned !!!'
            )
            count = None
            try:
                count = user['count_warnings']
            except TypeError:
                pass
            if not user:
                db.sql_insert_ban_user(
                    telegram_id=message.from_user.id
                )
            elif count >= 3:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Banned: {message.from_user.first_name}"
                )
                await bot.ban_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    until_date=datetime.datetime.now() + datetime.timedelta(minutes=5)
                )
            elif user:
                db.sql_update_ban_user_count(
                    telegram_id=message.from_user.id
                )
    else:
        await message.reply(
            text="There is no such command"
        )


def register_chat_actions_handlers(dp: Dispatcher):
    dp.register_message_handler(chat_messages)
