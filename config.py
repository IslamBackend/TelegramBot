from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config

storage = MemoryStorage()
BOT_TOKEN = config('TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
DESTINATION = config('DESTINATION')
ADMIN_ID = config("ADMIN_ID")
SECRET_WORD = config("SECRET_WORD")

