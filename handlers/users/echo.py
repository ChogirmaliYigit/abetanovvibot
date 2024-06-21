import random

from aiogram import Router, types, F
from loader import db
from keyboards.inline.buttons import get_random_food_markup, get_menu_markup


router = Router()


@router.callback_query(F.data == "get_random_food")
async def random_a_food(call: types.CallbackQuery):
    random_food = random.choice(await db.select_all_foods())
    await call.message.edit_text(
        f"Tanlangan ovqat: <b>{random_food.get('name')}</b>",
        reply_markup=get_random_food_markup,
    )


@router.callback_query(F.data == "see_menu")
async def see_menu(call: types.CallbackQuery):
    await call.message.edit_text(
        "Menu:",
        reply_markup=await get_menu_markup(),
    )


@router.message(F.text == "/menu")
async def command_see_menu(message: types.Message):
    await message.answer(
        "Menu:",
        reply_markup=await get_menu_markup(),
    )
