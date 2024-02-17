import aiogram.utils.exceptions
from aiogram import types, Dispatcher
from aiogram.types import ContentTypes

from config import bot, DESTINATION
from const import USER_FORM_TEXT
from database.sql_commands import DataBase
from keyboards.inline_buttons import questionnaire_keyboard, my_profile_keyboard
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    nickname = State()
    biography = State()
    location = State()
    gender = State()
    age = State()
    photo = State()


async def registration_user_start(call: types.CallbackQuery):
    db = DataBase()
    is_registered = db.sql_select_user_form(
        call.from_user.id
    )
    print(is_registered)
    if is_registered:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='You are already registered. \n'
                 'Would you like to update your profile or delete?',
            reply_markup=await my_profile_keyboard()
        )

    else:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Please send me your nickname'
        )
        await RegistrationStates.nickname.set()


async def load_nickname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your biography'
    )
    await RegistrationStates.next()


async def load_biography(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['biography'] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your location'
    )
    await RegistrationStates.next()


async def load_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your gender'
    )
    await RegistrationStates.next()


async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your age (Only integer)'
    )
    await RegistrationStates.next()


async def load_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Please start registration again!'
        )
        await state.finish()
        return
    async with state.proxy() as data:
        data['age'] = age
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Send me your photo'
    )
    await RegistrationStates.next()


async def load_photo(message: types.Message, state: FSMContext):
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
                    nickname=data['nickname'],
                    biography=data['biography'],
                    location=data['location'],
                    gender=data['gender'],
                    age=data['age']
                )
            )
            db.sql_insert_user_form_registration(
                telegram_id=message.from_user.id,
                nickname=data['nickname'],
                biography=data['biography'],
                location=data['location'],
                gender=data['gender'],
                age=data['age'],
                photo=path.name
            )
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Registration successfully ✅'
        )
        await state.finish()


def register_registration_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        registration_user_start, lambda call: call.data == 'registration'
    )
    dp.register_message_handler(
        load_nickname, state=RegistrationStates.nickname, content_types=ContentTypes.TEXT
    )
    dp.register_message_handler(
        load_biography, state=RegistrationStates.biography, content_types=ContentTypes.TEXT
    )
    dp.register_message_handler(
        load_location, state=RegistrationStates.location, content_types=ContentTypes.TEXT
    )
    dp.register_message_handler(
        load_gender, state=RegistrationStates.gender, content_types=ContentTypes.TEXT
    )
    dp.register_message_handler(
        load_age, state=RegistrationStates.age, content_types=ContentTypes.TEXT
    )
    dp.register_message_handler(
        load_photo, state=RegistrationStates.photo, content_types=ContentTypes.PHOTO
    )
