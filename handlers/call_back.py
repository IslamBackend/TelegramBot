import sqlite3

from aiogram import types, Dispatcher
from config import bot
from database.sql_commands import DataBase
from keyboards.inline_buttons import questionnaire_keyboard


async def start_questionnaire_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Your favorite anime?',
        reply_markup=await questionnaire_keyboard()
    )


async def first_card(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='You are ONE-PIECE fan 👑',
    )
    await save_answer(call)


async def second_card(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='You are NARUTO fan 🦊',
    )
    await save_answer(call)


async def save_answer(call: types.CallbackQuery):
    db = DataBase()
    db.sql_insert_answers(
        telegram_id=call.message.chat.id,
        answer=call.data
    )
    print(call.data)


def register_call_back_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_questionnaire_call,
                                       lambda call: call.data == 'start_questionnaire')
    dp.register_callback_query_handler(first_card,
                                       lambda call: call.data == 'first')
    dp.register_callback_query_handler(second_card,
                                       lambda call: call.data == 'second')
