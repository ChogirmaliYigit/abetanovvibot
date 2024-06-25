import random

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from asyncpg.exceptions import UniqueViolationError
from loader import db
from keyboards.inline.buttons import get_random_food_markup, get_menu_markup
from states import UserState


router = Router()


@router.callback_query(F.data == "get_random_food")
async def random_a_food(call: types.CallbackQuery, state: FSMContext):
    user = await db.select_user(telegram_id=call.from_user.id)
    user_foods = await db.select_user_foods(user.get("id"))
    if user_foods:
        random_food = random.choice(user_foods)
        await call.message.edit_text(
            f"Tanlangan ovqat: <b>{random_food.get('name')}</b>",
            reply_markup=get_random_food_markup,
        )
    else:
        await call.message.edit_text("Sizning menuga hali taom qo'shilmagan. Taom qo'shish uchun uning nomini yozing.")
        await state.set_state(UserState.add_food)


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
    user = await db.select_user(telegram_id=call.from_user.id)
    if call.data == "back":
        await call.message.edit_text("Bosh sahifa", reply_markup=get_random_food_markup)
    elif call.data.startswith("change_"):
        await call.message.edit_text("Taom uchun yangi nom kiriting:")
        await state.update_data({"food_id": int(call.data.split("_")[-1])})
        await state.set_state(UserState.edit_food)
    elif call.data.startswith("delete_"):
        await db.delete_food(food_id=int(call.data.split("_")[-1]))
        await see_menu(call, state)
    elif call.data == "get_random_food":
        await random_a_food(call)
    elif call.data == "add_food":
        await call.message.edit_text("Taom qo'shish uchun uning nomini yozing.")
        await state.set_state(UserState.add_food)


@router.message(UserState.edit_food)
async def edit_food(message: types.Message, state: FSMContext):
    data = await state.get_data()
    food_id = data.get("food_id")
    try:
        await db.update_food_name(message.text, food_id)
        await message.answer(f"<b>{message.text}</b> endi menuda🥳")
        user = await db.select_user(telegram_id=message.from_user.id)
        markup = await get_menu_markup(user.get("id"))
        if markup:
            await message.answer(
                "Menu:",
                reply_markup=markup,
            )
            await state.set_state(UserState.menu)
        else:
            await message.answer(
                "Sizning menuga hali taom qo'shilmagan. Taom qo'shish uchun uning nomini yozing.")
            await state.set_state(UserState.add_food)
    except UniqueViolationError:
        await message.answer(f"<b>{message.text}</b> allaqachon menuda mavjud. Yangi taom qo'shing.")


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
            await state.set_state(UserState.menu)
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
