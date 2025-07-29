from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import flower_bot

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(flower_bot.router)

    print("Flower bot is ready!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())