import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Виртуальный баланс пользователей
user_balances = {}


def register_slots_handler(bot):
    # Главный обработчик для входа в режим "🎰 Casino Game"
    @bot.message_handler(func=lambda message: message.text == "🎰 Casino Game")
    def handle_slots_entry(message):
        # Проверка: если пользователь новый, устанавливаем стартовый баланс
        if message.chat.id not in user_balances:
            user_balances[message.chat.id] = 50  # Начальный баланс 50$

        balance = user_balances[message.chat.id]

        bot.send_message(
            message.chat.id,
            f"🎰 **Добро пожаловать в Casino Game!** 🎰\n\n"
            f"💵 Ваш текущий баланс: **${balance}.**\n\n"
            f"📝 Правила и множители выигрышей:\n"
            f"- 🍒 3 вишни: x1.5\n"
            f"- 🍋 3 лимона: x2\n"
            f"- 🍉 3 арбуза: x3\n"
            f"- BAR 3 символа BAR: x4\n"
            f"- 777 супер-комбинация: x10 (очень редкая!)\n\n"
            f"⚠️ Минимальная ставка: **3$**\n\n"
            f"Выберите готовую ставку или введите свою сумму:",
            parse_mode="Markdown",
            reply_markup=generate_bet_keyboard(),
        )

    # Генерация кнопок для выбора ставок
    def generate_bet_keyboard():
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("$3", callback_data="bet_3"),
            InlineKeyboardButton("$5", callback_data="bet_5"),
            InlineKeyboardButton("$10", callback_data="bet_10"),
        )
        keyboard.add(
            InlineKeyboardButton("$20", callback_data="bet_20"),
            InlineKeyboardButton("$50", callback_data="bet_50"),
        )
        keyboard.add(InlineKeyboardButton("💰 Указать свою ставку", callback_data="custom_bet"))
        return keyboard

    # Обработчик выбора ставки из кнопок
    @bot.callback_query_handler(func=lambda call: call.data.startswith("bet_"))
    def handle_bet_selection(call):
        bet_amount = int(call.data.split("_")[1])  # Извлекаем сумму ставки
        process_bet(call.message.chat.id, bet_amount, call.message, from_custom=False)

    # Обработчик для ввода пользовательской ставки
    @bot.callback_query_handler(func=lambda call: call.data == "custom_bet")
    def handle_custom_bet_request(call):
        bot.send_message(
            call.message.chat.id,
            "👉 *Напишите свою ставку (минимум $3) в сообщении.*",
            parse_mode="Markdown",
        )

    # Обработка текста для пользовательской ставки
    @bot.message_handler(func=lambda message: message.text.isdigit())
    def handle_text_bet(message):
        bet_amount = int(message.text)
        process_bet(message.chat.id, bet_amount, message, from_custom=True)

    # Обработка ставки
    def process_bet(user_id, bet_amount, message, from_custom=False):
        balance = user_balances.get(user_id, 50)

        if balance <= 0:
            bot.send_message(
                user_id,
                "😔 У вас закончились средства! Пожалуйста, вернитесь позже или пополните баланс.",
            )
            return

        if bet_amount < 3:
            bot.send_message(user_id, "⚠️ Минимальная ставка — $3. Попробуйте ещё раз.")
            return

        if bet_amount > balance:
            bot.send_message(
                user_id,
                f"⚠️ У вас недостаточно средств! Ваш баланс: **${balance}**.",
                parse_mode="Markdown",
            )
            return

        # Вычитаем ставку
        user_balances[user_id] -= bet_amount

        # Сообщение о сделанной ставке
        if from_custom:
            bot.send_message(
                user_id,
                f"✅ Вы указали свою ставку: **${bet_amount}**. 🎰\n"
                f"💵 Оставшийся баланс: **${user_balances[user_id]}.**\n\nЗапускаем слот-машину!",
                parse_mode="Markdown",
            )
        else:
            bot.edit_message_text(
                f"✅ Ваша ставка: **${bet_amount}**. 🎰\n"
                f"💵 Оставшийся баланс: **${user_balances[user_id]}.**\n\nЗапускаем слот-машину!",
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode="Markdown",
            )

        # Отправка анимации "🎰"
        sent_message = bot.send_dice(user_id, emoji="🎰")
        dice_value = sent_message.dice.value

        # Обработаем результат
        time.sleep(3)  # Ждём завершения анимации
        handle_slots_result(user_id, bet_amount, dice_value)

    # Таблица результатов "🎰"
    def get_slot_outcome(dice_value):
        outcomes = {
            1: ("🍒🍒🍒", 1.5),  # Вишни
            2: ("🍋🍋🍋", 2),  # Лимоны
            3: ("🍉🍉🍉", 3),  # Арбузы
            4: ("BAR BAR BAR", 4),  # BAR
            5: ("777", 10),  # Джекпот
        }
        return outcomes.get(dice_value, (None, 0))

    # Обработка результата игры
    def handle_slots_result(user_id, bet_amount, dice_value):
        combination, multiplier = get_slot_outcome(dice_value)

        # Если выиграл
        if combination and multiplier > 0:
            win_amount = round(bet_amount * multiplier, 2)  # Вычисляем выигрыш
            user_balances[user_id] += win_amount

            bot.send_message(
                user_id,
                f"🎉 *Поздравляем! Вы выиграли!*\n\n"
                f"🎰 Комбинация: {combination}\n"
                f"✨ Множитель: x{multiplier}\n"
                f"💵 Ваш выигрыш: **${win_amount}**\n"
                f"💳 Текущий баланс: **${user_balances[user_id]}**",
                parse_mode="Markdown",
            )
        else:
            bot.send_message(
                user_id,
                f"😢 Увы, вы ничего не выиграли.\n"
                f"💳 Текущий баланс: **${user_balances[user_id]}**.",
                parse_mode="Markdown",
            )

        # Снова предложим сыграть
        bot.send_message(user_id, "Хотите сыграть ещё раз?", reply_markup=generate_bet_keyboard())
