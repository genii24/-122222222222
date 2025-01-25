from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def register_pvp_handler(bot):
    """
    Регистрация обработчика для кнопки "⚔️ PvP Битва".
    """

    @bot.message_handler(func=lambda message: message.text == "⚔️ PvP Битва")
    def pvp_menu(message):
        """
        Обработчик для перехода в меню PvP.
        """
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        # Добавляем кнопки для выбора PvP режимов
        btn_slots = KeyboardButton("⚔️ PvP: Slots")  # PvP режим "Slots"
        btn_miner = KeyboardButton("⚔️ PvP: Miner")  # PvP режим "Miner"
        btn_back = KeyboardButton("🔙 Назад")  # Кнопка для возврата в главное меню

        # Добавляем кнопки в раскладку
        markup.add(btn_slots, btn_miner, btn_back)

        # Отправляем пользователю сообщение с выбором режимов
        bot.send_message(
            message.chat.id,
            "⚔️ **Добро пожаловать в меню PvP битв!** ⚔️\n\n"
            "Выберите один из доступных PvP режимов для сражения:\n\n"
            "🎰 **PvP: Slots** — испытайте удачу в сражениях на слотах.\n"
            "⛏️ **PvP: Miner** — соревнуйтесь в добыче ресурсов.\n\n"
            "🔙 Нажмите 'Назад', чтобы вернуться в главное меню.",
            parse_mode="Markdown",
            reply_markup=markup
        )