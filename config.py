# config.py
from aiogram import Bot, Dispatcher
from decouple import config


Admins = [7006569892, ]

token = config("TOKEN")

bot = Bot(token=token)
dp = Dispatcher(bot)
