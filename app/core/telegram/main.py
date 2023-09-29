from .client import TgClient
from .bot import TgBot
from aiogram import Dispatcher

client = TgClient()
bot = TgBot()
dp = Dispatcher(bot)