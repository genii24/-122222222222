def register_football_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "select_game_football")
    def handle_football_game(call):
        bot.send_message(
            call.message.chat.id,
            "⚽️ **Вы выбрали мини-игру: Футбол!**\n"
            "Скоро стартует игра, оставайтесь на связи! 😊",
            parse_mode="Markdown"
        )