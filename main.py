import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import users
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher()
    dp.include_router(users.router)
    print("🌱 Bot is ready!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())