from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_keyboard():
    markup = InlineKeyboardMarkup()
    questionnaire_button = InlineKeyboardButton(
        'ANIME QUESTIONNAIRE',
        callback_data='start_questionnaire'
    )
    markup.add(questionnaire_button)
    return markup


async def questionnaire_keyboard():
    markup = InlineKeyboardMarkup()
    first_button = InlineKeyboardButton(
        'ONE-PIECE 👑',
        callback_data='first'
    )
    second_button = InlineKeyboardButton(
        'NARUTO 🦊',
        callback_data='second'
    )
    markup.add(first_button)
    markup.add(second_button)
    return markup
