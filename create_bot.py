from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config_tg.config import tg_bot_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot, storage=storage)


