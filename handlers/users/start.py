from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from loader import db, bot
from data.config import ADMINS
from utils.extra_datas import make_title
from keyboards.inline.buttons import get_random_food_markup


router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message):
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    user = await db.select_user(telegram_id=telegram_id)
    if not user:
        try:
            user = await db.add_user(telegram_id=telegram_id, full_name=full_name, username=username)
        except Exception as error:
            logger.info(error)
    if user:
        if not user.get("is_active"):
            await db.update_is_active(telegram_id)
        count = await db.count_users()
        user_link = f"https://t.me/{username}" if username else f"tg://user?id={user['telegram_id']}"
        msg = f"[{make_title(user['full_name'])}]({user_link}) bazaga qo'shildi\.\nBazada {count} ta foydalanuvchi bor\."
    else:
        user_link = f"https://t.me/{username}" if username else f"tg://user?id={telegram_id}"
        msg = f"[{make_title(full_name)}]({user_link}) bazaga oldin qo'shilgan"
    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=msg,
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
            )
        except Exception as error:
            logger.info(f"Data did not send to admin: {admin}. Error: {error}")
    await message.answer(
        f"Assalomu alaykum {make_title(full_name)}\!",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_random_food_markup,
    )
