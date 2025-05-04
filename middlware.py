import logging
import traceback
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from data import DataBase


class MessageMiddlWare(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Update, data: Dict[str, Any]):

        if event.callback_query:
            user_id = event.callback_query.from_user.id
        elif event.message:
            user_id = event.message.from_user.id
        else:
            user_id = event.event.from_user.id
        DataBase.increment_count(tg_id=user_id)
        try:
            return await handler(event, data)
        except Exception:
            logging.exception(f'[{user_id}] - {traceback.format_exc()}')
