# -*- coding: utf-8 -*-
"""
Davlat Botu — Telegram bot
===========================

Foydalanuvchi davlat nomini yozadi, bot esa uning bayrog'i, poytaxti,
millati, tili, dini, pul birligi, davlat rahbari va maydoni haqida
ma'lumot beradi.

Ishga tushirish uchun README.md faylini o'qing.
"""

import html
import logging
import os
import random
import re
from difflib import get_close_matches

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from countries_data import COUNTRIES, COUNTRIES_BY_ID, POPULAR_IDS

# ---------------------------------------------------------------------------
# Sozlamalar
# ---------------------------------------------------------------------------

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("davlat-botu")

APOSTROPHES = re.compile(r"[\'’ʻʼ'`]")
WHITESPACE = re.compile(r"\s+")


# ---------------------------------------------------------------------------
# Yordamchi funksiyalar
# ---------------------------------------------------------------------------

def normalize(text: str) -> str:
    """Foydalanuvchi kiritgan matnni solishtirish uchun standart shaklga keltiradi."""
    text = text.lower().strip()
    text = APOSTROPHES.sub("", text)
    text = WHITESPACE.sub(" ", text)
    return text


def find_country(query: str):
    """Aniq moslikni qidiradi (alias ro'yxati bo'yicha)."""
    norm = normalize(query)
    if not norm:
        return None
    for country in COUNTRIES:
        if norm in country["aliases"]:
            return country
    return None


def find_suggestions(query: str, limit: int = 3):
    """Aniq mos kelmasa, imlosi yaqin davlatlarni taklif qiladi."""
    norm = normalize(query)
    if not norm:
        return []
    alias_to_country = {}
    for country in COUNTRIES:
        for alias in country["aliases"]:
            alias_to_country[alias] = country
    close = get_close_matches(norm, alias_to_country.keys(), n=limit, cutoff=0.72)
    seen_ids = set()
    results = []
    for alias in close:
        country = alias_to_country[alias]
        if country["id"] not in seen_ids:
            seen_ids.add(country["id"])
            results.append(country)
    return results


def random_popular(count: int = 4):
    pool = [COUNTRIES_BY_ID[i] for i in POPULAR_IDS]
    return random.sample(pool, k=min(count, len(pool)))


def country_keyboard(countries) -> InlineKeyboardMarkup:
    rows = []
    row = []
    for country in countries:
        row.append(
            InlineKeyboardButton(
                f"{country['flag']} {country['name']}",
                callback_data=f"country:{country['id']}",
            )
        )
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def format_country_card(country: dict) -> str:
    e = html.escape
    lines = [
        f"{country['flag']} <b>{e(country['name'])}</b>  —  ✅ <i>topildi</i>",
        "",
        f"📍 <b>Poytaxti:</b> {e(country['capital'])}",
        f"👥 <b>Millati:</b> {e(country['nationality'])}",
        f"🗣 <b>Tili:</b> {e(country['language'])}",
        f"✨ <b>Dini:</b> {e(country['religion'])}",
        f"💰 <b>Pul birligi:</b> {e(country['currency'])}",
        f"🏛 <b>Davlat rahbari:</b> {e(country['leader'])}",
        f"📐 <b>Maydoni:</b> {e(country['area'])}",
        "",
        "<i>Namunaviy maʼlumot — 2026-yil holatiga koʻra.</i>",
    ]
    return "\n".join(lines)


async def send_country_card(target_message, country: dict) -> None:
    await target_message.reply_html(
        format_country_card(country),
        reply_markup=None,
    )


# ---------------------------------------------------------------------------
# Handlerlar
# ---------------------------------------------------------------------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Salom! 👋 Men <b>Davlat Botu</b>man.\n\n"
        "Menga biror davlat nomini yozing — masalan <b>Yaponiya</b> yoki "
        "<b>Oʻzbekiston</b> — men sizga uning bayrogʻi, poytaxti, millati, "
        "tili, dini, pul birligi, rahbari va maydoni haqida maʼlumot beraman.\n\n"
        "Barcha mavjud davlatlar roʻyxati uchun /royxat buyrugʻidan foydalaning.\n\n"
        "Yoki quyidagi tugmalardan birini tanlang:"
    )
    await update.message.reply_html(
        text,
        reply_markup=country_keyboard(random_popular()),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "ℹ️ <b>Yordam</b>\n\n"
        "Menga istalgan davlat nomini yozing (oʻzbek yoki inglizcha nomi bilan), "
        "men sizga u haqida qisqacha maʼlumot beraman.\n\n"
        "Buyruqlar:\n"
        "/start — botni qayta ishga tushirish\n"
        "/royxat — barcha mavjud davlatlar roʻyxati\n"
        "/help — ushbu yordam xabari"
    )
    await update.message.reply_html(text)


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    names = sorted(f"{c['flag']} {c['name']}" for c in COUNTRIES)
    text = "📋 <b>Bazadagi davlatlar</b> ({}):\n\n{}".format(
        len(COUNTRIES), "\n".join(names)
    )
    await update.message.reply_html(text)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = (update.message.text or "").strip()
    if not query:
        return

    country = find_country(query)
    if country:
        await send_country_card(update.message, country)
        return

    suggestions = find_suggestions(query)
    if suggestions:
        text = (
            f"🔎 <b>Topilmadi</b>\n\n"
            f"«{html.escape(query)}» nomli davlat aniq topilmadi. "
            f"Ehtimol, siz shuni nazarda tutgandirsiz:"
        )
        await update.message.reply_html(
            text, reply_markup=country_keyboard(suggestions)
        )
        return

    text = (
        f"🔎 <b>Topilmadi</b>\n\n"
        f"«{html.escape(query)}» nomli davlat bazada topilmadi. "
        f"Imloni tekshiring yoki quyidagilardan birini tanlang:"
    )
    await update.message.reply_html(
        text, reply_markup=country_keyboard(random_popular())
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data or ""
    if not data.startswith("country:"):
        return
    country_id = data.split(":", 1)[1]
    country = COUNTRIES_BY_ID.get(country_id)
    if not country:
        return
    await query.message.reply_html(format_country_card(country))


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Update %s ishlov berishda xatolik yuz berdi", update, exc_info=context.error)


# ---------------------------------------------------------------------------
# Ishga tushirish
# ---------------------------------------------------------------------------

def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit(
            "BOT_TOKEN topilmadi.\n"
            "1) .env.example faylini .env nomiga nusxalang\n"
            "2) .env ichidagi BOT_TOKEN qiymatiga @BotFather bergan tokenni yozing\n"
            "3) Botni qayta ishga tushiring."
        )

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("royxat", list_command))
    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_error_handler(error_handler)

    logger.info("Davlat Botu ishga tushdi — %d ta davlat bazada.", len(COUNTRIES))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
