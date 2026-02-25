from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} (id: {user.id}) заустил бота")
    await update.message.reply_text(
        f"Привет, {user.first_name}!\n"
        "Я бот для умного дома.\n"
        "Доступные команды:\n"
        "/help — напомнить о доступных командах\n"
        "/status — текущее состояние системы\n"
        "/light — операции со светом\n"
        "/vacuum — операции с пылесосом\n"
        "/humi — операции с увлажнителем\n"
        "/plug — операции с розеткой\n"
    )
    
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Запрошен статус пользователем {update.effective_user.id}")
    await update.message.reply_text(
        "🏠 **Состояние умного дома**\n"
        "🌡 Температура: +22.5°C\n"
        "💡 Свет в гостиной: выключен\n"
        "🔌 Розетки: все отключены\n"
        "🚪 Дверь: закрыта",
        parse_mode="Markdown"
    )
    
# async def help():
#
