import os
import asyncio
import logging
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, F, exceptions
from aiogram.filters import Command
import re

# Import logic from sibling files in api directory
from .fonts import FontTransformer
from .keyboards import get_font_keyboard

# Token setup
BOT_TOKEN = "8697512112:AAEm-Odf0_sKGdA_qSqefbkVVl4cB8a-VZA"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

PAGE_SIZE = 12 # 12 buttons per page is a good balance

def get_page_content_advanced(text: str, page: int):
    all_variants = FontTransformer.get_1000_variants(text)
    total_pages = (len(all_variants) + PAGE_SIZE - 1) // PAGE_SIZE
    
    start_idx = page * PAGE_SIZE
    end_idx = min(start_idx + PAGE_SIZE, len(all_variants))
    page_variants = all_variants[start_idx:end_idx]
    
    content = f"Sizning matningiz: <b>{text}</b>\n"
    content += f"Sahifa: {page + 1}/{total_pages}\n\n"
    content += "Shriftni tanlash uchun quyidagi tugmalarni bosing:"
    
    return content, total_pages, page_variants, start_idx

# Handlers
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    welcome_text = (
        "Salom! 👋\n\n"
        "Men siz yuborgan matnni 1000 dan ortiq chiroyli shriftlarga "
        "o'zgartirib bera olaman. ✨\n\n"
        "Istalgan matningizni yuboring:"
    )
    await message.answer(welcome_text)

@dp.message(F.text)
async def text_handler(message: types.Message):
    text = message.text.strip()
    if len(text) > 50: # Limit length for buttons
        await message.answer("Matn juda uzun. Iltimos, 50 belgidan kamroq matn yuboring.")
        return
    
    content, total_pages, variants, start_idx = get_page_content_advanced(text, 0)
    keyboard = get_font_keyboard(variants, 0, total_pages, start_idx)
    
    await message.answer(content, reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query(F.data.startswith("pg_"))
async def pagination_handler(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[1])
    
    # Extract original text
    msg_text = callback.message.text or callback.message.caption
    match = re.search(r"Sizning matningiz: (.*?)\n", msg_text)
    
    if not match:
        await callback.answer("Xatolik: Matn topilmadi.", show_alert=True)
        return
    
    original_text = match.group(1).strip()
    
    content, total_pages, variants, start_idx = get_page_content_advanced(original_text, page)
    keyboard = get_font_keyboard(variants, page, total_pages, start_idx)
    
    try:
        await callback.message.edit_text(content, reply_markup=keyboard, parse_mode="HTML")
    except exceptions.TelegramBadRequest:
        pass # Already on this page
    finally:
        await callback.answer()

@dp.callback_query(F.data.startswith("fnt_"))
async def font_select_handler(callback: types.CallbackQuery):
    index = int(callback.data.split("_")[1])
    
    # Extract original text
    msg_text = callback.message.text or callback.message.caption
    match = re.search(r"Sizning matningiz: (.*?)\n", msg_text)
    
    if not match:
        await callback.answer("Xatolik: Matn topilmadi.", show_alert=True)
        return
    
    original_text = match.group(1).strip()
    
    style_name, styled_text = FontTransformer.get_variant_by_index(original_text, index)
    
    response = f"<b>{style_name}</b> uslubidagi matn:\n\n"
    response += f"<code>{styled_text}</code>\n\n"
    response += "Nusxa olish uchun matn ustiga bosing."
    
    await callback.message.answer(response, parse_mode="HTML")
    await callback.answer(f"Tanlandi: {style_name}")

# FastAPI App
app = FastAPI()

@app.post("/api/index")
async def webhook(request: Request):
    update = types.Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/")
async def index():
    return {"message": "Bot is running with 1000+ fonts"}
