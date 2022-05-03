from aiogram.utils import executor
from create_bot import dp, storage
from data_base import sqlite_db


# ================================== ПРОВЕРКА ВЫХОДА БОТА В РЕЖИМ ON ===============================

async def on_startup(_):
    print("Бот вышел в онлайн")
    sqlite_db.sql_start()


# ============================ ИМПОРТ Хэндлеров и Хэндлеров Машины Состояний =============================

from handlers import client
client.register_handlers_client(dp)

# ========================================= Запуск Бота ===========================================

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
