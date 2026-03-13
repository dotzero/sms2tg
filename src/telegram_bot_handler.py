from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from src.conf import TG_CHAT_ID, TG_TOKEN
from src.sim868_cmd import setup_module


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.id != TG_CHAT_ID:
        await update.message.reply_text("🛑 Доступ запрещен")
        return

    await update.message.reply_text("🏓 pong")


async def setup_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.id != TG_CHAT_ID:
        await update.message.reply_text("🛑 Доступ запрещен")
        return

    try:
        await setup_module()
    except Exception as e:
        await update.message.reply_text(f"🛑 Ошибка: {str(e)}")


async def start_bot_polling():
    application = Application.builder().token(TG_TOKEN).build()

    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("setup", setup_cmd))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
