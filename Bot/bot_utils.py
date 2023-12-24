import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, InputMedia, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart
from aiogram.utils.media_group import MediaGroupBuilder
import random

import json 

from kino_parse.kino import Film
from kino_parse.kino import create_str_list
from kino_parse.collections import get_collections
from kino_parse.database_fun import *
from victoria_secret import TOKEN

from bot_items import AddFillter, CollFilter, film_kb, Pagination, paginator
from bot_commands import set_commands


bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher()


 # Функционал /start
@dp.message(CommandStart())
async def start(message: Message):
    await set_commands(bot)
    await message.answer(f"Привет, <b>{message.from_user.first_name}</b>! \nНапиши мне название фильма, который надо найти.")

# Обработка сообщений с дополнительной информацией 
@dp.message(AddFillter())
async def additional_info(message: Message):
    request = message.text
    db_film_name = get_movie(str(message.from_user.username))
    film = Film(db_film_name)

    if request == "Описание":
        ans = f"<b>Описание:</b> {film.get_description()}"
    elif request == "Режиссеры":
        directors = ", ".join(film.get_directors())
        ans = f"<b>Режиссеры:</b> {directors}"
    elif request == "Главные актеры":
        main_actors = ", ".join(film.get_actors())
        ans = f"<b>Главные актеры:</b> {main_actors}"
    else:
        if film.get_seasons() != None:
            ans = f"<b>Количество сезонов:</b> {film.get_seasons()}"
        else:
            ans = 'Скорее всего это фильм или информация не была найдена :('  

    await message.answer(ans)
    await message.answer("Что-то ещё?", reply_markup=film_kb)


# Подборка новогодних фильмов через пагинацию
@dp.callback_query(Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: Pagination):
    coll_name = callback_data.name
    if coll_name == "top":
        file_name= "Bot/movies.json"
    else:
        file_name = "Bot/collections.json"
    
    with open(file_name, encoding='utf-8') as json_data:
        data = json.load(json_data)
    
    page_num = int(callback_data.page)
    page = (page_num + len(data[coll_name]) - 1) % len(data[coll_name])

    if callback_data.action == "next":
        page = (page_num + 1) % len(data[coll_name])

    file = types.InputMediaPhoto(media=data[coll_name][page]['img'], caption=data[coll_name][page]['name'])
    await call.message.edit_media(media = file, reply_markup=paginator(page, coll_name))


@dp.message(F.text == "/omg")
async def top(message: Message):
    json_file = 'Bot/movies.json'
    with open(json_file, encoding='utf-8') as json_data:
            data = json.load(json_data)
    file = data['top'][0]['img']

    await message.answer("Happy New Year, honey :)", reply_markup=ReplyKeyboardRemove())
    
    await bot.send_photo(
        message.chat.id,
        photo=file,
        reply_markup=paginator(0,'top'),
        caption=data['top'][0]['name'],
    )

@dp.message(F.text == '/collections')
async def get_names(message: Message):
    await message.answer("У меня есть такие подборки, выбери команду и напиши её мне: \n \
/anti_stress - Подборка доброго расслабляющего кино \n \
/soviet - Подборка советского кино \n \
/holiday - Подборка новогодних фильмов \n \
/puzzle - Подборка фильмов головоломок \n \
/oscar - Подборка фильмов с премией оскар \n \
/animals - Подборка фильмов про животных \n \
/women - Подборка фильмов о сильных женщинах \n \
/middle_age - Подборка фильмов о средневековье")


# Подборка фильмов сразу одним сообщением
@dp.message(F.text == "/last")
async def top_movies(message: Message):

    json_file = 'Bot/movies.json'

    with open(json_file, encoding="utf-8") as json_data:
        data = json.load(json_data)

        caption = "<b>Название:</b>"

    for i in range(len(data['top'])):
        caption += "\n" + str(i + 1) + ". " + data['top'][i]['name']

    
    album_builder = MediaGroupBuilder(
        caption=caption
    )

    for e in data['top']:
        album_builder.add(
            type = "photo",
            media=e['img']

        )
    await message.answer("Happy New Year, honey :)", reply_markup=ReplyKeyboardRemove())
    
    await message.answer_media_group(
        media=album_builder.build()
    )

@dp.message(F.text == "😡")
async def top(message: Message):
    await message.answer("Вы у меня самые лучшие!")

# Посоветовать фильм из подборки топ-250 лучших
@dp.message(F.text == "/random")
async def random_from_top(message: Message):

    json_file = 'Bot/top_250_movies.json'

    film_index = random.randint(0, 249)

    with open(json_file, encoding="utf-8") as json_data:
        data = json.load(json_data)

    random_film_name = data['top_250_films'][film_index]
    
    await message.answer("Вот случайный фильм:", reply_markup=ReplyKeyboardRemove())
    object.__setattr__(message, "text", random_film_name)
    await echo(message)
# Обработка запроса подборки
    
@dp.message(CollFilter())
async def get_collection(message: Message):
    request = message.text
    get_collections(request[1:])
    collections = 'Bot/collections.json'
    with open(collections, encoding='utf-8') as json_data:
        coll_data = json.load(json_data)

    if request == "/anti_stress":
        coll = "anti_stress"
        name = coll_data[coll][0]['name']
        img = coll_data[coll][0]['img']       
    elif request == "/soviet":
        coll = "soviet"
        name = coll_data[coll][0]['name']
        img = coll_data[coll][0]['img']     
    elif request == "/holiday":
        coll = "holiday"
        name = coll_data[coll][0]['name']
        img = coll_data[coll][0]['img']
    elif request == "/puzzle":
        coll = "puzzle"
        name = coll_data[coll][0]['name']
        img = coll_data[coll][0]['img']
    elif request == "/oscar":
        coll = "oscar"
        name = coll_data[coll][0]['name']
        img = coll_data[coll][0]['img']
    elif request == "/animals":
        coll = "animals"
        name = coll_data[coll][0]['name']
        img = coll_data[coll][0]['img']
    elif request == "/women":
        coll = "women"
        name = coll_data[coll][0]['name']
        img = coll_data[coll][0]['img']
    else:
        coll = "middle_age"
        name = coll_data[coll][0]['name']
        img = coll_data[coll][0]['img']


    await message.answer("Ваша подборка: ")
    await bot.send_photo(
    message.chat.id,
    photo=img,
    reply_markup=paginator(0, coll),
    caption=coll_data[coll][0]['name'],
)

        
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


    if film_name is None:
        await message.answer("Не найдено :(")
    else:
        youtube_link = film.youtube_parser()
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

        other_films_by_request = create_str_list(message.text)
        question = 'Возможно, вы искали какой-то из этих фильмов?\n\n' + other_films_by_request
        
        ans = '<b>Название:</b> {} \n<b>Год создания:</b> {} \n<b>Рейтинг:</b> kinopoisk {} \ ivi  {}\n<b>Страна:</b> {} \n<b>Возраст:</b> {}'.format(film_name, 
            film.get_year(), film.get_rating(), ivi_rating, ', '.join(film.get_country()), film.get_age())
        await bot.send_photo(chat_id=message.chat.id, photo=film.get_poster_url(), caption=ans, reply_markup=urlkb.as_markup())
        await message.answer(question)
        await message.answer("Что-то ещё?", reply_markup=film_kb)

    



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
