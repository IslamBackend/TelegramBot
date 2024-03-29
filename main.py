from aiogram import executor
from config import dp
from database import sql_commands
from handlers import (
    start, call_back, chat_actions, registration, profile, reference
)


async def on_startup(_):
    db = sql_commands.DataBase()
    db.sql_create_tables()


start.register_start_handlers(dp=dp)
call_back.register_call_back_handlers(dp=dp)
registration.register_registration_handlers(dp=dp)
profile.register_profile_handlers(dp=dp)
reference.register_reference_handlers(dp=dp)
chat_actions.register_chat_actions_handlers(dp=dp)


if __name__ == '__main__':
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )
