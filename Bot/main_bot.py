import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart, Filter

import keyboards
from kino import *
from database_fun import *
from victoria_secret import *


class AddFillter(Filter):
    def __init__(self):
        self.descr = "Описание"
        self.direct = "Режиссеры"
        self.actors = "Главные актеры"
        self.seasons = "Количество сезонов"
    
    async def __call__(self, message: Message) -> bool:
        req = message.text
        return (req == self.descr) or (req == self.direct) or (req == self.actors) or (req == self.seasons)


# Создаём бота
bot = Bot(TOKEN)
dp = Dispatcher()

 # Функционал /start
@dp.message(CommandStart())
async def start(message: Message):
    print(message)
    await message.answer(f"Hello, {message.from_user.first_name}")

# Обработка сообщений с дополнительной информацией 
@dp.message(AddFillter())
async def sm(message: Message):
    request = message.text
    db_film_name = get_movie(str(message.from_user.username))
    film = Film(db_film_name)

    if request == "Описание":
        ans = f"Описание: {film.get_description()}"
    elif request == "Режиссеры":
        directors = ", ".join(film.get_directors())
        ans = f"Режиссеры: {directors}"
    elif request == "Главные актеры":
        main_actors = ", ".join(film.get_actors())
        ans = f"Главные актеры: {main_actors}"
    else:
        if film.get_seasons() != None:
            ans = f"Количество сезонов: {film.get_seasons()}"
        else:
            ans = 'Скорее всего это фильм или информация не была найдена'  

    await message.answer(ans)
    await message.answer("Что-то ещё?", reply_markup=keyboards.film_kb)



# Функционал при вводе названия фильма
@dp.message()
async def echo(message: Message):
    film = Film(message.text)
    user_name = str(message.from_user.username)
    film_name = film.get_name()

    if film_name is not None:
        if user_exists(user_name):
            user_update(user_name, film_name)
        else:
            user_add(user_name, film_name)


    youtube_link = film.youtube_parser()
    if film_name is None:
        await message.answer("Не найдено")
    else:
        urlkb = InlineKeyboardBuilder()
        
        ivi_rating, ivi_link = film.get_ivi_info()
        if ivi_link is not None:
            urlkb.add(types.InlineKeyboardButton(text="ivi", url =str(ivi_link)))
        

        urlkb.add(types.InlineKeyboardButton(text="kinopoisk", url=str(film.get_kinopoisk_url())))
        urlkb.add(types.InlineKeyboardButton(text= "youtube", url = str(youtube_link)))

        zona_link = film.zona_parser()
        if zona_link is not None:
            urlkb.add(types.InlineKeyboardButton(text="zona", url =str(zona_link)))

        anime_link = film.anime_parser()
        if anime_link is not None:
            urlkb.add(types.InlineKeyboardButton(text="anime", url =str(anime_link)))
            
        
        ans = 'Название: {} \nГод создания: {} \nРейтинг: kino {} \ ivi {}\nСтрана: {} \nВозраст: {}'.format(film_name, 
            film.get_year(), film.get_rating(), ivi_rating, ', '.join(film.get_country()), film.get_age())
        await bot.send_photo(chat_id=message.chat.id, photo=film.get_poster_url(), caption=ans, reply_markup=urlkb.as_markup())
        await message.answer("Что-то ещё?", reply_markup=keyboards.film_kb)
    



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
