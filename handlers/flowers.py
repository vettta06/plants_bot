from aiogram import Router, types
from aiogram.filters import CommandStart
from model.classifier import predict
import os

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "📸 Привет! Я — бот для определения цветов.\n"
        "Отправь мне фото цветка — и я скажу, что это за вид!"
    )

@router.message(lambda msg: msg.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = file.file_path

    downloaded_path = "data/temp_photo.jpg"
    await message.bot.download_file(file_path, downloaded_path)

    common_name, scientific_name = predict(downloaded_path)

    if scientific_name:
        text = f"🌸 Это *{common_name}*!\n"
        text += f"Научное название: _{scientific_name}_\n\n"
        text += "Хочешь совет по уходу за этим цветком?"
    else:
        text = "❌ Не удалось распознать цветок. Попробуй другое фото."

    await message.answer(text, parse_mode="Markdown")