import logging
from pathlib import Path
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.types import ContentType, File, Message

from aiogram.utils import executor

from stt import speach_to_text

logging.basicConfig(level=logging.INFO)

API_TOKEN = "5732112995:AAF2jUYLHD1bjQz9nNqLgnPTG2dhp0fLyl0"
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

os.environ["REPLICATE_API_TOKEN"] = "ca9b4ba5a16a763131558d84d478a17fa3a936a1"


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.first_name
    await bot.send_message(message.chat.id, f"Hello, {user_id}")


@dp.message_handler(content_types=[
    ContentType.VOICE,
    ContentType.AUDIO,
    ContentType.DOCUMENT
])
async def voice_message_handler(message: Message):
    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id
    elif message.content_type == types.ContentType.AUDIO:
        file_id = message.audio.file_id
    elif message.content_type == types.ContentType.DOCUMENT:
        file_id = message.document.file_id
    else:
        await message.reply("Формат документа не поддерживается")
        return

    file = await bot.get_file(file_id)
    file_id = file.file_id
    print(file)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.oga")
    await bot.download_file(file_path, destination=file_on_disk)
    await message.reply(speach_to_text(file_on_disk))
    os.remove(file_on_disk)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
