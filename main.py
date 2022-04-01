import requests
from aiogram.utils import executor

import data_base
from create_bot import dp, storage
from data_base import sqlite_db



# проверка
#1231231232
#1231231232
#1231231232
#1231231232
#1231231232
#1231231232
#1231231232

async def on_startup(_):
    print("Бот вышел в онлайн")
    sqlite_db.sql_start()


# Импорт хендлеров и хендлеров МШ
from handlers import client

client.register_handlers_client(dp)



if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
