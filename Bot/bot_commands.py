from aiogram import Bot 
from aiogram.types import BotCommand, BotCommandScopeDefault



async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start', 
            description='Начало работы'
        ), 
        BotCommand(
            command='random',
            description='Посоветовать фильм'
        ), 
        BotCommand(
            command='collections',
            description='Посмотреть подборки'
        ),
        BotCommand(
            command = 'choose',
            description='Подборка с выбором жанра, года и страны'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())