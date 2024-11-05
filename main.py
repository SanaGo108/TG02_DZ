import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from googletrans import Translator
from pydub import AudioSegment
from pydub.utils import which
from aiogram.types import FSInputFile
from config import TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Установка пути к ffmpeg
AudioSegment.converter = which("ffmpeg")
if AudioSegment.converter is None:
    raise RuntimeError("ffmpeg not found. Make sure ffmpeg is installed and available in PATH.")

# Создание объекта бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

translator = Translator()

# Убедимся, что директория img существует
if not os.path.exists('img'):
    os.makedirs('img')

# Обработчик для фото
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_name = os.path.join('img', f'{photo.file_id}.jpg')

    await photo.download(file_name)
    await message.reply("Photo saved!")

# Обработчик для голосовых сообщений
async def handle_voice(message: types.Message):
    voice = await message.voice.get_file()
    file_name_ogg = f'{voice.file_id}.ogg'
    file_name_wav = f'{voice.file_id}.wav'

    await voice.download(file_name_ogg)

    # Конвертируем ogg в wav
    audio = AudioSegment.from_ogg(file_name_ogg)
    audio.export(file_name_wav, format='wav')

    await message.reply("Voice message saved and converted to WAV format!")

    # Удаляем ogg файл, если это необходимо
    os.remove(file_name_ogg)

# Обработчик для текстовых сообщений
async def handle_text(message: types.Message):
    translated = translator.translate(message.text, dest='en')
    await message.reply(f"Translation to English: {translated.text}")

async def main():
    # Регистрация обработчиков
     dp.message.register(handle_photo, content_types=['photo'])
     dp.message.register(handle_voice, content_types=['voice'])
     dp.message.register(handle_text, content_types=['text'])

     # Запуск бота
     try:
         await dp.start_polling(bot)
     finally:
         await bot.close()

 if __name__ == '__main__':
     asyncio.run(main())