from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_keyboard():
    markup = InlineKeyboardMarkup()
    questionnaire_button = InlineKeyboardButton(
        'Questionnaire❔',
        callback_data='start_questionnaire'
    )
    registration_button = InlineKeyboardButton(
        'Registration 📝',
        callback_data='registration'
    )
    my_profile_button = InlineKeyboardButton(
        'My Profile 🪪',
        callback_data='my_profile_call'
    )
    random_profile_button = InlineKeyboardButton(
        'Random Profiles 🗂️',
        callback_data='random_profile_call'
    )
    markup.add(questionnaire_button)
    markup.add(my_profile_button)
    markup.add(registration_button)
    markup.add(random_profile_button)
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


async def like_dislike_keyboard(owner_tg_id):
    markup = InlineKeyboardMarkup()
    like_button = InlineKeyboardButton(
        'Like 👍',
        callback_data=f'liked_profile_{owner_tg_id}'
    )
    dislike_button = InlineKeyboardButton(
        'Dislike 👎',
        callback_data=f'random_profiles'
    )
    markup.add(like_button)
    markup.add(dislike_button)
    return markup


async def my_profile_keyboard():
    markup = InlineKeyboardMarkup()
    update_button = InlineKeyboardButton(
        'UPDATE 👤',
        callback_data=f'update'
    )
    delete_button = InlineKeyboardButton(
        'DELETE 🫥',
        callback_data=f'delete'
    )
    markup.add(update_button)
    markup.add(delete_button)
    return markup
