from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
import logging
from YandexIOT import SmartHome

from configs import YA_TOKEN, NIGHT_LAMP_ID, SOCKET_ID, HUMIDIFIER_ID

logger = logging.getLogger(__name__)
home = SmartHome(YA_TOKEN)

#Фунцкия результата действия с устройством
async def action_result(update: Update, success: bool, action: str, device_name: str):
    if success:
        await update.message.reply_text(f"✅ Результат: {device_name}, {action}")
    else:
        await update.message.reply_text(f"❌ Результат: {device_name}, {action}")

async def debug_devices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        devices = home.get_devices()
        if not devices:
            await update.message.reply_text("Нет устройств или ошибка получения списка.")
            return
        # Выведем информацию о первом устройстве
        first = devices[0]
        await update.message.reply_text(f"Тип первого устройства: {type(first)}\nАтрибуты: {dir(first)}")
        # Далее пробуем вывести имена, если есть
        msg = "📋 Устройства из YandexIOT:\n"
        for d in devices:
            # Попробуем разные варианты получения имени
            name = getattr(d, 'name', None) or getattr(d, '_name', None) or getattr(d, 'device_name', None) or str(d)
            msg += f"• {name} (ID: {d.id})\n"
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# --- Socket Actions ---

async def socket_on(update, context: ContextTypes.DEFAULT_TYPE):
    try:
        device_name = home.get_device_by_id(SOCKET_ID)
        device_name.turn_on()
        await update.message.reply_text("Розетка включена")
        logger.info(f"Socket ({SOCKET_ID}) is ON, by user {update.effective_user.id}")
    except Exception as er:
        logger.error(f"Error for socket: {er}")
        await update.message.reply_text("Failed to turn on the Socket")

async def socket_off(update, context: ContextTypes.DEFAULT_TYPE):
    try:
        device_name = home.get_device_by_id(SOCKET_ID)
        device_name.turn_off()
        await update.message.reply_text("Розетка выключена")
        logger.info(f"Socket ({SOCKET_ID}) is OFF, by user {update.effective_user.id}")
    except Exception as er:
        logger.error(f"Error for socket: {er}")
        await update.message.reply_text("Failed to turn off the Socket")

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
    logger.info(f"Запрошен статус пользователем {update.effective_user.id}, {update.effective_user.first_name}")
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
