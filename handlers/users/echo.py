import random

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from asyncpg.exceptions import UniqueViolationError
from loader import db
from keyboards.inline.buttons import get_random_food_markup, get_menu_markup
from states import UserState


router = Router()


@router.callback_query(F.data == "get_random_food")
async def random_a_food(call: types.CallbackQuery):
    user = await db.select_user(telegram_id=call.from_user.id)
    random_food = random.choice(await db.select_user_foods(user.get("id")))
    await call.message.edit_text(
        f"Tanlangan ovqat: <b>{random_food.get('name')}</b>",
        reply_markup=get_random_food_markup,
    )


@router.callback_query(F.data == "see_menu")
async def see_menu(call: types.CallbackQuery, state: FSMContext):
    user = await db.select_user(telegram_id=call.from_user.id)
    markup = await get_menu_markup(user.get("id"))
    if markup:
        await call.message.edit_text(
            "Menu:",
            reply_markup=markup,
        )
        await state.set_state(UserState.menu)
    else:
        await call.message.edit_text("Sizning menuga hali taom qo'shilmagan. Taom qo'shish uchun uning nomini yozing.")
        await state.set_state(UserState.add_food)


@router.callback_query(UserState.menu)
async def menu_actions(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back":
        await call.message.edit_text("Bosh sahifa", reply_markup=get_random_food_markup)
    elif call.data == "get_random_food":
        await random_a_food(call)
    elif call.data == "add_food":
        await call.message.edit_text("Taom qo'shish uchun uning nomini yozing.")
        await state.set_state(UserState.add_food)


@router.message(UserState.add_food)
async def add_food(message: types.Message, state: FSMContext):
    user = await db.select_user(telegram_id=message.from_user.id)
    if message.text == "/tugadi":
        await state.clear()
        markup = await get_menu_markup(user.get("id"))
        if markup:
            await message.answer(
                "Menu:",
                reply_markup=markup,
            )
        else:
            await message.answer(
                f"Bosh sahifa",
                reply_markup=get_random_food_markup,
            )
    else:
        try:
            await db.add_food(user.get("id"), message.text)
            await message.answer(f"<b>{message.text}</b> menuga qo'shildi. Davom etish uchun yana taom nomini yozing, aks holda /tugadi buyrug'ini bering.")
        except UniqueViolationError:
            await message.answer(f"<b>{message.text}</b> allaqachon menuda mavjud. Yangi taom qo'shing.")
