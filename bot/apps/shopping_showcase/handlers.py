from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.database.crud import db_location
from bot.core.keyboards import *
from bot.apps.shopping_showcase.keyboards import *

router = Router()

@router.callback_query(F.data == "choose_server")
async def choose_server(callback_data: CallbackQuery):
    await callback_data.message.delete()
    await callback_data.answer()
    locations = await db_location.get_all()
    if locations == []:
        await callback_data.message.answer("Извините, пока нет доступных vpn", reply_markup=back_to_main)
        return

    message = "Доступные сервера для покупки\n"

    for location in locations:
        message += f"{location.name}\n"
    await callback_data.message.answer(message, reply_markup=all_servers(locations))

