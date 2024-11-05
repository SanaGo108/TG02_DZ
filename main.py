import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from googletrans import Translator
from config import TOKEN

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

translator = Translator()

# Handler for /start command
@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer("Привет! Я бот-помощник.")

# Handler for photo messages
@dp.message(F.photo)
async def handle_photo(message: Message):
    if not os.path.exists('img'):
        os.makedirs('img')

    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    photo_path = f'img/{photo.file_id}.jpg'
    await bot.download_file(file_info.file_path, photo_path)
    await message.answer("Файл сохранен")

# Handler for text messages to translate to English
@dp.message(F.text)
async def handle_text(message: Message):
    text_to_translate = message.text
    translated_text = translator.translate(text_to_translate, src='auto', dest='en').text
    await message.answer(translated_text)

# Command to send a voice message
@dp.message(Command(commands=['sendvoice']))
async def send_voice(message: Message):
    voice_path = 'path_to_voice_message.ogg'  # Specify the path to your voice message
    with open(voice_path, 'rb') as voice:
        await message.answer_voice(voice)

# Run the bot
if __name__ == '__main__':
    dp.run_polling(bot)