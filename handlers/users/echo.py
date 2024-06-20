import random

from aiogram import Router, types
from loader import db
from keyboards.inline.buttons import get_random_food_markup


router = Router()


@router.callback_query()
async def random_a_food(call: types.CallbackQuery):
    random_food = random.choice(await db.select_all_foods())
    await call.message.edit_text(
        f"Tanlangan ovqat: <b>{random_food.get('name')}</b>",
        reply_markup=get_random_food_markup,
    )
