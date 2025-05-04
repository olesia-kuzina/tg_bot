from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

import keys
from handlers import router
from data import db_session, DataBase
import asyncio


async def set_menu(bot: Bot):
    s = [
        BotCommand(command="/help", description="описание"),
        BotCommand(command="/country", description="описание"),
        BotCommand(command="/city", description="описание"),
    ]
    await bot.set_my_commands(s)

async def main(bot: Bot):
    dp = Dispatcher()
    dp.startup.register(set_menu)
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def start():
    db_session.global_init("data/bot.db")
    bot = Bot(keys.key_api_tg)
    asyncio.run(main(bot))

if __name__ == "__main__":
    start()