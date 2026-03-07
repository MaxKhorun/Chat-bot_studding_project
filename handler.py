import asyncio

from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
import logging
from YandexIOT import SmartHome

from configs import YA_TOKEN, NIGHT_LAMP_ID, SOCKET_ID, HUMIDIFIER_ID

logger = logging.getLogger(__name__)
home = SmartHome(YA_TOKEN)


# Фунцкия результата действия с устройством
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

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     logger.info(f"Пользователь {user.first_name} (id: {user.id}) заустил бота")
#     await update.message.reply_text(
#         f"Привет, {user.first_name}!\n"
#         "Я бот для умного дома.\n"
#         "Доступные команды:\n"
#         "/help — напомнить о доступных командах\n"
#         "/status — текущее состояние системы\n"
#         "/light — операции со светом\n"
#         "/vacuum — операции с пылесосом\n"
#         "/humi — операции с увлажнителем\n"
#         "/plug — операции с розеткой\n"
#     )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} (id: {user.id}) запустил бот")
    messages = [
        "Умею я немного; вы можете пользоваться только теми командами, которые я укажу:",
        "Действуйте последовательно, следуйте моим командам, и у нас всё получится. =)",
        "Если готовы, то все поцелуйтесь и жмите - /8_marta"]
    await update.message.reply_text(
        f"Привет, {user.first_name}!\n"
        "Это бот для поиска подарка на 8-е марта."
    )
    await asyncio.sleep(1.5)
    for t in messages:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=t,
        )
        await asyncio.sleep(1)

async def startEihgtMarch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} (id: {user.id}) кликнул /8_marta")
    await update.message.reply_text(
        f"Начинаем поиски!\n"
        "Думаю, что нужно проверить балкон для начала 🤔.\n"
        "Радужный кот не так прост, как кажется 🤔😉.\n"
    )
    await asyncio.sleep(1.5)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Когда будете готовы идти дальше, кликайте вот это - /next 👍"
    )

async def next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} (id: {user.id}) клинул /next")
    messages = [
        "Следующая подсказка в машине - 100% 😎",
        """
        Теперь точно пора одеваться для путешествия, из которого вернемся вечером.\nСобираем сумки, закрываем дверь и выбегаем на улицу к машине!
        """,
        "Как доберётесь, загляните в бардачок. Когда всё найдете и будете готовы двигаться дальше, кликайте снова сюда - /go! 👍"
    ]
    await update.message.reply_text(
        f"Отлично! 🌷\n"
        "Это нам, возможно, понадобится -> берем с собой на всякий случай.\n"
    )
    await asyncio.sleep(1.5)
    for t in messages:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=t
        )
        await asyncio.sleep(1)

async def go(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} (id: {user.id}) клинул /go")
    await update.message.reply_text(
        "Ну, супер же! 🌷\n"
        "Нас ожидает небольшая поездка, расслабляемся и получаем 100% удовольствия 😎")
    await  asyncio.sleep(1.5)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Буду ожидать вас на месте. 😉\n"
        "Как доберётесь, и будете готовы выходить из машины, кликайте - /i_m_here! 👍.\n"
    )

# async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info(f"Запрошен статус пользователем {update.effective_user.id}, {update.effective_user.first_name}")
#     await update.message.reply_text(
#         "🏠 **Состояние умного дома**\n"
#         "🌡 Температура: +22.5°C\n"
#         "💡 Свет в гостиной: выключен\n"
#         "🔌 Розетки: все отключены\n"
#         "🚪 Дверь: закрыта",
#         parse_mode="Markdown"
#     )

# async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info(f"Запрошен статус пользователем {update.effective_user.id}, {update.effective_user.first_name}")
#     await update.message.reply_text(
#         "🏠 **Состояние умного дома**\n"
#         "🌡 Температура: +22.5°C\n"
#         "💡 Свет в гостиной: выключен\n"
#         "🔌 Розетки: все отключены\n"
#         "🚪 Дверь: закрыта",
#         parse_mode="Markdown"
#     )

# async def help():
#

async def i_m_here(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} (id: {user.id}) клинул /i_m_here")
    await update.message.reply_text(
        "Тили-тили! Трали-вали!🌷\n"
        "Мы на месте, как я понимаю. Двигаемся дальше, но прежде... 😎")
    await  asyncio.sleep(1.5)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=("На улице теплее, чем зимой, но всё ещё прохладно.\n"
              "Чтобы продолжать, нужно подготовиться. ☝️\n"
              "Оглянитесь и посмотрите, нет ли по-близости подходящего 'Свитера', чтобы согреться. 😉\n"
              "Когда найдёте, то поймёте, надеюсь, что делать.\n"
              "\n"
              "Жми, если считаешь, что пора  -> /go_ahead. А мы проверим, так ли это. 😅")
    )

async def go_ahead(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} (id: {user.id}) клинул /go_ahead")
    await update.message.reply_text(
        "Итак...\n"
        "Если вы всё поняли и нажали, но ещё на улице, то бегом ТУДА! 😁\n"
        "Если вы на месте, то нужно расположиться с комфортом прежде, чем продолжать дальше.😉\n"
    )
    await  asyncio.sleep(1.5)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""Если вы уже сидите - /napoleon_forever жми и готовимся к финалу =)"""
    )

async def napoleon_forever(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} (id: {user.id}) клинул /napoleon_forever")
    await update.message.reply_text(
        "Мы находимся на самой важной стадии. ☝️\n"
        "Нужно выбрать, чем будем завтракать, и какой Наполеон будем кушать! 😁\n"
        "Приступаем! Выбираем! 💪\n"
        "Выберете и жмите /ready_for_desert смело!"
    )

async def desert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} (id: {user.id}) клинул /ready_for_desert")
    messages = [
        "Выбрали?",
        "Мо-лод-цы! 😁",
        "💪\n",
        "Теперь... Кушаем, сидим, ждем, терпим. Ожидаем финальных знаков, так как мы в конце пути, зайки.😘\nВозвращайтесь, когда дойдёте до десерта =)"
        "\nBon appetit!"
    ]
    for t in messages:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=t
        )
        await asyncio.sleep(1)
    await asyncio.sleep(1.5)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="А как будете готовы к десерту - давите на /final, чтобы выяснить, гже же они - последние сюрпризы! 🎁♥️"
    )

async def finalStep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} (id: {user.id}) клинул /final")
    messages = [
        "Попросите у вашего папы безмен. 🤣",
        "Зачем?",
        "НУ-Ж-НО! 💪",
        "Срочно бежим в машину и открываем багажник. 🏃‍♀️‍➡️",
        "Взвешиваем пакеты.🕵️‍♀️ В среднем ищем конверт, сыщики мои -> в нём последний ключ. 😜",
        "С 8-м Марта! Люблю вас! 😘"
    ]

    for t in messages:

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=t
    )
        await asyncio.sleep(2)
