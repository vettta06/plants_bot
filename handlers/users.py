from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import json


router = Router()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Отправить локацию", request_location=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет, садовод! 🌱\n"
        "Я помогу тебе выращивать урожай вовремя.\n"
        "Отправь свою геолокацию — и я подскажу, когда и что сажать в твоём регионе.",
        reply_markup=keyboard
    )


@router.message(lambda msg: msg.location is not None)
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude

    await message.answer(
        f"✅ Получено: {lat:.4f}, {lon:.4f}\n"
        "Определяю твой регион..."
    )

    try:
        with open("data/garden_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        await message.answer("❌ Ошибка: файл данных не найден.")
        return
    except json.JSONDecodeError:
        await message.answer("❌ Ошибка: повреждён файл данных.")
        return

    found_region = None
    for region in data["regions"]:
        lat_min, lat_max = region["lat_range"]
        lon_min, lon_max = region["lon_range"]
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            found_region = region
            break

    if not found_region:
        await message.answer(
            "🌍 Я не знаю данных для твоего региона.\n"
            "Пока я поддерживаю: Московскую, Краснодарскую и Новосибирскую области.\n"
            "Попробуй ближе к крупному городу (Москва, Краснодар, Новосибирск)."
        )
        return

    name = found_region["name"]
    crops = found_region["crops"]

    text = f"🌱 Ты в регионе: *{name}*\n\n"
    text += "📅 Сроки посадки:\n\n"

    for crop, times in crops.items():
        text += f"📌 *{crop.capitalize()}*\n"
        for stage, period in times.items():
            if stage == "sow_indoors":
                text += f"   Посев (рассада): {period}\n"
            elif stage == "sow_direct":
                text += f"   Посев в грунт: {period}\n"
            elif stage == "transplant":
                text += f"   Высадка: {period}\n"
        text += "\n"

    text += "✅ Рекомендации учтены по последнему заморозку."

    await message.answer(text, parse_mode="Markdown")