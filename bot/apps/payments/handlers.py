import asyncio
from datetime import datetime
import uuid

from dateutil.relativedelta import relativedelta

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery,BufferedInputFile,LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode

from bot.utils.backend import *
from bot.utils.progress_message_editor import progress_message_editor
from bot.database.crud import db_server,db_vpn

from bot.core.keyboards import *
from bot.apps.payments.keyboards import *


from config.settings import COST_VPN


router = Router()


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.callback_query(F.data.startswith("bay_server_"))
async def cmd_buy(callback_data: CallbackQuery):
    await callback_data.answer()
    location = callback_data.data.split("_")[-1]
    if server_search(location) == None:
        await callback_data.message.answer("Извините, в данный момент нет доступных vpn с такой локацией\n Попробуйте позже или выберите другую локацию", reply_markup=back_to_main)
        return
    await callback_data.message.answer_invoice(
        title=f"Подписка на VPN '{location}'",
        description=f"Активация VPN {location}на 1 месяц",
        payload="bay_server_" + location,
        provider_token="",
        currency="XTR",
        prices=[
            LabeledPrice(
                label="Подписка",
                amount=COST_VPN
            )
        ],
        start_parameter="one-month-sub",
    )


@router.message(F.successful_payment.invoice_payload.startswith("bay_server_"))
async def process_successful_payment(message: Message):
    payment_info = message.successful_payment
    location = payment_info.invoice_payload.split("_")[-1]# нужная информация "Локация"
    servers = await db_server.get_all_location_name(location_name=location)
    server_ip, server_id = await server_search(servers)

    name_user = str(uuid.uuid4())

    data = await add_user(
        api_token=API_BACKEND,
        ip=server_ip,
        name_user=name_user)

    date = datetime.now() + relativedelta(months=1)

    await db_vpn.add(user_id=message.from_user.id,file_name=name_user,data=data,date_break=date, server_id=server_id)

    await message.answer(f"Ваша ссылка для подключения:\n <code>{data}</code>",parse_mode=ParseMode.HTML)
    await message.answer("Вы купили Vpn", reply_markup=back_to_main)

@router.callback_query(F.data.startswith("extend_"))
async def bayes(callback_data: CallbackQuery):
    await callback_data.message.delete()
    await callback_data.answer()
    server_id = callback_data.data.split("_")[-1]

    await callback_data.message.answer_invoice(
        title=f"Продление VPN №'{server_id}'",
        description=f"Продление VPN №{server_id}на 1 месяц",
        payload="extend_" + server_id,
        provider_token="",
        currency="XTR",
        prices=[
            LabeledPrice(
                label="Подписка",
                amount=COST_VPN
            )
        ],
        start_parameter="one-month-sub",
    )


@router.message(F.successful_payment.invoice_payload.startswith("extend_"))
async def process_successful_payment(message: Message):
    payment_info = message.successful_payment
    id = payment_info.invoice_payload.split("_")[-1]
    date_old = await db_vpn.get_date_break(id)
    new_date_break = date_old + relativedelta(months=1)
    await db_vpn.update_date_break(id=id, new_date_break=new_date_break)

    await message.answer(f"Вы продлили vpn до {str(new_date_break.strftime("%Y.%m.%d")) + f" №{id}"}",reply_markup=back_to_main)



