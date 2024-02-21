import sqlite3

from aiogram.utils.deep_linking import _create_link
from aiogram import types, Dispatcher
from config import bot, DESTINATION
from const import START_MENU
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

    command = message.get_full_command()

    if command[1] != '':
        link = await _create_link('start', payload=command[1])
        owner = db.sql_select_user_by_link(
            link=link
        )
        if owner['telegram_id'] == message.from_user.id:
            await bot.send_message(
                chat_id=message.from_user.id,
                text='You can not use own link!!!'
            )
            return
        try:
            db.sql_insert_referral(
                owner=owner['telegram_id'],
                referral=message.from_user.id
            )
            db.sql_update_balance(
                owner=owner['telegram_id']
            )
        except sqlite3.IntegrityError:
            pass

    with open(DESTINATION + 'bot_ava.jpg', "rb") as photo:
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=photo,
            caption=START_MENU.format(
                user=message.from_user.first_name),
            reply_markup=await start_keyboard()
        )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
