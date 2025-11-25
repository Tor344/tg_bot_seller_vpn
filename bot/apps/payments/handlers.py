import asyncio
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery,BufferedInputFile
from aiogram.filters import Command

from bot.database.crud import db_server,db_vpn

from bot.core.keyboards import *
from bot.apps.payments.keyboards import *


router = Router()



@router.callback_query(F.data.startswith("bay_server_"))
async def bayes(callback_data: CallbackQuery):
    await callback_data.message.delete()
    await callback_data.answer()
    # servers = await db_server.get_all_for_name(callback_data.data.split("_")[-1])
    # server_ip, server_id = await server_search.server_search(servers)
    # msg = await callback_data.message.answer("🔄 VPN создается")
    #
    # stop_flag = asyncio.Event()
    #
    # task = asyncio.create_task(progress_message_editor(msg, stop_flag))
    #
    # count_vpn = await db.get_count_vpn(callback_data.from_user.id)
    # name_user = str(callback_data.from_user.id) +"_" + str(count_vpn)
    #
    # data = request_to_backend.add_user(
    #     api_token=API_BACKEND,
    #     ip=server_ip,
    #     name_user=name_user
    # )
    #
    # date_break = (datetime.today() + relativedelta(months=1)).strftime("%Y.%m.%d")
    data = "Hello word"
    date = datetime.now()
    await db_vpn.add(user_id=callback_data.from_user.id,data=data,date_break=date, server_id=1)
    # stop_flag.set()
    # await callback_data.message.delete()
    # await asyncio.sleep(0.1)
    file_bytes = data.encode('utf-8')  # конвертация строки в байты
    input_file = BufferedInputFile(file_bytes, filename='open.vpn')
    await callback_data.message.answer_document(document=input_file)
    await callback_data.message.answer("Ваш файл",reply_markup=back_to_main)


@router.callback_query(F.data.startswith("extend_"))
async def bayes(callback_data: CallbackQuery):
    await callback_data.message.delete()
    await callback_data.answer()
    numeral = callback_data.data.split("_")[-1]
    await callback_data.message.answer(f"Вы продлили vpn {int(numeral) + 1}")
