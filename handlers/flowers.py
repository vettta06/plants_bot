import shutil
from pathlib import Path

from aiogram import Router, types
from aiogram.filters import CommandStart
from model.classifier import predict, plant_info, class_names
from aiogram.types import FSInputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import os

TEMP_DIR = Path("data/temp")
CORRECTIONS_DIR = Path("data/corrections")
TEMP_DIR.mkdir(exist_ok=True)

last_photo_path = None

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "🌿 Привет! Я — бот для определения растений.\n"
        "Отправь мне фото растения — и я скажу, что это за вид!"
    )


@router.message(lambda msg: msg.photo)
async def handle_photo(message: types.Message):
    print(f"Получено фото от {message.from_user.id}")

    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = file.file_path

    downloaded_path = "data/temp_photo.jpg"
    await message.bot.download_file(file_path, downloaded_path)
    print(f"✅ Фото скачано: {downloaded_path}")

    common_name, scientific_name = predict(downloaded_path)
    print(f"Предсказание: {common_name}, {scientific_name}")

    if os.path.exists(downloaded_path):
        os.remove(downloaded_path)
        print("🗑️ Временный файл удалён")

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
    else:
        text = "Не удалось распознать растение. Попробуй другое фото."

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Верно"), KeyboardButton(text="❌ Ошибка")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)

    last_photo_path = str(downloaded_path)

    await message.answer(text, parse_mode="Markdown")
    print("Ответ отправлен")


@router.message(lambda msg: msg.text == "❌ Ошибка")
async def handle_mistake(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="берёза"), KeyboardButton(text="дуб"), KeyboardButton(text="крапива")],
            [KeyboardButton(text="мать-и-мачеха"), KeyboardButton(text="одуванчик"), KeyboardButton(text="роза")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("А что это за растение?", reply_markup=keyboard)

@router.message(lambda msg: msg.text in class_names)
async def handle_correction(message: types.Message):
    global last_photo_path
    correct_name = message.text

    if last_photo_path and os.path.exists(last_photo_path):
        target_dir = CORRECTIONS_DIR / correct_name
        target_dir.mkdir(exist_ok=True)
        shutil.copy(last_photo_path, target_dir / f"corrected_{message.from_user.id}.jpg")

        await message.answer(
            f"Спасибо! Я запомнил, что это — *{correct_name}* 🌱",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer("Не могу найти фото для исправления.", reply_markup=ReplyKeyboardRemove())

    last_photo_path = None