# handlers/start.py
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def register_start_handler(bot):
    @bot.message_handler(commands=['start'])
    def start_command(message):
        # Сохраняем ID пользователя в файл users.txt
        user_id = message.chat.id
        save_user_id(user_id)

        # Создаем inline-кнопку "Главное меню"
        markup = InlineKeyboardMarkup()
        main_menu_button = InlineKeyboardButton("👉 Главное меню", callback_data="main_menu")
        markup.add(main_menu_button)

        # Отправляем приветственное сообщение с inline-кнопкой
        bot.send_message(
            message.chat.id,
            "Добро пожаловать в бота! 👋\n\n"
            "Это честное онлайн казино! 🎰\n\n"
            "Нажмите “Главное меню”, чтобы продолжить:",
            reply_markup=markup
        )

    # Обработчик нажатия на inline-кнопку "Главное меню"
    @bot.callback_query_handler(func=lambda call: call.data == "main_menu")
    def handle_main_menu(call):
        from handlers.main_menu import create_main_menu
        create_main_menu(bot, call.message)


# Функция для сохранения ID пользователя в файл
def save_user_id(user_id):
    file_name = "users.txt"  # Имя файла для хранения ID пользователей
    try:
        # Читаем существующие ID из файла
        with open(file_name, "r") as file:
            existing_ids = file.read().splitlines()
    except FileNotFoundError:
        # Если файл ещё не существует, создаём пустой список
        existing_ids = []

    # Проверяем, что ID ещё не записан
    if str(user_id) not in existing_ids:
        with open(file_name, "a") as file:
            file.write(f"{user_id}\n")