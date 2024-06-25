import random

from aiogram import Bot
from loader import db
from data.config import ADMINS


async def send_random_food(bot: Bot):
    users = await db.select_all_users()
    count = 0
    for user in users:
        random_food = random.choice(await db.select_user_foods(user.get("id")))
        try:
            await bot.send_message(user.get("telegram_id"), text=f"Tanlangan ovqat: <b>{random_food.get('name')}</b>")
            count += 1
        except Exception as exc:
            user_link = f"https://t.me/{user.get('username')}" if user.get('username') else f"tg://user?id{user.get('telegram_id')}"
            await bot.send_message(ADMINS[0], f"Tanlangan ovqat <a href='{user_link}'>{user.get('full_name', user.get('telegram_id'))}</a> ga yuborilmadi.\n\nXatolik ({exc.__class__.__name__}): {str(exc)[:3900]}")
    await bot.send_message(ADMINS[0], f"Tanlangan ovqat {count} ta foydalanuvchiga muvaffaqiyatli yuborildi!")
