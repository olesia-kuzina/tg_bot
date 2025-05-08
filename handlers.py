from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardMarkup
from states import FSMForm
import requests
from aiogram.fsm.state import default_state
from data import DataBase
from country_helpers import CountryHelpers

router = Router()
AI = None


def cancel_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text='Отменить')]])
    return kb


@router.message(Command("attraction"))
async def attraction(message: Message, state: FSMContext):
    await message.answer(
        text="отправьте город или страну, а я назову 5 достопримечательностей и интересныы факты к ним",
        reply_markup=cancel_kb())
    await state.set_state(FSMForm.enter_request)


@router.message(StateFilter(FSMForm.enter_request))
async def process_attraction(message: Message):
    await message.answer(await AI.get_text_message(request=message.text))
    await message.answer(
        text="отправьте город или страну, а я назову несколько достопримечательностей и интересныы факты к ним",
        reply_markup=cancel_kb())


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text='Привет!')
    DataBase.add_user(name=message.from_user.username, tg_id=message.from_user.id)


@router.message(Command("count"))
async def count(message: Message):
    await message.answer(f"вы отправили {DataBase.get_count(message.from_user.id)} сообщений")


@router.message(lambda message: message.text == "Отменить", ~StateFilter(default_state))
async def process_cancel(message: Message, state: FSMContext):
    await message.answer("Ввод отменён", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Command("help"))
async def help(message: Message):
    await message.answer(text="Это сообщение поможет сориентироваться по работе с этим ботом")


@router.message(Command("country"))
async def capitals(message: Message, state: FSMContext):
    await message.answer(text="Введите страну, а я назову столицу", reply_markup=cancel_kb())
    await state.set_state(FSMForm.enter_country)


@router.message(Command("city"))
async def city(message: Message, state: FSMContext):
    await message.answer(text="отправьте город, а я назову страну, в которой находится этот город",
                         reply_markup=cancel_kb())
    await state.set_state(FSMForm.enter_city)


@router.message(StateFilter(FSMForm.enter_city))
async def process_city(message: Message, state: FSMContext):
    toponym_to_find = message.text

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response or len(response.json()["response"]['GeoObjectCollection']['featureMember']) == 0:
        await message.answer("Такого города не существует")

    else:
        json_response = response.json()
        await message.answer(json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                                 'metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['CountryName'])
    await message.answer(text="отправьте город, а я назову страну, в которой находится этот город",
                         reply_markup=cancel_kb())


@router.message(StateFilter(FSMForm.enter_country))
async def process_country(message: Message, state: FSMContext):
    capital = CountryHelpers.search_capital(message.text)
    if not capital:
        await message.answer("Такой страны не существует")

    else:
        await message.answer(capital)
    await message.answer(text="отправьте страну, а я назову столицу",
                         reply_markup=cancel_kb())
