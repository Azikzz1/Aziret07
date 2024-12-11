from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import cancel_markup, start_markup
from aiogram.types import ReplyKeyboardRemove


class FSMShop(StatesGroup):
    model_name = State()
    size = State()
    category = State()
    price = State()
    photo = State()
    submit = State()


async def start_fsm_shop(message: types.Message):
    await FSMShop.model_name.set()
    await message.answer('Введите название модели:', reply_markup=cancel_markup)


async def load_model_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['model_name'] = message.text
    await FSMShop.next()
    await message.answer('Введите размер:')


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await FSMShop.next()
    await message.answer('Введите категорию:')


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
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
    await message.answer_photo(photo=data['photo'],
                               caption=f"Название модели: {data['model_name']}\n"
                                       f"Размер: {data['size']}\n"
                                       f"Категория: {data['category']}\n"
                                       f"Стоимость: {data['price']}\n"
                                       f"Все верно? (Да/Нет)")
    await FSMShop.submit.set()


async def load_submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
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
    dp.register_message_handler(load_size, state=FSMShop.size)
    dp.register_message_handler(load_category, state=FSMShop.category)
    dp.register_message_handler(load_price, state=FSMShop.price)
    dp.register_message_handler(load_photo, state=FSMShop.photo, content_types=['photo'])
    dp.register_message_handler(load_submit, state=FSMShop.submit)
