import random
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен вашего бота
TOKEN = "7001544678:AAF568OnS7jVyERdllzfJBIbGGy6C82bWIg"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для хранения данных пользователей
user_data = {}

# Клавиатура для выбора игры
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Угадай число", callback_data="game_guess_number")],
            [InlineKeyboardButton(text="Камень, ножницы, бумага", callback_data="game_rps")],
            [InlineKeyboardButton(text="Викторина", callback_data="game_quiz")],
            [InlineKeyboardButton(text="Помощь", callback_data="help")]
        ]
    )
    return keyboard

# Команда /start
@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот с играми. Выбери игру:",
        reply_markup=get_main_keyboard()
    )

# Команда /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "Доступные игры:\n"
        "1. Угадай число: бот загадывает число, а ты пытаешься его угадать.\n"
        "2. Камень, ножницы, бумага: сыграй против бота в классическую игру.\n"
        "3. Викторина: ответь на вопросы и проверь свои знания.\n\n"
        "Команды:\n"
        "/start - начать\n"
        "/help - показать правила"
    )
    await message.answer(help_text)

# Обработка callback-запросов
@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "game_guess_number":
        # Игра "Угадай число"
        user_data[user_id] = {"game": "guess_number", "secret_number": random.randint(1, 100)}
        await callback.message.answer("Я загадал число от 1 до 100. Попробуй угадать!")
    elif callback.data == "game_rps":
        # Игра "Камень, ножницы, бумага"
        user_data[user_id] = {"game": "rps"}
        await callback.message.answer("Выбери: камень, ножницы или бумага?")
    elif callback.data == "game_quiz":
        # Игра "Викторина"
        user_data[user_id] = {"game": "quiz", "score": 0, "question_index": 0}
        await ask_quiz_question(callback.message, user_id)
    elif callback.data == "help":
        await cmd_help(callback.message)
    await callback.answer()

# Обработка текстовых сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        await message.answer("Выбери игру:", reply_markup=get_main_keyboard())
        return

    game_data = user_data[user_id]
    game_type = game_data.get("game")

    if game_type == "guess_number":
        # Игра "Угадай число"
        try:
            guess = int(message.text)
            secret_number = game_data["secret_number"]

            if guess < secret_number:
                await message.answer("Мое число больше!")
            elif guess > secret_number:
                await message.answer("Мое число меньше!")
            else:
                await message.answer(f"Поздравляю! Ты угадал число {secret_number}!")
                del user_data[user_id]
        except ValueError:
            await message.answer("Пожалуйста, введите число!")

    elif game_type == "rps":
        # Игра "Камень, ножницы, бумага"
        user_choice = message.text.lower()
        bot_choice = random.choice(["камень", "ножницы", "бумага"])

        if user_choice in ["камень", "ножницы", "бумага"]:
            result = determine_rps_winner(user_choice, bot_choice)
            await message.answer(f"Ты выбрал {user_choice}, я выбрал {bot_choice}. {result}")
            del user_data[user_id]
        else:
            await message.answer("Пожалуйста, выбери: камень, ножницы или бумага.")

    elif game_type == "quiz":
        # Игра "Викторина"
        user_answer = message.text.lower()
        correct_answer = quiz_questions[game_data["question_index"]]["answer"].lower()

        if user_answer == correct_answer:
            game_data["score"] += 1
            await message.answer("Правильно!")
        else:
            await message.answer(f"Неправильно. Правильный ответ: {correct_answer}.")

        game_data["question_index"] += 1
        if game_data["question_index"] < len(quiz_questions):
            await ask_quiz_question(message, user_id)
        else:
            await message.answer(f"Викторина окончена! Твой счёт: {game_data['score']}/{len(quiz_questions)}")
            del user_data[user_id]

# Функция для определения победителя в игре "Камень, ножницы, бумага"
def determine_rps_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "Ничья!"
    elif (user_choice == "камень" and bot_choice == "ножницы") or \
         (user_choice == "ножницы" and bot_choice == "бумага") or \
         (user_choice == "бумага" and bot_choice == "камень"):
        return "Ты выиграл!"
    else:
        return "Я выиграл!"

# Вопросы для викторины
quiz_questions = [
    {"question": "Сколько планет в Солнечной системе?", "answer": "8"},
    {"question": "Какой газ преобладает в атмосфере Земли?", "answer": "Азот"},
    {"question": "Кто написал 'Войну и мир'?", "answer": "Толстой"},
]

# Функция для задания вопроса викторины
async def ask_quiz_question(message: types.Message, user_id: int):
    question_index = user_data[user_id]["question_index"]
    question = quiz_questions[question_index]["question"]
    await message.answer(question)

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())ёёё