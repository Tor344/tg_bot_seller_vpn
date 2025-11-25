from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.core.keyboards import *
from bot.apps.start.keyboards import *

from bot.database.crud import db_user

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await db_user.add(id=message.from_user.id)
    await message.answer("Главная",reply_markup=start_inline_keyboard)


@router.callback_query(F.data == "support")
async def support(callback_data: CallbackQuery):
    await callback_data.message.delete()
    await callback_data.answer()
    await callback_data.message.answer("Все возникшие проблемы вы можете решить с пользователем @Shit_wordbot",reply_markup=back_to_main)


@router.callback_query(F.data == "main")
async def main(callback_data: CallbackQuery):
    await callback_data.message.delete()
    await callback_data.answer()
    await start(callback_data.message)