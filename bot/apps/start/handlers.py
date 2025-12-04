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
    await message.answer("""Привет! Ты в боте сервиса безопасного VPN.

С помощью нашего VPN ты сможешь:
• Открывать заблокированные сайты и сервисы  
• Защищать трафик в публичных сетях Wi‑Fi  
• Сохранять анонимность и конфиденциальность в интернете

Чтобы начать, выбери подходящий тариф. Если нужна помощь с выбором — нажми «Поддержка», и мы подскажем.""",reply_markup=start_inline_keyboard)


@router.callback_query(F.data == "support")
async def support(callback_data: CallbackQuery):
    await callback_data.message.delete()
    await callback_data.answer()
    await callback_data.message.answer("Все возникшие проблемы вы можете решить с пользователем @bobvalk",reply_markup=back_to_main)


@router.callback_query(F.data == "main")
async def main(callback_data: CallbackQuery):
    await callback_data.message.delete()
    await callback_data.answer()
    await start(callback_data.message)