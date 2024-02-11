from aiogram import Dispatcher, Bot
from decouple import config

BOT_TOKEN = config('TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)
