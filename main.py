from aiogram import Bot, Dispatcher

import keys
from handlers import router
from data import db_session, DataBase
import asyncio

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    db_session.global_init("data/bot.db")
    bot = Bot(keys.key_api_tg)
    asyncio.run(main())