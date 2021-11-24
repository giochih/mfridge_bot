
import aiogram

button1 = aiogram.types.InlineKeyboardButton('Добавить')
button2 = aiogram.types.InlineKeyboardButton('Проверить')
button3 = aiogram.types.InlineKeyboardButton('Что приготовить?')
greet_board = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2).add(button3)


def create_board(mas):
    new_board = aiogram.types.InlineKeyboardMarkup()
    for i in mas:
        new_board .add(aiogram.types.InlineKeyboardButton(i, callback_data=i))
    return new_board
