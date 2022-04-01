from aiogram import types, Dispatcher
from create_bot import dp, bot

from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import client_kb


# @dp.message_handler(commands=["start", "registration"])
async def start_command(message: types.Message):
    await message.answer("Привет, сегодня я помогу тебе пройти регистрацию в нашем боте", reply_markup=kb_client)


# @dp.message_handler(commands=["Отмена"])
async def registration_cancellation(message: types.Message):
    await message.answer("Хорошего дня!")


# @dp.message_handler(commands=["Зарегистрироваться"])
async def registration_action(message: types.Message):
    await message.answer("Начнём!")
    await cm_start(message)


# Завершение регистрации

# @dp.message_handler()
async def registration_goodbye(message: types.Message):
    await message.answer("Регистрация завершена!")
#1231231232

# ===================================== [ Машина СОСТОЯНИЙ ]
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
    await message.reply('Загрузите Ваше фото')


# Выход из состояний

# @dp.message_handler(state='*', commands='Отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('До встречи!')


# Ловим первый ответ и пишем в словарь

# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    # data = state.proxy()
    async with state.proxy() as data:   # --> значение из контекста (м.б. и есть контекст)
        data['user_id'] = message.from_user.id
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply(f"Теперь введите ФИО. Пример ввода: 'Николаев Николай Николаевич',\n\n"
                        f"Если хотите воспользоваться функцией автозаполнение, то мы возьмём имя Вашего профиля в телеграмм   ***   {full_name(message)}   ***   нажмите команду /name_accept \n"
                        f"Или можете ввести имя сами")


def full_name(message: types.Message):
    """ Функция проверяющаяя имя и фамилию пользователя на пустое значение """
    full_name = []
    full_name = message.from_user.first_name + str(message.from_user.last_name)
    if message.from_user.last_name == None:
        return message.from_user.first_name + ''
    else:
        return full_name


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
        await message.reply('Ответ не может содержать дробные числа и текст!\n /'
                            'Диапазон введённого значения должен находится от 10 до 100')


# Ловим четвёртый ответ

# @dp.message_handler(state=FSMAdmin.skills
async def load_skills(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['skills'] = message.text
    await FSMAdmin.next()
    await message.reply('Ваш номер телефона в формате (9211802465)')


# Ловим пятый ответ
# @dp.message_handler(state=FSMAdmin.phone
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


async def echo(message: types.Message):
    await message.answer('Не понял Вашей команды. Проверьте правильность ввода')

    # Регистрием хэндлеры


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start", "registration"])
    dp.register_message_handler(registration_cancellation, commands=["Отмена"])
    dp.register_message_handler(registration_action, commands=["Зарегистрироваться"])
    dp.register_message_handler(echo)

    # Машина состояний

    dp.register_message_handler(cancel_handler, state='*', commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(check_load_name, commands=["yes"], state=FSMAdmin.name)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_skills, state=FSMAdmin.skills)
    dp.register_message_handler(load_phone, state=FSMAdmin.phone)

# @dp.message_handler(commands=["regist"], state=None)
# async def registration_action(message: types.Message):
#     await message.answer("Вы начали регистрацию.\n\n" "1. Введите ваше ФИО")
