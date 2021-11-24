from main import bot,dp
from dataf import add,check,sooner
from btns import greet_board, create_board
import aiogram
import asyncio
from states import Curr
from ingrid import ingrid_search, recommend
from datetime import datetime as dt


def checkdate(date):
    try:
        now = dt.now()
        if dt.strptime(date, '%d.%m.%y')<= now:
            return False
        else:
            return True
    except:
        return False


@dp.message_handler(commands=['start'])
async def hi(message: aiogram.types.message):
    await message.reply("хай",reply_markup=greet_board)

@dp.message_handler(state=None)
async def choose_ingr(message: aiogram.types.message,state:aiogram.dispatcher.FSMContext):
    reply = message.text
    if reply == "Добавить":
        print(message.chat.id)
        # добавить продукт
        await bot.send_message(message.chat.id, text='Введите название продукта')
        await Curr.ingrid.set()
    elif reply == 'Проверить':
        # проверить продукты
        await bot.send_message(message.chat.id, text=check(message.chat.id))
    elif reply == 'Что приготовить?':
        # что приготовить
        meal = sooner(message.chat.id)
        if meal == []:
            await bot.send_message(message.chat.id, text="У вас ничего не добавлено")
        else:
            s = 'Cкоро испортится '
            for food in meal:
                s += food + ', '
            await bot.send_message(message.chat.id, text=s[:-2])
            recommendations = recommend(meal)
            if recommendations == []:
                await bot.send_message(message.chat.id, text='Рецептов нет')
            else:
                s = "Доступные рецепты:"
                await bot.send_message(message.chat.id, text=s)
                for food in recommendations:
                    s =  '"'+food[0]+ '" по ссылке:\n'+ food[1]
                    await bot.send_message(message.chat.id, text=s)


@dp.callback_query_handler(state=Curr.ingrid)
async def process_callback_kb1btn1(callback_query: aiogram.types.CallbackQuery,state:aiogram.dispatcher.FSMContext):

    code = callback_query.data
    t= 'Добавлю ' + code + '. Когда этот продукт испортится?\n Введите в формате dd.mm.yy. Если не хотите добавлять этот продукт напишите Нет'
    await Curr.date.set()
    await state.update_data({'prod':code})
    await bot.send_message(callback_query.from_user.id, text=t)


@dp.message_handler(state=Curr.ingrid)
async def choose_ingr(message: aiogram.types.message,state:aiogram.dispatcher.FSMContext):
    reply= message.text
    mas = ingrid_search(reply)
    board = create_board(mas)
    await message.reply("Хорошо, что вы имелли ввиду?\n Если нет подходящего варианта, переформулируйте запрос и введите заново", reply_markup=board)

@dp.message_handler(state=Curr.date)
async def choose_ingr(message: aiogram.types.message,state:aiogram.dispatcher.FSMContext):
    reply = message.text
    if reply.lower() == 'нет':
        t ='Ок, отмена'
        await message.reply(t)
        await state.finish()
    else:
        if checkdate(reply):
            data = await state.get_data()
            t = 'Хорошо, добавлю ' + data.get('prod') + " который испортится " + reply
            await message.reply(t)
            add(message.chat.id, data.get('prod'), reply)
            await state.finish()
        else:
            t = 'Вы уверны, что дата введена правильно? Попробуйте снова'
            await message.reply(t)
