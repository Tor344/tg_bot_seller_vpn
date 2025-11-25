from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="user",callback_data='user_inline_keyboard')]])

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[[KeyboardButton(text="user",callback_data='user_keyboard')]])


def my_vpn(vpns: list) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for vpn in vpns:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text=f"Дублировать {vpn.id} файл", callback_data=f'duplicate_file_{vpn.id}'),
                InlineKeyboardButton(text=f"Продлить {vpn.id} сервер", callback_data=f'extend_{vpn.id}')
            ]
        )
    inline_keyboard.append(
        [InlineKeyboardButton(text="На главную", callback_data='main')]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

back_to_main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="На главную", callback_data='main')]])

user_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[[KeyboardButton(text="user",callback_data='user_keyboard')]])