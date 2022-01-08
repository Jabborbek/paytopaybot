import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 total=None,file_name=None,path_url_send_file=None)
    except asyncpg.exceptions.UniqueViolationError:
        await db.select_user(telegram_id=message.from_user.id)

    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\n"
                         f"Faylni yuboring! (Diqqat (.db) fayl yuborilsin!)")
