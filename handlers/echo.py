from aiogram import types
from aiogram.dispatcher import Dispatcher


async def echo_handler(message: types.Message):
    try:
        number = int(message.text)
        squared_number = number ** 2
        await message.answer(str(squared_number))
    except ValueError:
        await message.answer(message.text)


def register_echo_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_handler)
