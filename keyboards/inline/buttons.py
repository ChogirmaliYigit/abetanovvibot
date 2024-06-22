from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db

inline_keyboard = [[
    InlineKeyboardButton(text="✅ Yes", callback_data='yes'),
    InlineKeyboardButton(text="❌ No", callback_data='no')
]]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

random_food_button = InlineKeyboardButton(text="Tasodifiy ovqat tanlash", callback_data="get_random_food")

back_button = InlineKeyboardButton(text="Orqaga", callback_data="back")

get_random_food_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            random_food_button,
            InlineKeyboardButton(text="Menu'ni ko'rish", callback_data="see_menu"),
        ],
    ],
)


add_food_button = InlineKeyboardButton(text="Taom qo'shish", callback_data="add_food")


async def get_menu_markup(user_id: int):
    keyboard = []
    for food in await db.select_user_foods(user_id):
        keyboard.append([
            InlineKeyboardButton(text=food.get("name"), callback_data=str(food.get("id"))),
        ])
    if keyboard:
        keyboard.append([random_food_button, add_food_button])
        keyboard.append([back_button])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    return None
