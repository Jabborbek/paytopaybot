from pathlib import Path
import os
from aiogram import types
from aiogram.types import CallbackQuery,InputFile
from data.config import ADMINS
from func.connect_to_db import connect_to_db_func
from func.key_code import get_hash_code
from keyboards.inline.product_keys import build_keyboard
from loader import dp, bot,db
from aiogram.types import LabeledPrice
from utils.misc.product import Product


path_url = "D:/Shaxsiy/paytopay/database"


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def doc_handler(message: types.Message):
    if message.document['file_name'].endswith('.db'):
        file_name=(message.document['file_name'])
        await db.update_file_name(file_name=file_name,telegram_id=message.from_user.id)
        download_path = Path().joinpath(f"{path_url}", f"{file_name}")
        await message.document.download(destination=download_path)
        price = await connect_to_db_func(path_url=path_url,file_name=file_name)
        caption = "<b>Test tekshirish uchun to'lov.</b>\n\n"
        caption += f"Jami to'lov miqdori: {price*1000} so'm\n"
        total = price*100000
        await db.update_user_tottal_price(total=int(total),telegram_id=message.from_user.id)
        photo_file = InputFile(path_or_bytesio="data/yadro.jpg")

        await bot.send_photo(chat_id=message.from_user.id, photo=photo_file,
                             caption=caption, reply_markup=build_keyboard("testamount"))

        await get_hash_code(path_url=path_url,file_name=file_name,user_id=message.from_user.id)

    else:
        await bot.send_message(chat_id=message.from_user.id, text="Bizga .db fayl yuboring!")


@dp.message_handler(content_types=['photo','video','audio','voice'])
async def see_message(message: types.Message):
    await message.answer("Bizga .db fayl yuboring!")


@dp.callback_query_handler(text="product:testamount")
async def praktikum_invoice(call: CallbackQuery):
    await call.message.delete()
    aaa = await db.select_user(telegram_id=call.from_user.id)
    test_check = Product(
        title="Testni tekshirish uchun to'lov",
        description="To'lov qilish uchun quyidagi tugmani bosing.",
        currency="UZS",
        prices=[
            LabeledPrice(
                label="Test tekshirish uchun to'lov",
                amount=int(aaa[2]),
            )
        ],
        start_parameter="create_invoice_test",
        need_name=True,
        need_phone_number=True,

    )


    await bot.send_invoice(chat_id=call.from_user.id,
                           **test_check.generate_invoice(),
                           payload="payload:testamount")
    await call.answer()

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    user = await db.select_user(telegram_id=pre_checkout_query.from_user.id)

    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                            ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                               text="To'lovingiz uchun rahmat!")


    await bot.send_document(chat_id=pre_checkout_query.from_user.id, document=InputFile(
            path_or_bytesio=user[5]))

    os.remove(f"{path_url}/{user[4]}")
    os.remove(f"{user[5]}")

    await bot.send_message(chat_id=ADMINS[0],
                               text=f"ID: {pre_checkout_query.id}\n"
                                    f"Telegram user: {pre_checkout_query.from_user.full_name}\n"                                
                                    f"Xaridor: {pre_checkout_query.order_info.name}\n"
                                    f"Tel: {pre_checkout_query.order_info.phone_number}\n"
                                    f"To'lov miqdori:  {user[2]/100} so'm")
