import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Путь к файлу для хранения игр
GAMES_FILE = "games.txt"


# Функция записи новой игры в файл
def write_open_game(game):
    """
    Записывает информацию об игре в файл GAMES_FILE.
    """
    with open(GAMES_FILE, "a", encoding="utf-8") as file:
        file.write(f"{game['user_id']}|{game['username']}|{game['game']}|{game['status']}|{game['amount']}\n")


# Проверяем наличие файла игр, создаем его, если он не существует
if not os.path.exists(GAMES_FILE):
    with open(GAMES_FILE, "w", encoding="utf-8") as file:
        pass  # Создаем пустой файл


# Регистрируем обработчик для игры "Баскетбол"
def register_basketball_handler(bot):
    # Шаг 1: Обработчик выбора "Баскетбол"
    @bot.callback_query_handler(func=lambda call: call.data == "select_game_basketball")
    def ask_for_amount(call):
        # Просим у пользователя указать сумму в USDT
        bot.send_message(
            call.message.chat.id,
            "🏀 **Игра 'Баскетбол' выбрана!**\n\n"
            "Пожалуйста, укажите сумму в USDT для участия в игре.",
            parse_mode="Markdown"
        )

        # Ожидаем ответа от пользователя
        bot.register_next_step_handler(call.message, create_basketball_game)

    # Шаг 2: Обработчик для создания игры с суммой
    def create_basketball_game(message):
        try:
            # Пытаемся преобразовать введённый текст в число (сумма в USDT)
            amount = float(message.text)

            if amount <= 0:
                raise ValueError("Сумма должна быть больше 0.")

            # Информация об игре
            game_info = {
                "user_id": message.chat.id,
                "username": message.from_user.username if message.from_user.username else "Без имени",
                "game": "Баскетбол",
                "amount": amount,  # Указанная сумма
                "status": "waiting"  # Игра ожидает второго игрока
            }

            # Сохраняем игру в файл GAMES_FILE
            write_open_game(game_info)

            # Сообщаем пользователю об успешном создании игры
            bot.send_message(
                message.chat.id,
                f"🏀 **Игра 'Баскетбол' успешно создана!**\n\n"
                f"💵 Сумма участия: {amount} USDT\n\n"
                "Теперь другие пользователи смогут присоединиться к вашей игре через раздел 📂 **Открытые игры**.",
                parse_mode="Markdown"
            )
        except ValueError:
            # Если пользователь ввёл некорректное значение, просим повторить ввод
            bot.send_message(
                message.chat.id,
                "❌ **Некорректное значение суммы. Пожалуйста, укажите числовое значение суммы в USDT.**"
            )
            bot.register_next_step_handler(message, create_basketball_game)  # Снова ожидаем корректный ввод