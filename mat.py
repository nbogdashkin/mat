import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re
import datetime

TOKEN = "ВАШ_ТОКЕН_ОТ_БОТА"

# Пример мата
blacklist = ["хуй", "пизда", "блять", "сука", "ебан", "гандон", "мразь", "уебок", "пидор", "долбоеб"]

# Инициализация логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚓 Мент на месте. Мат не пройдет!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    user = update.effective_user

    if any(re.search(rf"\b{word}\b", message_text) for word in blacklist):
        until = datetime.datetime.now() + datetime.timedelta(hours=24)
        try:
            await context.bot.restrict_chat_member(
                chat_id=update.effective_chat.id,
                user_id=user.id,
                permissions={"can_send_messages": False},
                until_date=until
            )
            await update.message.reply_text(f"🧨 {user.first_name}, ты в муте на 24 часа за мат.")
        except Exception as e:
            await update.message.reply_text("❗ Не удалось замьютить. Может, у меня нет прав.")
    else:
        logging.info("Сообщение без мата")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
