# send_products.py
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from db import main_db
from aiogram.types import InputMediaPhoto


async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    button_all_products = types.InlineKeyboardButton('Вывести все товары',
                                                     callback_data='send_all_products')
    button_one_products = types.InlineKeyboardButton('Вывести по одному',
                                                     callback_data='send_one_products')
    keyboard.add(button_all_products, button_one_products)
    await message.answer('Выберите как просмотреть товары: ', reply_markup=keyboard)


async def send_all_products(call: types.CallbackQuery):
    products = main_db.fetch_all_products()
    if products:  # True
        for product in products:
            caption = (f'Название модели: {product["model_name"]}\n'
                       f'Размер: {product["size_1"]}\n'
                       f'Стоимость: {product["price"]}\n'
                       f'ProductID: {product["productid"]}\n'
                       f'Категория: {product["category"]}\n'
                       f'Описание продукта: {product["infoproduct"]}\n'
                       f'Введите коллекцию продукта: {product["collection"]}\n')

            await call.message.answer_photo(photo=product['photo'], caption=caption)
    else:  # False
        await call.message.answer('База пустая! Товаров нет.')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands=['store'])
    dp.register_callback_query_handler(send_all_products, Text(equals='send_all_products'))
