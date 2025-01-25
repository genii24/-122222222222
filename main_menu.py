from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from handlers import register_pvp_handler  # Импорт обработчика PvP из __init__.py


def register_main_menu_handler(bot):
    @bot.message_handler(func=lambda message: message.text == "Главное меню")
    def show_main_menu(message):
        create_main_menu(bot, message)

    # Регистрируем PvP при подключении главного меню
    register_pvp_handler(bot)


def create_main_menu(bot, message):
    # Создаем главное меню с кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    # Создание кнопок
    btn_slots = KeyboardButton("🎰 Casino Game")  # Переименовали кнопку
    btn_lobby = KeyboardButton("🏠 Лобби")
    btn_referral = KeyboardButton("🤝 Реф. система")
    btn_profile = KeyboardButton("👤 Профиль")
    btn_top = KeyboardButton("🏆 Топ")
    btn_pvp = KeyboardButton("⚔️ PvP битва")  # Новая кнопка для PvP битвы

    # Группируем кнопки на две кнопки в строке
    markup.add(btn_slots, btn_lobby, btn_referral, btn_profile, btn_top, btn_pvp)

    # Отправляем меню с ярким описанием
    bot.send_message(
        message.chat.id,
        "✨ **Добро пожаловать в Главное меню!** ✨\n\n"
        "Выберите одну из доступных категорий для продолжения:\n\n"
        "🎰 **Casino Game** — попробуйте свою удачу в играх!\n"
        "🏠 **Лобби** — общайтесь и находите новые игры.\n"
        "🤝 **Реф. система** — зовите друзей и получайте бонусы.\n"
        "👤 **Профиль** — следите за своими достижениями.\n"
        "🏆 **Топ** — узнайте, кто на вершине рейтинга.\n"
        "⚔️ **PvP битва** — сразитесь с другими игроками и докажите, что вы лучший!\n\n"
        "👉 Выберите один из пунктов ниже, чтобы начать!",
        parse_mode="Markdown",
        reply_markup=markup
    )