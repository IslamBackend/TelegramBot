from config import bot
from aiogram import types, Dispatcher
from database.sql_commands import DataBase
from aiogram.utils.deep_linking import _create_link
import os
import binascii
from const import REFERENCE_MENU_TEXT
from keyboards.inline_buttons import referral_keyboard


async def reference_menu_call(call: types.CallbackQuery):
    db = DataBase()
    data = db.sql_select_referral_menu_info(
        owner=call.from_user.id
    )
    await bot.send_message(
        chat_id=call.from_user.id,
        text=REFERENCE_MENU_TEXT.format(
            user=call.from_user.first_name,
            balance=data['balance'],
            total=data['total_referrals']
        ),
        reply_markup=await referral_keyboard()
    )


async def generate_link(call: types.CallbackQuery):
    db = DataBase()
    user = db.sql_select_user(tg_id=call.from_user.id)
    if not user['link']:
        token = binascii.hexlify(os.urandom(8)).decode()
        link = await _create_link('start', payload=token)
        print(link)
        db.sql_update_like(
            tg_id=call.from_user.id,
            link=link
        )
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'Here is your new link {user["link"]}',
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'Here is your old link {user["link"]}',
        )

def register_reference_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        reference_menu_call,
        lambda call: call.data == 'reference_menu'
    )
    dp.register_callback_query_handler(
        generate_link,
        lambda call: call.data == 'generate_link'
    )