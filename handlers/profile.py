import random
import sqlite3

import aiogram.utils.exceptions
from aiogram import types, Dispatcher

from config import bot
from const import USER_FORM_TEXT
from database.sql_commands import DataBase
from keyboards.inline_buttons import *
import re


async def my_profile_call(call: types.CallbackQuery):
    db = DataBase()
    profile = db.sql_select_user_form(
        telegram_id=call.from_user.id
    )
    with open(profile['photo'], "rb") as photo:
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=USER_FORM_TEXT.format(
                nickname=profile['nickname'],
                biography=profile['biography'],
                location=profile['location'],
                gender=profile['gender'],
                age=profile['age']
            )
        )


async def random_profiles_call(call: types.CallbackQuery):
    if call.message.caption.startswith('Hello'):
        pass
    else:
        try:
            await call.message.delete()
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass

    db = DataBase()
    # profiles = db.sql_select_all_user_form()
    profiles = db.sql_select_filter_user_form(
        telegram_id=call.from_user.id
    )

    if not profiles:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='There is no user user_profiles\n'
                 'or you liked all profiles'
        )
        return

    random_profile = random.choice(profiles)

    with open(random_profile['photo'], "rb") as photo:
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=USER_FORM_TEXT.format(
                nickname=random_profile['nickname'],
                biography=random_profile['biography'],
                location=random_profile['location'],
                gender=random_profile['gender'],
                age=random_profile['age']
            ),
            reply_markup=await like_dislike_keyboard(
                owner_tg_id=random_profile['telegram_id']
            )
        )


async def like_detect_call(call: types.CallbackQuery):
    owner = re.sub('liked_profile_', '', call.data)
    db = DataBase()
    try:
        db.sql_insert_like(
            owner=owner,
            liker=call.from_user.id
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='You like this account!'
        )
    finally:
        await random_profiles_call(call=call)


def register_profile_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        my_profile_call,
        lambda call: call.data == 'liked_profile_'
    )
    dp.register_callback_query_handler(
        random_profiles_call,
        lambda call: call.data == 'random_profile_call'
    )
    dp.register_callback_query_handler(
        like_detect_call,
        lambda call: 'liked_profile_' in call.data
    )
