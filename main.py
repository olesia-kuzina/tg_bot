import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

import keys
from AI import AIHelper
from data import db_session
import handlers
from middlware import MessageMiddlWare

logging.basicConfig(
    filename='logging.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.DEBUG
)



async def set_menu(bot: Bot):
    s = [
        BotCommand(command="/help", description="описание"),
        BotCommand(command="/country", description="описание"),
        BotCommand(command="/city", description="описание"),
        BotCommand(command="/count", description="описание"),
        BotCommand(command="/attraction", description="описание"),
    ]
    await bot.set_my_commands(s)

async def main(bot: Bot):
    handlers.AI = AIHelper()
    dp = Dispatcher()
    dp.update.middleware(MessageMiddlWare())
    dp.startup.register(set_menu)
    dp.include_router(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def start():
    db_session.global_init("data/bot.db")
    bot = Bot(keys.key_api_tg)
    asyncio.run(main(bot))

if __name__ == "__main__":
    start()