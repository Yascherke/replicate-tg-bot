import logging
from pathlib import Path
import replicate
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.types import ContentType, File, Message

from aiogram.utils import executor

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
        print(file, file_id)
        file_path = file.file_path
        file_on_disk = Path("", f"{file_id}.tmp")
        await bot.download_file(file_path, destination=file_on_disk)
        await message.reply("Аудио получено")

        model = replicate.models.get("openai/whisper")
        version = model.versions.get("30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed")


        # https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#input
        inputs = {
            # Audio file
            'audio': open(file_on_disk),

            # Choose a Whisper model.
            'model': "base",
            'translate': False,
            'temperature': 0,
            'suppress_tokens': "-1",
            'condition_on_previous_text': True,
            'temperature_increment_on_fallback': 0.2,
            'compression_ratio_threshold': 2.4,
            'logprob_threshold': -1,
            'no_speech_threshold': 0.6,
        }

        # https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#output-schema
        output = version.predict(**inputs)
        print('here working')
        await message.reply(output)

        os.remove(file_on_disk)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)