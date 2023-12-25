from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.types import (
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove,
    KeyboardButton, 
    InlineKeyboardButton
)

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Pagination(CallbackData, prefix = "pag"):
    action: str
    page: int
    name: str


def paginator(page: int=0, name: str=""):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=Pagination(action="prev", page=page, name=name).pack()),
        InlineKeyboardButton(text="➡", callback_data=Pagination(action="next", page=page, name=name).pack()),
        width=2
    )
    return builder.as_markup()

class AddFilter(Filter):
    def __init__(self):
        self.descr = "Описание"
        self.direct = "Режиссеры"
        self.actors = "Главные актеры"
        self.seasons = "Количество сезонов"
    
    async def __call__(self, message: Message) -> bool:
        req = message.text
        return (req == self.descr) or (req == self.direct) or (req == self.actors) or (req == self.seasons)
class CollFilter(Filter):
    def __init__(self):
        self.anti_stress = "/anti_stress" # Кино антистресс
        self.soviet = "/soviet" # Советское
        self.holiday = "/holiday" # Новогодние фильмы про любовь и волшебство
        self.puzzle = "/puzzle" # Фильмы головоломки 
        self.oscar = "/oscar" # Премия оскар
        self.animals = "/animals" # Лучшее кино про животных
        self.women = "/women" # Истории великих женщин
        self.middle_age = "/middle_age" # Фильмы про средневековье
        self.passion = "/passion" 
    
    async def __call__(self, message: Message) -> bool:
        req = message.text
        return (req == self.anti_stress) or (req == self.soviet) \
                or (req == self.holiday) or (req == self.puzzle) \
                or (req == self.oscar) or (req == self.animals)  \
                or (req == self.women) or (req == self.middle_age) or (req == self.passion)
    
class ChoiceFilter(Filter):
    def __init__(self):
            self.genre = "Выбрать жанр"
            self.country = "Выбрать год"
            self.year = "Выбрать страну"
    
    async def __call__(self, message: Message) -> bool:
        req = message.text
        return (req == self.genre) or (req == self.country) or (req == self.year)

film_kb = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text='Режиссеры'), 
            KeyboardButton(text='Главные актеры')
        ], 
        [ 
            KeyboardButton(text='Описание'), 
            KeyboardButton(text='Количество сезонов')
        ]
    ], 
    resize_keyboard=True, # сделать кнопки маленькими
    one_time_keyboard=True, # скрывается после первого использования
    input_field_placeholder='Выберите действие из меню', 
    selective=True # чтобы норм в чатах работало, хз насколько нам это надо 
)

choice_kb = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text='Выбрать жанр'), 
            KeyboardButton(text='Выбрать год'),
            KeyboardButton(text= 'Выбрать страну')
        ]
    ], 
    resize_keyboard=True, # сделать кнопки маленькими
    one_time_keyboard=True, # скрывается после первого использования
    input_field_placeholder='Выберите действие из меню', 
    selective=True # чтобы норм в чатах работало, хз насколько нам это надо 
)
