from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мои VPN", callback_data='my_vpn')],
    [InlineKeyboardButton(text="Выбрать VPN для покупки", callback_data='choose_server')],
    [InlineKeyboardButton(text="Поддержка", callback_data='support')],
    [InlineKeyboardButton(text="Инструкция", callback_data='instructions')]
])

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[[KeyboardButton(text="start",callback_data='start_keyboard')]])

