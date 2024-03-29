import keyboards.client_kb
from create_bot import dp, bot

from keyboards import kb_client

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db

import datetime

# *************************************** [НАЧАЛО] ***************************************************

from config_tg.config import debug_mode


# @dp.message_handler(commands=["start", "registration"])

async def start_command(message: types.Message):
    # if str(message.from_user.id) in [i[0] for i in set(sqlite_db.sql_get_user_ids())]:
    if not sqlite_db.sql_is_user_id_in_user_ids(str(message.from_user.id)) or debug_mode:
        await message.answer("Привет, сегодня я помогу тебе пройти регистрацию в нашем боте", reply_markup=kb_client)
    else:
        await message.answer("Ты уже регистрировался!")


# @dp.message_handler(commands=["Отмена"])
async def registration_cancellation(message: types.Message):
    await message.answer("Хорошего дня!")


# @dp.message_handler(commands=["Зарегистрироваться"]) todo: продекорировать все функции
async def registration_action(message: types.Message):
    await message.answer("Начнём!")
    await cm_start(message)


# ======================== ВЫЗОВ КАЛЬКУЛЯТОРА (ОСНОВНОЙ КОД ПРОПИСАН В КОНЦЕ) ============================

# @dp.message_handler(commands=["Калькулятор"])
# async def calculater(message: types.Message):
#     await message.answer("Отлично! Теперь тебе доступен наш калькулятор \n"
#                          "Давай, что-нибудь посчитаем! \n"
#                          "0", reply_markup=keyboards.client_kb.kb_calculater)


# ============================= [ МАШИНА СОСТОЯНИЙ (РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ) ] ==============================
class FSMAdmin(StatesGroup):
    user_id = State()
    photo = State()
    name = State()
    age = State()
    skills = State()
    phone = State()


# Начало диалога загрузки нового пункта меню

async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply(
        'Загрузите Ваше фото или мы можем загрузить фотографию вашего профиля. Просто кликните тут --> /take_photo_profile')


# Выход из состояний

# @dp.message_handler(state='*', commands='cancel')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('До встречи!')


# Ловим первый ответ и пишем в словарь
# @dp.message_handler(state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):

    if message.text == '/take_photo_profile':
        photos = await bot.get_user_profile_photos(message.from_user.id)

        if not photos.photos:
            await message.reply('У Вас нет фотографии в Профиле')
            return
        photo = photos.photos[0][-1]

    elif message.content_type == 'photo':
        photo = message.photo[0]

    else:
        photo = None

    if photo:
        file_name = f"user_photos/{datetime.datetime.now().strftime('%Y.%m.%d - %H-%M-%S')} - {message.from_user.id}.jpg"
        await photo.download(file_name)

        async with state.proxy() as data:  # --> значение из контекста.. Сначала получим словарь с данными data. А когда выходим из этого генератора, всё записывается в state
            data['user_id'] = message.from_user.id
            data['photo'] = file_name
        await FSMAdmin.next()
        await message.reply(f"Теперь введите ФИО. Пример ввода: 'Николаев Николай Николаевич',\n\n"
                            f"Если хотите воспользоваться функцией автозаполнение, то нажмите команду -----> "
                            f"/name_accept \n"
                            f"и мы возьмём имя из Вашего профиля "f" *  {full_name(message)}   * ")

    else:
        await message.reply("Кажется ты ввёл, что-то не то")


def full_name(message: types.Message):
    """ Функция проверяющая имя и фамилию пользователя на пустое значение """
    name = []
    name = message.from_user.first_name + str(message.from_user.last_name)
    if message.from_user.last_name is None:
        return message.from_user.first_name + ''
    else:
        return name


# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.text == "/name_accept":
        name = full_name(message)
    else:
        name = message.text
    # name = message.from_user.first_name + ' ' + message.from_user.last_name if message.text == "/name_accept" else message.text

    if name.replace(' ', '').isalpha():
        async with state.proxy() as data:
            data['name'] = name
        await FSMAdmin.next()
        await message.reply('Ваш возраст')

    elif [s for s in name if s in '1234567890']:
        async with state.proxy() as data:
            data['name'] = name
        await message.reply('Уверены ли Вы, что Ваше имя должно содержать цифры? Если да нажмите на команду /yes')

    else:
        await message.reply('Проверьте правильность введённых данных')


# @dp.message_handler(commands=["yes"], state=FSMAdmin.name)
async def check_load_name(message: types.Message, state: FSMContext):
    await FSMAdmin.next()
    await message.reply("Ваш возраст")


# Ловим третий ответ
# @dp.message_handler(state=FSMAdmin.age)
async def load_age(message: types.Message, state: FSMContext):
    if message.text.isnumeric() and 10 < int(message.text) < 100:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.reply('Какими навыками в программировании Вы обладаете?')
    else:
        await message.reply('Ответ не может содержать дробные числа и текст!\n'
                            ' А также диапазон введённого значения должен находится от 10 до 100')


# Ловим четвёртый ответ
# @dp.message_handler(state=FSMAdmin.skills
async def load_skills(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['skills'] = message.text
    await FSMAdmin.next()
    await message.reply('Ваш номер телефона в формате (9211802465)')
    # Другой способ ответить пользователю (то как выглядит метод ***reply*** внутри)
    # await message.bot.send_message(chat_id=message.chat.id, text='Ваш номер телефона в формате (9211802465)')


# Ловим пятый ответ
# @dp.message_handler(state=FSMAdmin.phone)
async def load_phone(message: types.Message, state: FSMContext):
    if message.text.isnumeric() and len(message.text) == 10:
        async with state.proxy() as data:
            data['phone'] = int(message.text)

        await sqlite_db.sql_add_command(state)
        await state.finish()

        await registration_goodbye(message)
    else:
        await message.reply(
            "Номер должен состоять из 10 цифр, без пробелов и без первых символов (+7) и 8, в формате (9211802465)")


# ============ ФУНКЦИИ ПРОВЕРКА (ЕСЛИ ПОЛЬЗОВАТЕЛЬ ВВЁЛ ПРОИЗВОЛЬНОЕ СООБЩЕНИЕ, СТИКЕР, ФОТОГРАФИЮ ОТППРАВИЛ) =========

async def echo(message: types.Message):
    await message.answer('Не понял Вашей команды. Проверьте правильность ввода')


@dp.message_handler(content_types=['sticker'])
async def handle_sticker(message: types.Message):
    await message.delete()


@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    await message.delete()


@dp.message_handler(content_types=['animation'])
async def handle_photo(message: types.Message):
    await message.delete()


# Завершение регистрации
# @dp.message_handler()
async def registration_goodbye(message: types.Message):
    await message.answer("Регистрация завершена!")


# ===========================================РЕГИСТРИРУЕМ ХЭНДЛЕРЫ======================================

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start", "registration"])
    dp.register_message_handler(registration_cancellation, commands=["Отмена"])
    dp.register_message_handler(registration_action, commands=["Зарегистрироваться"])
    dp.register_message_handler(echo)

    # Машина состояний

    dp.register_message_handler(cancel_handler, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_photo, state=FSMAdmin.photo)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(check_load_name, commands=["yes"], state=FSMAdmin.name)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_skills, state=FSMAdmin.skills)
    dp.register_message_handler(load_phone, state=FSMAdmin.phone)

    # КАЛЬКУЛЯТОР ПОСЛЕ РЕГИСТРАЦИИ


value = ''
old_value = ''


@dp.message_handler(commands=["Калькулятор"])
async def calculater(message: types.Message):
    await message.answer("Отлично! Теперь тебе доступен наш калькулятор \n"
                         "Давай, что-нибудь посчитаем! \n"
                         "0", reply_markup=keyboards.client_kb.kb_calculater)


@dp.callback_query_handler()
async def callback_func(query):
    button = query.data
    value = query.message.text.split('\n')[-1]

    if button == 'exit':
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        return

    if button == 'C':
        value = '0'
    elif button == '=':
        value = str(eval(value))
    else:
        value = button if value == '0' and button.isnumeric() else value + button

    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value,
                                reply_markup=keyboards.client_kb.kb_calculater)
