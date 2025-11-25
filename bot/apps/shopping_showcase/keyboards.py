from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="shopping_showcase",callback_data='shopping_showcase_inline_keyboard')]])

def all_servers(locations: list) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for location in locations:
        inline_keyboard.append(
            [InlineKeyboardButton(text=f"Купить сервер {location.name} ", callback_data=f'bay_server_{location.name}')])

    inline_keyboard.append(
        [InlineKeyboardButton(text="На главную", callback_data='main')])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[[KeyboardButton(text="shopping_showcase",callback_data='shopping_showcase_keyboard')]])
