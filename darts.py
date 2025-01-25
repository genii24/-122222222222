def register_darts_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "select_game_darts")
    def handle_darts_game(call):
        bot.send_message(
            call.message.chat.id,
            "🎯 **Вы выбрали мини-игру: Дартс!**\n"
            "Скоро стартует игра, оставайтесь на связи! 😊",
            parse_mode="Markdown"
        )