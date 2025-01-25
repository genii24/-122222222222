import os
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Глобальное хранилище активных игр
active_games = {}


def register_lobby_handler(bot):
    @bot.message_handler(func=lambda message: message.text == "🏠 Лобби")
    def show_lobby(message):
        create_lobby_menu(bot, message)

    # Обработчик кнопки "📂 Открытые игры"
    @bot.callback_query_handler(func=lambda call: call.data == "open_games")
    def show_open_games(call):
        open_games = read_games_from_file("games.txt")

        if not open_games:
            bot.send_message(
                call.message.chat.id,
                "🔍 **Нет доступных игр. Создайте новую игру!**",
                parse_mode="Markdown"
            )
        else:
            for game in open_games:
                if game["status"] == "waiting":
                    markup = InlineKeyboardMarkup()
                    join_button = InlineKeyboardButton(
                        f"Присоединиться ({game['amount']} USDT)",
                        callback_data=f"join_game_{game['id']}"  # Привязываем ID игры к кнопке
                    )
                    markup.add(join_button)

                    bot.send_message(
                        call.message.chat.id,
                        f"🕹️ **Игра:** {game['game']}\n"
                        f"👤 **Создатель:** {game['username']} (ID: {game['user_id']})\n"
                        f"💵 **Сумма участия:** {game['amount']} USDT\n",
                        reply_markup=markup,
                        parse_mode="Markdown"
                    )

    # Обработчик кнопки "Присоединиться"
    @bot.callback_query_handler(func=lambda call: call.data.startswith("join_game_"))
    def join_game(call):
        open_games = read_games_from_file("games.txt")
        game_id = int(call.data.split("_")[-1])  # Извлекаем ID игры из callback_data

        # Ищем игру по ID
        selected_game = next((game for game in open_games if game["id"] == game_id), None)
        if not selected_game or selected_game["status"] != "waiting":
            bot.answer_callback_query(call.id, "❌ Игра недоступна.")
            return

        # Инициализация матча: добавляем в активные игры
        active_games[game_id] = {
            "creator_id": selected_game["user_id"],
            "opponent_id": call.from_user.id,
            "game": selected_game["game"],
            "emoji_moves": {},
            "score": {selected_game["user_id"]: 0, call.from_user.id: 0}  # Счёт игроков
        }

        # Отправляем сообщение о старте игры
        bot.send_message(
            call.message.chat.id,
            f"🎮 Игра '{selected_game['game']}' началась!\n"
            f"👤 Создатель игры: {selected_game['user_id']}\n"
            f"👥 Противник: {call.from_user.id}\n\n"
            "Победит тот, кто забьёт 10 очков первым! Кидайте баскетбольные смайлики 🏀 или общайтесь свободно!"
        )

        start_game(bot, game_id)


# Логика начала и общения
def start_game(bot, game_id):
    game = active_games[game_id]
    creator_id = game["creator_id"]
    opponent_id = game["opponent_id"]

    # Обработчик сообщений между игроками
    @bot.message_handler(func=lambda message: message.from_user.id in [creator_id, opponent_id])
    def handle_messages(message):
        player_id = message.from_user.id
        game = active_games.get(game_id)

        # Если сообщение не подходит под эту игру
        if not game:
            return

        # Баскетбол: если игрок кидает смайл 🏀 или 🤾‍♂️
        if message.text in ["🏀", "🤾‍♂️"]:
            handle_basketball_move(bot, message, game_id)
            return

        # Свободное общение: пересылаем сообщение сопернику
        opponent_id = game["creator_id"] if player_id == game["opponent_id"] else game["opponent_id"]
        bot.send_message(opponent_id, f"📩 Сообщение от вашего соперника:\n\n{message.text}")


# Баскетбольная механика
def handle_basketball_move(bot, message, game_id):
    game = active_games[game_id]
    player_id = message.from_user.id

    # Если игрок уже сделал ход (использовал баскетбольный смайлик)
    if game["emoji_moves"].get(player_id):
        bot.send_message(player_id, "❌ Вы уже сделали ход в этом раунде! Ждём соперника!")
        return

    # Записать ход игрока
    game["emoji_moves"][player_id] = message.text
    bot.send_message(player_id, "✔️ Ваш ход засчитан, ждём соперника!")

    # Проверяем, сделали ли оба игрока ход
    if len(game["emoji_moves"]) == 2:
        process_round(bot, game_id)


# Обработка результатов раунда
def process_round(bot, game_id):
    game = active_games[game_id]
    creator_id = game["creator_id"]
    opponent_id = game["opponent_id"]

    # Случайно выбираем, кто забил гол
    scorer = random.choice([creator_id, opponent_id])
    game["score"][scorer] += 1

    # Отправить результаты игрокам
    bot.send_message(
        creator_id,
        f"🎮 Результаты раунда:\n"
        f"🏀 Победил: {'Создатель' if scorer == creator_id else 'Противник'}\n"
        f"Счёт: {game['score'][creator_id]} : {game['score'][opponent_id]}"
    )
    bot.send_message(
        opponent_id,
        f"🎮 Результаты раунда:\n"
        f"🏀 Победил: {'Вы' if scorer == opponent_id else 'Ваш соперник'}\n"
        f"Счёт: {game['score'][creator_id]} : {game['score'][opponent_id]}"
    )

    # Очистка ходов
    game["emoji_moves"].clear()

    # Проверка на завершение игры
    if game["score"][creator_id] >= 10 or game["score"][opponent_id] >= 10:
        end_game(bot, game_id)


# Завершение игры
def end_game(bot, game_id):
    game = active_games[game_id]
    creator_id = game["creator_id"]
    opponent_id = game["opponent_id"]

    # Определяем победителя
    if game["score"][creator_id] > game["score"][opponent_id]:
        winner = creator_id
    else:
        winner = opponent_id

    # Сообщаем игрокам об окончании игры
    bot.send_message(
        creator_id,
        f"🏆 Игра завершена! Итоговый счёт: "
        f"{game['score'][creator_id]}:{game['score'][opponent_id]}\n"
        f"Победитель: {'Вы' if winner == creator_id else 'Ваш соперник'}!"
    )
    bot.send_message(
        opponent_id,
        f"🏆 Игра завершена! Итоговый счёт: "
        f"{game['score'][creator_id]}:{game['score'][opponent_id]}\n"
        f"Победитель: {'Вы' if winner == opponent_id else 'Ваш соперник'}!"
    )

    # Удаляем игру из активных
    del active_games[game_id]


# Функция для чтения игр из файла
def read_games_from_file(filename):
    if not os.path.exists(filename):
        return []

    games = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i, line in enumerate(lines, start=1):
            game_data = line.strip().split("|")
            if len(game_data) == 5:
                games.append({
                    "id": i,
                    "user_id": int(game_data[0]),
                    "username": game_data[1],
                    "game": game_data[2],
                    "status": game_data[3],
                    "amount": float(game_data[4])
                })
    return games


# Создание меню лобби
def create_lobby_menu(bot, message):
    markup = InlineKeyboardMarkup()
    btn_bowling = InlineKeyboardButton("🎳 Боулинг", callback_data="select_game_bowling")
    btn_football = InlineKeyboardButton("⚽️ Футбол", callback_data="select_game_football")
    btn_basketball = InlineKeyboardButton("🏀 Баскетбол", callback_data="select_game_basketball")
    open_games_button = InlineKeyboardButton("📂 Открытые игры", callback_data="open_games")
    markup.add(btn_bowling, btn_football, btn_basketball)
    markup.add(open_games_button)

    bot.send_message(
        message.chat.id,
        "🏠 **Добро пожаловать в Лобби!**\n\n"
        "Вы можете выбрать мини-игру для создания:\n\n"
        "🎳 Боулинг\n"
        "⚽️ Футбол\n"
        "🏀 Баскетбол\n\n"
        "Или просмотреть 📂 **Открытые игры** и присоединиться к ним!",
        reply_markup=markup,
        parse_mode="Markdown"
    )