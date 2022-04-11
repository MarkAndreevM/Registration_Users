from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton("/Зарегистрироваться")
b2 = KeyboardButton("/Отмена")
b3 = KeyboardButton("/Калькулятор")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).insert(b3).add(b2)

# КНОПКИ ДЛЯ КАЛЬКУЛЯТОРА

kb_calculater = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_calculater.row(InlineKeyboardButton('🚫', callback_data='exit'),
                  InlineKeyboardButton('C', callback_data='C'),
                  InlineKeyboardButton('<=', callback_data='<='),
                  InlineKeyboardButton('/', callback_data='/'))

kb_calculater.row(InlineKeyboardButton('7', callback_data='7'),
                  InlineKeyboardButton('8', callback_data='8'),
                  InlineKeyboardButton('9', callback_data='9'),
                  InlineKeyboardButton('*', callback_data='*'))

kb_calculater.row(InlineKeyboardButton('4', callback_data='4'),
                  InlineKeyboardButton('5', callback_data='5'),
                  InlineKeyboardButton('6', callback_data='6'),
                  InlineKeyboardButton('-', callback_data='-'))

kb_calculater.row(InlineKeyboardButton('1', callback_data='1'),
                  InlineKeyboardButton('2', callback_data='2'),
                  InlineKeyboardButton('3', callback_data='3'),
                  InlineKeyboardButton('+', callback_data='+'))

kb_calculater.row(InlineKeyboardButton(' ', callback_data='no'),
                  InlineKeyboardButton('0', callback_data='0'),
                  InlineKeyboardButton(',', callback_data='.'),
                  InlineKeyboardButton('=', callback_data='='))
