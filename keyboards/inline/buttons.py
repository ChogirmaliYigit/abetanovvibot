from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db

inline_keyboard = [[
    InlineKeyboardButton(text="✅ Yes", callback_data='yes'),
    InlineKeyboardButton(text="❌ No", callback_data='no')
]]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

random_food_button = InlineKeyboardButton(text="Tasodifiy ovqat tanlash", callback_data="get_random_food")

get_random_food_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            random_food_button,
            InlineKeyboardButton(text="Menu'ni ko'rish", callback_data="see_menu"),
        ],
    ],
)


async def get_menu_markup():
    keyboard = []
    for food in await db.select_all_foods():
        keyboard.append([
            InlineKeyboardButton(text=food.get("name"), callback_data=str(food.get("id"))),
        ])
    keyboard.append([random_food_button])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
