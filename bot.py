from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

TOKEN = "8222244787:AAFuTiNUENXTDSvp04qP2KWLVC10NyyHRwU"

user_data = {}

# 👉 ВІТАЛЬНИЙ ТЕКСТ
WELCOME_TEXT = (
    "⛵ Вітаємо у вітрильній школі!\n\n"
    "⚓ Навчання, тренування, команда, змагання\n"
    "🌊 Діти від 8 років\n\n"
    "Оберіть дію 👇"
)

# 👉 КНОПКИ МЕНЮ
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("⛵ Записатися", callback_data="register")],
        [InlineKeyboardButton("ℹ️ Інфо", callback_data="info")],
        [InlineKeyboardButton("📞 Контакти", callback_data="contacts")],
    ]
    return InlineKeyboardMarkup(keyboard)

# 👉 СЕГМЕНТАЦІЯ
def get_group(age: int):
    if age <= 12:
        return "🟡 Оптиміст"
    elif 13 <= age <= 15:
        return "🔵 ILCA Intro"
    else:
        return "🔴 ILCA / Спортивна група"

# 👉 СТАРТ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {}

    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=get_main_keyboard()
    )

# 👉 ОБРОБКА КНОПОК
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    if query.data == "register":
        user_data[chat_id] = {}
        await query.message.reply_text("⛵ Як звати дитину?")

    elif query.data == "info":
        await query.message.reply_text(
            "ℹ️ Інформація:\n\n"
            "⛵ Вітрильна школа для дітей\n"
            "📅 Тренування 2-3 рази на тиждень\n"
            "🏆 Участь у змаганнях\n"
            "👨‍🏫 Досвідчені тренери"
        )

    elif query.data == "contacts":
        await query.message.reply_text(
            "📞 Контакти:\n\n"
            "📱 Телефон: +380983877121\n"
            "📍 Черкаси, яхт-клуб\n"
            "💬 Telegram: @Kozatski_vitryla_bot"
        )

# 👉 ОСНОВНА ЛОГІКА АНКЕТИ
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_data:
        user_data[chat_id] = {}

    data = user_data[chat_id]

    # ІМ'Я
    if "name" not in data:
        data["name"] = text
        await update.message.reply_text("🎂 Вік дитини?")

    # ВІК
    elif "age" not in data:
        try:
            age = int(text)
        except ValueError:
            await update.message.reply_text("❗ Введіть вік цифрами")
            return

        data["age"] = age
        data["group"] = get_group(age)

        await update.message.reply_text("📏 Зріст дитини (см)?")

    # ЗРІСТ
    elif "height" not in data:
        try:
            height = int(text)
        except ValueError:
            await update.message.reply_text("❗ Введіть зріст цифрами")
            return

        data["height"] = height
        await update.message.reply_text("⚖️ Вага дитини (кг)?")

    # ВАГА
    elif "weight" not in data:
        try:
            weight = int(text)
        except ValueError:
            await update.message.reply_text("❗ Введіть вагу цифрами")
            return

        data["weight"] = weight
        await update.message.reply_text("📞 Ваш номер телефону?")

    # ТЕЛЕФОН
    elif "phone" not in data:
        data["phone"] = text

        # клієнту
        await update.message.reply_text(
            f"✅ Дякуємо!\n\n"
            f"👶 Ім’я: {data['name']}\n"
            f"🎂 Вік: {data['age']}\n"
            f"📏 Зріст: {data['height']} см\n"
            f"⚖️ Вага: {data['weight']} кг\n"
            f"⛵ Група: {data['group']}\n"
            f"📞 Телефон: {data['phone']}\n\n"
            f"Ми зв’яжемось з вами 👌"
        )

        # тренеру
        await context.bot.send_message(
            chat_id=557139758,
            text=(
                f"🚨 НОВА ЗАЯВКА!\n\n"
                f"👶 Ім’я: {data['name']}\n"
                f"🎂 Вік: {data['age']}\n"
                f"📏 Зріст: {data['height']} см\n"
                f"⚖️ Вага: {data['weight']} кг\n"
                f"⛵ Група: {data['group']}\n"
                f"📞 Телефон: {data['phone']}"
            )
        )

        print("Нова заявка:", data)

    print("Нова заявка:", data)
# 👉 ЗАПУСК
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()