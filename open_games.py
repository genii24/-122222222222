import random


# Функция для чтения ID игр
def read_open_games():
    games = [
        {"id": 1, "player1": 7016453953, "player2": None, "status": "waiting"},
        {"id": 2, "player1": 123456789, "player2": None, "status": "waiting"}
    ]
    return games


# Хранилище активных игр
active_games = {}


# Функция присоединения игрока к доступной игре
def join_game(player_id, game_id):
    games = read_open_games()

    # Поиск игры с нужным ID
    selected_game = next((game for game in games if game["id"] == game_id), None)

    if not selected_game:
        print("❌ Игра с данным ID не найдена.")
        return

    if selected_game["status"] != "waiting" or selected_game["player2"] is not None:
        print(f"❌ Игра с ID {game_id} уже недоступна для присоединения.")
        return

    # Игрок присоединяется
    selected_game["player2"] = player_id
    selected_game["status"] = "in_progress"
    print(f"🎮 Игрок {player_id} присоединился к игре с ID {game_id}!")

    # Регистрируем активную игру
    active_games[game_id] = {
        "player1": selected_game["player1"],
        "player2": selected_game["player2"],
        "player1_score": 0,
        "player2_score": 0
    }

    # Запускаем процесс игры
    play_game(game_id)


# Логика игры (до 3 очков)
def play_game(game_id):
    game = active_games[game_id]
    print(f"🎮 Игра началась! Игроки {game['player1']} и {game['player2']}.")

    while True:
        for player in ["player1", "player2"]:
            success = random.choice([True, False])  # 50% шанс забить
            if success:
                active_games[game_id][f"{player}_score"] += 1
                print(f"Игрок {game[player]} забивает! 🎯")
            else:
                print(f"Игрок {game[player]} промахнулся 💨.")

            # Проверяем победителя
            if active_games[game_id][f"{player}_score"] == 3:
                print(f"🏆 Победитель: Игрок {game[player]}!")
                del active_games[game_id]  # Удаляем активную игру
                return


# Пример использования
join_game(9876543210, 1)  # Игрок с ID 9876543210 присоединяется к игре с ID 1