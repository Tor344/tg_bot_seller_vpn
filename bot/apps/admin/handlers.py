from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.database.crud import db_server, db_location, db_admin
from aiogram.enums import ParseMode

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    # if not(db_admin.is_admin(message.from_user.id)):
    #     return
    await message.answer("""
    Здесь вы можете работать с базой данных
    1. <code>add_server</code> {ip сервера} {локация сервера}
    2. <code>add_location</code> {место положение}
    3. <code>add_admin</code> {id админа}
    4. <code>delete_admin</code> {id админа}
    5. <code>get_vpn</code> {имя vpn} {время работы vpn в формате YYYY:MM:DD} {Локация} {Тип vpn}
    6. <code>add_vpn_type</code> {id админа}
    """,parse_mode=ParseMode.HTML)

@router.message(F.text.startswith("add_server "))
async def admin_panel(message: Message):
    # if not(db_admin.is_admin(message.from_user.id)):
    #     return
    ip, location_name = message.text.split(" ")[-2:]
    result = await db_server.add(ip=ip, location_name=location_name)
    if not result:
        await message.answer("В чем то проблем")
        return
    await message.answer("Успешно добавлен сервер")


@router.message(F.text.startswith("add_location "))
async def admin_panel(message: Message):
    # if not(db_admin.is_admin(message.from_user.id)):
    #     return
    name = message.text.split(" ")[-1]

    await db_location.add(name=name)
    await message.answer("Успешно добавлена локация")



@router.message(F.text.startswith("add_admin "))
async def admin_panel(message: Message):
    # if not (db_admin.is_admin(message.from_user.id)):
    #     return

    admin = await db_admin.add(id=message.from_user.id)

    if not admin:
        await message.answer("уже есть такой админ")
        return
    await message.answer("Админ успешно добавлен")


@router.message(F.text.startswith("delete_admin "))
async def admin_panel(message: Message):
    # if not (db_admin.is_admin(message.from_user.id)):
    #     return
    admin = await db_admin.delete(id=message.from_user.id)
    if not admin:
        await message.answer("Нет такого админа")
        return
    await message.answer('Админ успешно удален')


#Нужно сначала написать Api агента
# @router.message(F.text.startswith("get_vpn "))
# async def admin_panel(message: Message):
#     if not (db_admin.is_admin(message.from_user.id)):
#         return
#
#     name_user, date, location = message.text.split(" ")[-3:]
#     servers = await db_server.get_all_for_name(location)
#     server_ip, server_id = await src.server_search.server_search(servers)
#     stop_flag = asyncio.Event()
#
#     task = asyncio.create_task(progress_message_editor(msg, stop_flag))
#
#     count_vpn = await db.get_count_vpn(callback_data.from_user.id)
#     name_user = str(callback_data.from_user.id) + "_" + str(count_vpn)
#
#     data = request_to_backend.add_user(
#         api_token=API_BACKEND,
#         ip=server_ip,
#         name_user=name_user
#     )
#
#     date_break = (datetime.today() + relativedelta(months=1)).strftime("%Y.%m.%d")
#     await db_vpn.add(tg_id=callback_data.from_user.id, data=data, date_break=date_break, server_id=server_id)
#     stop_flag.set()
#     await callback_data.message.delete()
#     await asyncio.sleep(0.1)
#     file_bytes = data.encode('utf-8')  # конвертация строки в байты
#     input_file = BufferedInputFile(file_bytes, filename='open.vpn')
#     await callback_data.message.answer_document(document=input_file)
#     await callback_data.message.answer("Ваш файл", reply_markup=back_to_main)
