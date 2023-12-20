from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardButton
)

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

class Pagination(CallbackData, prefix = "pag"):
    action: str
    page: int


def paginator(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=Pagination(action="prev", page=page).pack()),
        InlineKeyboardButton(text="➡", callback_data=Pagination(action="next", page=page).pack()),
        width=2
    )
    return builder.as_markup()

class AddFillter(Filter):
    def __init__(self):
        self.descr = "Описание"
        self.direct = "Режиссеры"
        self.actors = "Главные актеры"
        self.seasons = "Количество сезонов"
    
    async def __call__(self, message: Message) -> bool:
        req = message.text
        return (req == self.descr) or (req == self.direct) or (req == self.actors) or (req == self.seasons)
    
    
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