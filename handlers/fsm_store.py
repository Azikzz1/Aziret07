from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import cancel_markup, start_markup
from aiogram.types import ReplyKeyboardRemove
from db import main_db


class FSMShop(StatesGroup):
    model_name = State()
    size_1 = State()
    price = State()
    photo = State()
    category = State()
    productid = State()
    infoproduct = State()
    collection = State()
    submit = State()


async def start_fsm_shop(message: types.Message):
    await FSMShop.model_name.set()
    await message.answer('Введите название модели:', reply_markup=cancel_markup)


async def load_model_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['model_name'] = message.text
    await FSMShop.next()
    await message.answer('Введите размер:')


async def load_size_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_1'] = message.text
    await FSMShop.next()
    await message.answer('Введите стоимость:')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSMShop.next()
    await message.answer('Отправьте фото товара:')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await FSMShop.next()
    await message.answer('Введите категорию:')


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await FSMShop.next()
    await message.answer('Введите productID:')


async def load_productid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['productid'] = message.text
    await FSMShop.next()
    await message.answer('Введите описание продукта:')


async def load_infoproduct(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['infoproduct'] = message.text
    await FSMShop.next()
    await message.answer('Введите коллекцию продукты:')


async def load_collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text
    await FSMShop.next()
    await message.answer(f'Верные ли данные?')
    await message.answer_photo(photo=data['photo'],
                               caption=f'Название модели: {data["model_name"]}\n'
                                       f'Размер: {data["size_1"]}\n'
                                       f'Стоимость: {data["price"]}\n'
                                       f'ProductID: {data["productid"]}\n'
                                       f'Категория: {data["category"]}\n'
                                       f'Описание продукта: {data["infoproduct"]}\n'
                                       f'Введите коллекцию продукта: {data["collection"]}\n'
                                       f'Все верно? (Да/Нет)')
    await FSMShop.submit.set()


async def load_submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
            await main_db.sql_insert_store(
                model_name=data['model_name'],
                size_1=data['size_1'],
                price=data['price'],
                photo=data['photo'],
                productid=data['productid'],
            )
            await main_db.sql_insert_products_details(
                productid=data['productid'],
                category=data['category'],
                infoproduct=data['infoproduct']
            )
            await main_db.sql_insert_collection_products(
                productid=data['productid'],
                collection=data['collection']
            )
            await message.answer('Товар успешно добавлен!', reply_markup=start_markup)
        await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer('Добавление товара отменено.', reply_markup=start_markup)
        await state.finish()
    else:
        await message.answer('Пожалуйста, введите "Да" или "Нет".')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=start_markup)


def register_fsmshop_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='отмена',
                                                 ignore_case=True), state='*')
    dp.register_message_handler(start_fsm_shop, commands=['add_item'])
    dp.register_message_handler(load_model_name, state=FSMShop.model_name)
    dp.register_message_handler(load_size_1, state=FSMShop.size_1)
    dp.register_message_handler(load_price, state=FSMShop.price)
    dp.register_message_handler(load_photo, state=FSMShop.photo, content_types=['photo'])
    dp.register_message_handler(load_productid, state=FSMShop.productid)
    dp.register_message_handler(load_category, state=FSMShop.category)
    dp.register_message_handler(load_infoproduct, state=FSMShop.infoproduct)
    dp.register_message_handler(load_collection, state=FSMShop.collection)
    dp.register_message_handler(load_submit, state=FSMShop.submit)
