import random
import sqlite3

import aiogram.utils.exceptions
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentTypes

from config import bot, DESTINATION
from const import USER_FORM_TEXT
from database.sql_commands import DataBase
from keyboards.inline_buttons import *
import re


async def my_profile_call(call: types.CallbackQuery):
    db = DataBase()
    profile = db.sql_select_user_form(
        telegram_id=call.from_user.id
    )
    try:
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
                ),
                reply_markup=await my_profile_keyboard()
            )
    except TypeError:
        pass


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


async def delete_profile_call(call: types.CallbackQuery):
    db = DataBase()
    db.sql_delete_user_form(
        call.from_user.id
    )
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Your profile deleted successfully!'
    )


class UpdateProfileStates(StatesGroup):
    nickname = State()
    biography = State()
    location = State()
    gender = State()
    age = State()
    photo = State()


async def update_profile_start(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Please send me your updated nickname'
    )
    await UpdateProfileStates.nickname.set()


async def load_updated_nickname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['updated_nickname'] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your updated biography'
    )
    await UpdateProfileStates.next()


async def load_updated_biography(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['updated_biography'] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your updated location'
    )
    await UpdateProfileStates.next()


async def load_updated_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['updated_location'] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your updated gender'
    )
    await UpdateProfileStates.next()


async def load_updated_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['updated_gender'] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your updated age'
    )
    await UpdateProfileStates.next()


async def load_updated_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['updated_age'] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your updated photo'
    )
    await UpdateProfileStates.next()


async def load_updated_photo(message: types.Message, state: FSMContext):
    db = DataBase()

    path = await message.photo[-1].download(
        destination_dir=DESTINATION
    )
    async with state.proxy() as data:
        with open(path.name, "rb") as photo:
            await bot.send_photo(
                chat_id=message.from_user.id,
                photo=photo,
                caption=USER_FORM_TEXT.format(
                    nickname=data['updated_nickname'],
                    biography=data['updated_biography'],
                    location=data['updated_location'],
                    gender=data['updated_gender'],
                    age=data['updated_age']
                )
            )
            db.sql_update_user_form(
                telegram_id=message.from_user.id,
                nickname=data['updated_nickname'],
                biography=data['updated_biography'],
                location=data['updated_location'],
                gender=data['updated_gender'],
                age=data['updated_age'],
                photo=path.name
            )
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Profile updated successfully ✅'
        )
        await state.finish()


def register_profile_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        my_profile_call,
        lambda call: call.data == 'my_profile_call'
    )
    dp.register_callback_query_handler(
        random_profiles_call,
        lambda call: call.data == 'random_profile_call'
    )
    dp.register_callback_query_handler(
        like_detect_call,
        lambda call: 'liked_profile_' in call.data
    )
    dp.register_callback_query_handler(
        delete_profile_call,
        lambda call: call.data == 'delete'
    )

    dp.register_callback_query_handler(
        update_profile_start, lambda call: call.data == 'update'
    )
    dp.register_message_handler(
        load_updated_nickname, state=UpdateProfileStates.nickname, content_types=ContentTypes.TEXT
    )
    dp.register_message_handler(
        load_updated_biography, state=UpdateProfileStates.biography, content_types=ContentTypes.TEXT
    )
    dp.register_message_handler(
        load_updated_location, state=UpdateProfileStates.location, content_types=ContentTypes.TEXT
    )
    dp.register_message_handler(
        load_updated_gender, state=UpdateProfileStates.gender, content_types=ContentTypes.TEXT
    )
    dp.register_message_handler(
        load_updated_age, state=UpdateProfileStates.age, content_types=ContentTypes.TEXT
    )
    dp.register_message_handler(
        load_updated_photo, state=UpdateProfileStates.photo, content_types=ContentTypes.PHOTO
    )
