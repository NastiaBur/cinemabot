import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

import keyboards
from kino import *
from database_fun import *
from victoria_secret import *

# Создаём бота
bot = Bot(TOKEN)
dp = Dispatcher()

# Функционал /start
@dp.message(F.text == "/start")
async def start(message: Message):
    print(message)
    await message.answer(f"Hello, {message.from_user.first_name}")


# Функционал кнопки "Описание"
@dp.message(F.text == "Описание")
async def sm(message: Message):
    
    s = get_movie(str(message.from_user.username))
    film = get_info(s)
    await message.answer(f"Описание: {film.description}")
    await message.answer("Что-то ещё?", reply_markup=keyboards.film_kb)

# Функционал кнопки "Режиссеры"
@dp.message(F.text == "Режиссеры")
async def sm(message: Message):
    s = get_movie(str(message.from_user.username))
    film = get_info(s)
    print(" ".join(film.directors))
    await message.answer("Режиссеры: {}".format(", ".join(film.directors)))
    await message.answer("Что-то ещё?", reply_markup=keyboards.film_kb)

# Функционал кнопки "Главные актеры"
@dp.message(F.text == "Главные актеры")
async def sm(message: Message):
    s = get_movie(str(message.from_user.username))
    film = get_info(s)
    print(" ".join(film.directors))
    await message.answer("Главные актеры: {}".format(", ".join(film.actors)))
    await message.answer("Что-то ещё?", reply_markup=keyboards.film_kb)

# Функционал кнопки "Количество сезонов"
@dp.message(F.text == "Количество сезонов")
async def sm(message: Message):
    s = get_movie(str(message.from_user.username))
    film = get_info(s)
    print(" ".join(film.directors))
    print(type(film.seasons))
    print(film.seasons)
    if film.seasons != None:
        await message.answer("Количество сезонов: {}".format(film.seasons))
    else:
        await message.answer('Скорее всего это фильм или информация не была найдена')
    await message.answer("Что-то ещё?", reply_markup=keyboards.film_kb)


# Функционал при вводе названия фильма
@dp.message()
async def echo(message: Message):
    film = get_info(message.text)
    user_name = str(message.from_user.username)
    
    if film.name is not None:
        if user_exists(user_name):
            user_update(user_name, film.name)
        else:
            user_add(user_name, film.name)


    if film.name is None:
        await message.answer("Не найдено")
    else:
        rating, link = ivi_parser(film.name)
        if link is None:
            links = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="kinopoisk", url=str(film.site_url))
                ]
            ]   
            )
        else:
            links = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Ivi", url =str(link)),
                    InlineKeyboardButton(text="kinopoisk", url=str(film.site_url))
                ]
            ]   
            )

            
        
        ans = 'Название: {} \nГод создания: {} \nРейтинг: kino {} \ ivi {}\nСтрана: {} \nВозраст: {}'.format(film.name, 
            film.year, film.rating, rating, ', '.join(film.country), film.age)
        await bot.send_photo(chat_id=message.chat.id, photo=film.poster_url, caption=ans, reply_markup=links)
        await message.answer("Что-то ещё?", reply_markup=keyboards.film_kb)
    



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
