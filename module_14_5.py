from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from crud_functions import initiate_db, add_user, is_included
import sqlite3

# Инициализация базы данных
initiate_db()

# Токен и бот
api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Основное меню
main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(KeyboardButton("Рассчитать"), KeyboardButton("Информация"), KeyboardButton("Купить"),
                       KeyboardButton("Регистрация"))

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот для расчёта калорий и покупки продуктов. Выберите опцию ниже:",
                         reply_markup=main_menu_keyboard)

@dp.message_handler(lambda message: message.text.lower() == "регистрация")
async def sing_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь с таким именем уже существует, введите другое имя.")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    if not email:  # Проверка на пустое значение
        await message.answer("Email не может быть пустым, попробуйте снова.")
        return
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isdigit():  # Проверка на числовое значение
        await message.answer("Возраст должен быть числом, попробуйте снова.")
        return
    await state.update_data(age=age)

    # Завершаем регистрацию, сохраняем данные в базу данных
    user_data = await state.get_data()
    username = user_data.get("username")
    email = user_data.get("email")
    age = user_data.get("age")

    # Проверка на наличие всех данных
    if not all([username, email, age]):
        await message.answer("Ошибка в процессе регистрации. Пожалуйста, начните снова.")
        await state.finish()
        return

    # Добавление пользователя в базу данных
    add_user(username, email, age)
    await message.answer("Регистрация прошла успешно!")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
