import random
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = "7001544678:AAF568OnS7jVyERdllzfJBIbGGy6C82bWIg"
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text="Найти информацию", callback_data="find_info")],
            [InlineKeyboardButton(text="Связаться", callback_data="contact")],
            [InlineKeyboardButton(text="О боте", callback_data="about")]
        ]
    )
    
    return keyboard

@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Это тестовый бот!",
        reply_markup=get_keyboard()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    Command_text = (
        "Доступные команды:\n"
        "/start - запустить бота\n"
        "/help - показывает список команд\n"
        "/random - случайное число"
    )
    await message.answer(Command_text)

@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    number = random.randint(1, 100)
    await message.answer(f"Случайное число:{number}")
@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data == "find_info":
        await callback.message.answer("Введите информацию для поиска")
    elif callback.data == "contact":
        await callback.message.answer("Напишите нам в личку")
    elif callback.data == "about":
        await callback.message.answer("Это наш на библиотеке aiogram")
    await callback.answer()

# Запуск бота
async def main():
    logging.basicConfig(
        level=logging.INFO,
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())