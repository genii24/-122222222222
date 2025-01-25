def register_dice_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "select_game_dice")
    def handle_dice_game(call):
        bot.send_message(
            call.message.chat.id,
            "🎲 **Вы выбрали мини-игру: Кубик!**\n"
            "Скоро стартует игра, оставайтесь на связи! 😊",
            parse_mode="Markdown"
        )