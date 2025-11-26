from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode

from bot.database.crud import db_vpn,db_server

from bot.core.keyboards import *
from bot.apps.user.keyboards import *
router = Router()

@router.callback_query(F.data == "my_vpn")
async def print_my_vpn(callback_data: CallbackQuery):
    await callback_data.message.delete()
    await callback_data.answer()
    vpns = await db_vpn.get_vpns_by_user(callback_data.from_user.id)
    if vpns == []:
        await callback_data.message.answer("Извините, у вас до сих пор нет vpn",reply_markup=back_to_main)
        return
    message = ""
    for index, vpn in enumerate(vpns):
        message += f"VPN ID: {vpn.id}\n    Местоположение:{await db_server.get_location(vpn.id)}\n    Окончание действия: {vpn.date_break.strftime("%Y.%m.%d")}\n"
    await callback_data.message.answer(message, reply_markup=my_vpn(vpns))


@router.callback_query(F.data.startswith("duplicate_file_"))
async def user(callback_data: CallbackQuery):
    await callback_data.answer()
    data = await db_vpn.get_data(callback_data.data.split("_")[-1])
    await callback_data.message.answer(f"Ваша ссылка для подключения:\n <code>{data}</code>",parse_mode=ParseMode.HTML)
    await print_my_vpn(callback_data)

