from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from model.classifier import predict, plant_info
import os

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "🌿 Привет! Я — бот для определения растений.\n"
        "Отправь мне фото растения — и я скажу, что это за вид!"
    )

@router.message(lambda msg: msg.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = file.file_path

    downloaded_path = "data/temp_photo.jpg"
    await message.bot.download_file(file_path, downloaded_path)

    common_name, scientific_name = predict(downloaded_path)

    if os.path.exists(downloaded_path):
        os.remove(downloaded_path)

    if common_name and scientific_name:
        info = plant_info[common_name]
        text = (
            f"🌿 **{common_name.capitalize()}**\n"
            f"🧬 *{scientific_name}*\n"
            f"🏡 Семейство: {info['family']}\n"
            f"📍 {info['region']}\n"
            f"📅 {info['season']}\n"
            f"💡 {info['uses']}"
        )

        image_path = info["image_path"]
        print(f"🖼️ Отправляю фото: {image_path}")

        if not os.path.exists(image_path):
            print(f"❌ Файл не найден: {image_path}")
            await message.answer(text, parse_mode="Markdown")
            return

        photo = FSInputFile(image_path)

        try:
            await message.answer_photo(
                photo=photo,
                caption=text,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ Ошибка при отправке фото: {e}")
            await message.answer(text, parse_mode="Markdown")
    else:
        await message.answer("❌ Не удалось распознать растение. Попробуй другое фото.")