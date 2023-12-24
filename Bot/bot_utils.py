import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart
import random

import json 

from kino_parse.kino import Film
from kino_parse.collections import get_collections
from kino_parse.database_fun import *
from kino_parse.fichi import create_str_list
from victoria_secret import TOKEN

from bot_items import AddFillter, CollFilter, film_kb, Pagination, paginator
from bot_commands import set_commands
from logger import bot_logger


bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher()


 # Функционал /start
@dp.message(CommandStart())
async def start(message: Message):
    '''
    Функция, обрабатывающая команду /start.

    Параметры:
    message (Message): Объект, содержащий информацию о сообщении.

    Описание:
    Функция вызывается при получении команды /start. Возвращает приветственное сообщение и просит пользователя ввести название фильма.

    Пример использования:
    >> start(message)
    '''
    bot_logger.info(f'User {message.from_user.id} started the bot and updated collections')
    await set_commands(bot)
    await message.answer(f"Привет, <b>{message.from_user.first_name}</b>! \nНапиши мне название фильма, который надо найти.")

# Обработка сообщений с дополнительной информацией 
@dp.message(AddFillter())
async def additional_info(message: Message):
    ''''
    Функция, обрабатывающая дополнительную информацию о фильме.

    Параметры:
    message (Message): Объект, содержащий информацию о сообщении.

    Описание:
    Функция вызывается при получении запроса на дополнительную информацию о фильме: Описание, Режиссеры, Главные актеры, Количество сезонов. 
    В зависимости от запроса, функция возвращает запрашиваемую информацию о фильме, взятую с помощью соотвествующего метода класса Film.
    '''
    request = message.text
    db_film_name = get_movie(str(message.from_user.username))
    film = Film(db_film_name)
    if db_film_name:
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
    elif (request == "Режиссеры"):
        ans = "Режиссер фильма None Эдгар Сан Хуан :)"
    else:
        ans = "Информация не была найдена, пожалуйста, введи название фильма"  
    
    bot_logger.debug(f'Sent request {request.lower()} for the film {db_film_name}')
    await message.answer(ans)
    await message.answer("Что-то ещё?", reply_markup=film_kb)


# Подборка новогодних фильмов через пагинацию
@dp.callback_query(Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: Pagination):
    '''
    Функция, обрабатывающая запросы пагинации.

    Параметры:
    call (CallbackQuery): Объект, содержащий информацию о вызове обратного запроса.
    callback_data (Pagination): Объект, содержащий информацию о данных пагинации.

    Описание:
    Функция вызывается при получении запроса на пагинацию списка фильмов. В зависимости от действия (предыдущая или следующая страница), 
    функция обновляет выводимое на экране изображение и название фильма с помощью метода edit_media объекта сообщения.
    '''
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
    '''
    Функция-обработчик для команды "/omg".
    
    Параметры:
    message: Message - Полученное сообщение от пользователя.

    Описание: 
    Принимает сообщение и отправляет пользователю фотографию с подписью и клавиатурой пагинации.
    '''

    bot_logger.info("Received a message /omg")
    json_file = 'Bot/movies.json'
    with open(json_file, encoding='utf-8') as json_data:
            data = json.load(json_data)
    file = data['top'][0]['img']

    await message.answer("Happy New Year, honey :)", reply_markup=ReplyKeyboardRemove())
    bot_logger.debug("Sent a special collection with pagination")    
    await bot.send_photo(
        message.chat.id,
        photo=file,
        reply_markup=paginator(0,'top'),
        caption=data['top'][0]['name'],
    )

@dp.message(F.text == '/collections')
async def get_names(message: Message):
    '''
    Функция-обработчик для команды "/collections".
    
    Параметры:
    message: Message - Полученное сообщение от пользователя.

    Описание: 
    Принимает сообщение и отправляет пользователю список доступных подборок фильмов.
    '''
    bot_logger.info("Received a message /collections and sent info")
    await message.answer("У меня есть такие подборки, выбери команду и напиши её мне: \n /anti_stress - Подборка доброго расслабляющего кино \n \
/soviet - Подборка советского кино \n /holiday - Подборка новогодних фильмов \n /puzzle - Подборка фильмов головоломок \n /oscar - Подборка фильмов с премией оскар \n \
/animals - Подборка фильмов про животных \n /women - Подборка фильмов о сильных женщинах \n /middle_age - Подборка фильмов о средневековье \n \
/passion - Подборка фильмов с изюминкой, \n /omg - Наша специальная подборка") 


@dp.message(F.text == "😡")
async def top(message: Message):
    bot_logger.info("Received a special message and sent a secret response")
    await message.answer("Вы у меня самые лучшие!")




@dp.message(F.text == "/random")
async def random_from_top(message: Message):
    '''
    Функция-обработчик для команды "/random".
    
    Параметры:
    message: Message - Полученное сообщение от пользователя.

    Описание: 
    Принимает сообщение и отправляет пользователю случайный фильм из топ-250.
    '''
    bot_logger.debug("Received a /random message")
    json_file = 'Bot/top_250_movies.json'

    film_index = random.randint(0, 249)

    with open(json_file, encoding="utf-8") as json_data:
        data = json.load(json_data)

    random_film_name = data['top_250_films'][film_index]
    
    await message.answer("Вот случайный фильм:", reply_markup=ReplyKeyboardRemove())
    object.__setattr__(message, "text", '/random' + random_film_name)
    await echo(message)



    
@dp.message(CollFilter())
async def get_collection(message: Message):
    '''
    Функция-обработчик для получения подборки.
    
    Параметры:
    message: Message - Полученное сообщение от пользователя.

    Описание: 
    Принимает сообщение с запросом подборки и отправляет пользователю запрашиваемую подборку.
    '''
    request = message.text
    bot_logger.info(f"get a usual collection request {request}")
    get_collections(request[1:])
    collections = 'Bot/collections.json'
    with open(collections, encoding='utf-8') as json_data:
        coll_data = json.load(json_data)
    
    coll = request[1:]
    name = coll_data[coll][0]['name']
    img = coll_data[coll][0]['img']


    await message.answer("Ваша подборка: ")
    await bot.send_photo(
    message.chat.id,
    photo=img,
    reply_markup=paginator(0, coll),
    caption=name)
    bot_logger.info(f"Sent a collection with name {request[1:]}")

        
# Функционал при вводе названия фильма
@dp.message()
async def echo(message: Message):
    command_random = False
    if message.text.startswith('/random'):
        modified_message = message.text.replace('/random', '')
        command_random = True
        bot_logger.debug("Catched a /random message")
    else:
        modified_message = message.text
    film = Film(modified_message)
    user_name = str(message.from_user.username)
    film_name = film.get_name()
    if film_name is not None:
        if user_exists(user_name):
            user_update(user_name, film_name)
            bot_logger.info("Sent an update request to the database")
        else:
            user_add(user_name, film_name)
            bot_logger.info("Sent an add request to the database")
            
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
        
        ans = '<b>Название:</b> {} \n<b>Год создания:</b> {} \n<b>Рейтинг:</b> kinopoisk {} \ ivi  {}\n<b>Страна:</b> {} \n<b>Возраст:</b> {}'.format(film_name, 
            film.get_year(), film.get_rating(), ivi_rating, ', '.join(film.get_country()), film.get_age())

        await bot.send_photo(chat_id=message.chat.id, photo=film.get_poster_url(), caption=ans, reply_markup=urlkb.as_markup())
        if not command_random:
            other_films_by_request = create_str_list(message.text)
            question = 'Возможно, вы искали какой-то из этих фильмов?\n\n' + other_films_by_request
            await message.answer(question)

        await message.answer("Что-то ещё?", reply_markup=film_kb)

