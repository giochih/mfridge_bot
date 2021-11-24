from config import tel_token
import aiogram
import asyncio
import aioschedule
import sqlite3
from datetime import datetime as dt
from aiogram.contrib.fsm_storage.memory import MemoryStorage


loop = asyncio.get_event_loop()
bot = aiogram.Bot(tel_token)
dp = aiogram.Dispatcher(bot, loop=loop, storage=MemoryStorage())


async def clear():
    connect = sqlite3.connect('data.db')
    cur = connect.cursor()
    now = dt.now()
    mas = []
    for line in cur.execute(f"""select * from data """):
        if dt.strptime(line[2], '%d.%m.%y') <= now:
            mas.append(line)
    for line in mas:
        cur.execute(f"""delete from data where (id = {line[0]} and ing_name='{line[1]}' and ing_lifetime = '{line[2]}'); 
                    """)
        text = line[2]+' испортился продукт ' + line[1] + '\n Этот продукт удален из вашего списка продуктов'
        await bot.send_message(line[0], text=text)
    connect.commit()


async def scheduler():
    aioschedule.every().day.at("22:00").do(clear)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == "__main__":
    from hand import dp
    aiogram.executor.start_polling(dp, skip_updates=False, on_startup=on_startup)

