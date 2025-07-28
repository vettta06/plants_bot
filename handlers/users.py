from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
