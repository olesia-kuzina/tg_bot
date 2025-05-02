from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text='Привет!')


@router.message(Command("/help"))
async def help(message: Message):
    await message.answer(text="Это сообщение поможет сориентироваться по работе с этим ботом")


@router.message(Command("/stop"))
async def stop(message: Message):
    await message.answer(text="работа всех функций остановлена")

@router.message(Command("/capitals"))
async def capitals(message: Message):
    await message.answer(text="Введите страну, а я назову сталицу")


@router.message(Command("/city"))
async def city(message: Message):
    await message.answer(text="отправьте город, а я назову страну, в которой находится этот город")
