from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ---------------- KONFIGURACJA ----------------
TOKEN = "8531618094:AAGtPF1ZFkn-NZ34ZjFjPShwVBtOB08Mz4k"
ADMIN_ID = 5877913952
BLIK_NUMBER = "572 630 288"
VIP_LINK = "https://t.me/+TvxUf2b2ybNjZWZk"
# ----------------------------------------------

# Start / menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💎 VIP miesięczny — 250 zł", callback_data="vip_month")],
        [InlineKeyboardButton("🏆 VIP Lifetime — 500 zł", callback_data="vip_life")],
        [InlineKeyboardButton("📘 Ebook Liquidity & Imbalance — 50 zł", callback_data="ebook_liq")],
        [InlineKeyboardButton("📗 Ebook Psychologia Tradingu — 50 zł", callback_data="ebook_psy")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Witaj w sklepie VIP Trading!\n\n"
        "Wybierz produkt, który chcesz kupić:",
        reply_markup=reply_markup
    )

# Obsługa wyboru produktu
async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    products = {
        "vip_month": "VIP MIESIĘCZNY",
        "vip_life": "VIP LIFETIME",
        "ebook_liq": "EBOOK LIQUIDITY & IMBALANCE",
        "ebook_psy": "EBOOK PSYCHOLOGIA TRADINGU",
    }

    product = products.get(query.data, "Produkt")
    context.user_data["product"] = product

    text = (
        f"🛒 Wybrałeś:\n*{product}*\n\n"
        f"📱 Wyślij BLIK na numer:\n👉 {BLIK_NUMBER}\n\n"
        "Po płatności wyślij tutaj *screena potwierdzenia* 📸"
    )

    await query.message.reply_text(text, parse_mode="Markdown")

# Obsługa screena
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    product = context.user_data.get("product", "NIEZNANY PRODUKT")

    caption = (
        f"🆕 NOWA PŁATNOŚĆ\n\n"
        f"👤 User: {user.first_name}\n"
        f"🆔 ID: {user.id}\n"
        f"🛒 Produkt: {product}"
    )

    keyboard = [
        [InlineKeyboardButton("✅ VIP MIESIĘCZNY", callback_data=f"accept_vip_month_{user.id}")],
        [InlineKeyboardButton("🏆 VIP LIFETIME", callback_data=f"accept_vip_life_{user.id}")],
        [InlineKeyboardButton("📘 EBOOK LIQUIDITY", callback_data=f"send_liq_{user.id}")],
        [InlineKeyboardButton("📗 EBOOK PSYCHO", callback_data=f"send_psy_{user.id}")],
        [InlineKeyboardButton("❌ ODRZUĆ", callback_data=f"reject_{user.id}")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=caption,
        reply_markup=reply_markup
    )

    await update.message.reply_text(
        "✅ Screen wysłany do weryfikacji.\n"
        "Poczekaj na potwierdzenie."
    )

# Obsługa przycisków admina
async def admin_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    parts = data.split("_")
    action = parts[0]
    user_id = int(parts[-1])

    if action == "accept":
        if "vip" in data:
            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    "🔥 PŁATNOŚĆ POTWIERDZONA!\n\n"
                    "Witamy w VIP 😈\n\n"
                    f"👉 LINK DO GRUPY:\n{VIP_LINK}"
                )
            )
            await query.message.reply_text("✅ VIP wysłany klientowi")

    elif action == "send":
        if "liq" in data:
            await context.bot.send_document(
                chat_id=user_id,
                document=open("liquidity.pdf", "rb"),
                caption="📘 Ebook Liquidity & Imbalance\nMiłej nauki 🔥"
            )
            await query.message.reply_text("✅ Ebook Liquidity wysłany")

        elif "psy" in data:
            await context.bot.send_document(
                chat_id=user_id,
                document=open("psychologia.pdf", "rb"),
                caption="📗 Ebook Psychologia Tradingu\nMiłej nauki 🔥"
            )
            await query.message.reply_text("✅ Ebook Psychologia wysłany")

    elif action == "reject":
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Płatność odrzucona.\nSkontaktuj się z administratorem."
        )
        await query.message.reply_text("❌ Płatność odrzucona")

# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_choice, pattern="^(vip|ebook)"))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(admin_actions))

    print("🔥 BOT PRO DZIAŁA...")
    app.run_polling()

if __name__ == "__main__":
    main()
