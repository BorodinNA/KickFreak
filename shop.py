import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Замените на Telegram ID создателя (администратора) бота
ADMIN_ID = 7533975681


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start.
    Отправляет сообщение с инструкцией и клавиатурой, содержащей кнопку 'Старт'.
    """
    keyboard = [["Старт"]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    text = (
        "Заполните всю необходимую информацию:\n"
        "1) ИМЯ, ФАМИЛИЯ, ОТЧЕСТВО\n"
        "2) Город, Область(Край и т.п)\n"
        "3) Адрес\n"
        "4) Ваш почтовый индекс\n"
        "5) Мобильный телефон\n"
        "6) Название интересующего товара\n"
        "7) Размер\n"
        "Оправьте всю информацию ответом на это сообщение"
    )
    await update.message.reply_text(text, reply_markup=reply_markup)


async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик текстовых сообщений.
    Если сообщение является ответом на сообщение с инструкцией,
    пересылает информацию о пользователе и текст сообщения админу,
    а также отправляет пользователю сообщение с напоминанием.
    """
    if (
        update.message.reply_to_message
        and "Заполните всю необходимую информацию:"
        in update.message.reply_to_message.text
    ):
        user = update.message.from_user
        # Собираем информацию о пользователе
        user_info = f"ID: {user.id}\nИмя: {user.first_name}"
        if user.last_name:
            user_info += f" {user.last_name}"
        if user.username:
            user_info += f"\nUsername: @{user.username}"

        # Формируем сообщение для администратора
        admin_text = (
            f"Получено сообщение от пользователя:\n{user_info}\n\n"
            f"Сообщение:\n{update.message.text}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text)

        # Отправляем сообщение пользователю с напоминанием
        await update.message.reply_text(
            "Информация отправлена. Если в течение 2 часов не поступит ответа от магазина или же если у вас закрыты личные сообщения, напишите @KickFreak_Sup."
        )


def main() -> None:
    """
    Основная функция для запуска бота.
    """
    # Замените токен ниже на токен вашего бота
    application = (
        Application.builder()
        .token("7516780980:AAH2I8e_w3Piozz-U8embNcO9G-lPCU0x0A")
        .build()
    )

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply)
    )

    # Запускаем бота
    application.run_polling()


if __name__ == "__main__":
    main()
