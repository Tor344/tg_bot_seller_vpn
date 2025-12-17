import pathlib

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile,InputMediaPhoto
from aiogram.filters import Command
from aiogram.enums import ParseMode

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


@router.callback_query(F.data == "instructions")
async def instructions(callback_data: CallbackQuery):
    await callback_data.answer()
    await callback_data.message.delete()
    script_dir = pathlib.Path(__file__).parent.parent.parent
    photos = [
        FSInputFile(f"{script_dir}/media/5339052465770401257.jpg"),
        FSInputFile(f"{script_dir}/media/5339052465770401258.jpg"),
        FSInputFile(f"{script_dir}/media/5339052465770401260.jpg")
    ]
    media = [
        InputMediaPhoto(media=photos[2], caption="""1. Скопируйте ссылку, полученную после покупки
    2. Скачайте
            ios: https://apps.apple.com/ru/app/v2raytun/id6476628951
            android: https://play.google.com/store/apps/details?id=com.v2raytun.android&hl=ru&pli=1
    3. Следуйте действиям на фото
"""),
        InputMediaPhoto(media=photos[1]),InputMediaPhoto(media=photos[1])
    ]

    # Send to the same chat as callback
    await callback_data.message.answer_media_group(media)
    await callback_data.message.answer("Вернуться на главную",reply_markup=back_to_main)