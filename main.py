from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher import FSMContext
# import  asyncio
from keyboards import *
from config import *
import texts
from crud_functions import *

bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb_start)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = ikb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')

@dp.message_handler(text='Информация')
async def inform(message):
    with open('Photo/about.jpg', 'rb') as about_img:
        await message.answer_photo(about_img, texts.About, reply_markup = kb_start)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await UserState.age.set()
    data = await  state.get_data()
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth = message.text)
    await UserState.growth.set()
    data = await  state.get_data()
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_(message, state):
    await state.update_data(weight = message.text)
    await UserState.weight.set()
    data = await  state.get_data()
    calories = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
    await message.answer(f"Ваша норма калорий: {calories}")

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    f = 1
    for product in products:
        with open(f'Photo/{f}.jpg', 'rb') as img:
            await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
            await message.answer_photo(img)
            f += 1
        await message.answer(text='', reply_murkup=ikb_buy)


@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    initiate_db()
