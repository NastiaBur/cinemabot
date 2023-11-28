import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message

import keyboards
from kino import get_info
from database_fun import *
# import codecs

bot = Bot("6987883476:AAEDMR0zI1MfeuiURulhNpFmD7Lq0ligW2Y")
dp = Dispatcher()


@dp.message(F.text == "/start")
async def start(message: Message):
    print(message)
    await message.answer(f"Hello, {message.from_user.first_name}")


@dp.message(F.text == "Описание")
async def sm(message: Message):
    print(message)
    # f = codecs.open('last.txt', 'r', 'utf-8')
    # s = f.readline()
    # print(s)
    
    s = get_movie(str(message.from_user.first_name))
    film = get_info(s)
    await message.answer(f"Описание: {film.description}")

@dp.message()
async def echo(message: Message):
    print(message)
    film = get_info(message.text)
    # f = codecs.open('last.txt', 'w', 'utf-8')
    # f.write(message.text)
    user_name = str(message.from_user.first_name)
    print(user_name)
    if user_exists(user_name):
        user_update(user_name, film.name)
    else:
        user_add(user_name, film.name)
    ans = 'Название: {} \nГод создания: {} \nРейтинг: {} \nСтрана: {} \nВозраст: {}'.format(film.name, film.year, film.rating, ', '.join(film.country), film.age)
    await message.answer(ans, reply_markup=keyboards.film_kb)
    # await message.answer("Here you go: ", reply_markup=keyboards.links_kb)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
