from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

links_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Youtube", url ="https://www.youtube.com/watch?v=ic8j13piAhQ")
        ]
    ]
)

main_kb = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text='Найти фильм'), 
            KeyboardButton(text='Подборка по жанрам')
        ], 
        [ 
            KeyboardButton(text='Мой список фильмов'), 
            KeyboardButton(text='Eщё что-то')
        ]
    ], 
    resize_keyboard=True, # сделать кнопки маленькими
    one_time_keyboard=True, # скрывается после первого использования
    input_field_placeholder='Выберите действие из меню', 
    selective=True # чтобы норм в чатах работало, хз насколько нам это надо 
)

film_kb = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text='Режисера'), 
            KeyboardButton(text='Главные актеры')
        ], 
        [ 
            KeyboardButton(text='Описание'), 
            KeyboardButton(text='Покажи еще что-то')
        ]
    ], 
    resize_keyboard=True, # сделать кнопки маленькими
    one_time_keyboard=True, # скрывается после первого использования
    input_field_placeholder='Выберите действие из меню', 
    selective=True # чтобы норм в чатах работало, хз насколько нам это надо 
)