import asyncio
from datetime import datetime
import uuid

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery,BufferedInputFile,LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command

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
    location = callback_data.data.split("_")[-1]

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
    print(payment_info.invoice_payload)# нужная информация "Локация"
    await message.answer("Вы купили Vpn",reply_markup=back_to_main)

    # server_ip, server_id = await server_search(servers)
    #
    # name_user = str(uuid.uuid4())
    #
    # response = await add_user(
    #     api_token=API_BACKEND,
    #     ip=server_ip,
    #     name_user=name_user)
    #
    # data = response.get("data")
    # type = response.get("type")
    # date = datetime.now()
    #
    # await db_vpn.add(user_id=callback_data.from_user.id,name_user=name_user,data=data,date_break=date, server_id=1,type=type)
    # if type == "ovpn":
    #     file_bytes = data.encode('utf-8')  # конвертация строки в байты
    #     input_file = BufferedInputFile(file_bytes, filename='open.vpn')
    #     await callback_data.message.answer_document(document=input_file)
    #     await callback_data.message.answer("Ваш файл",reply_markup=back_to_main)
    # else:
    #     await callback_data.message.answer(f"Ваша ссылка для подключения:<code>{data}</code>",reply_markup=back_to_main)


@router.callback_query(F.data.startswith("extend_"))
async def bayes(callback_data: CallbackQuery):
    await callback_data.message.delete()
    await callback_data.answer()
    server_id = callback_data.data.split("_")[-1]

    await callback_data.message.answer_invoice(
        title=f"Продление  VPN №'{server_id}'",
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
    print(payment_info.invoice_payload)# нужная информация "Локация"
    server_id = payment_info.invoice_payload.split("_")[-1]
    await message.answer(f"Вы продлили vpn до {"Какого то числа" + f"№{server_id}"}",reply_markup=back_to_main)



