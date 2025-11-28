from datetime import datetime, timedelta

import pytz

from aiogram.types import InlineKeyboardMarkup

from bot.database.crud import db_vpn
from bot.core.keyboards import *

from config import settings

from bot.utils.backend import delete_user

from config.settings import API_BACKEND

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Moscow'))

async def up_data_database(bot):
    vpns = await db_vpn.get_all()
    moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
    for vpn in vpns:
        datelamda = (vpn.date_break - moscow_time).days
        if datelamda <= 0:
            user_id = vpn.user.id
            await bot.send_message(
                chat_id=user_id,
                text=f"Вы не продлили ваш vpn №{vpn.id} локация: {vpn.server.location.name}"
            )
            await delete_user(ip=vpn.server.ip, api_token=API_BACKEND, name_user=vpn.file_name)
            await db_vpn.delete(id=vpn.id)
            continue
        if datelamda < 5:
            user_id = vpn.user.id
            await bot.send_message(
                chat_id=user_id,
                text=f"У тебя скоро истечёт VPN №{vpn.id} локация {vpn.server.location.name}, осталось {datelamda} дней", reply_markup=extend_vpn(vpn.id)
            )

