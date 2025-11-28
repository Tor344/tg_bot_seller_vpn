from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

admin_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="admin",callback_data='admin_inline_keyboard')]])

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[[KeyboardButton(text="admin",callback_data='admin_keyboard')]])

back_to_main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="На главную", callback_data='main')]])

def extend_vpn(vpn_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"Продлить {vpn_id} сервер", callback_data=f'extend_{vpn_id}')]])