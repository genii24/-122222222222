

import random


def register_bowling_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "select_game_bowling")
    def handle_bowling_game(call):
        bot.send_message(
            call.message.chat.id,
            "🎳 **Вы выбрали мини-игру: Боулинг!**\n"
            "Отправьте эмодзи 🎳 (боулинг), чтобы сделать бросок и узнать результат!",
            parse_mode="Markdown"
        )

    # Обрабатываем сообщение с эмодзи 🎳
    @bot.message_handler(func=lambda message: message.text == "🎳")
    def play_bowling(message):
        # Генерируем случайный результат боулинга
        result = random.randint(0, 10)

        # Обрабатываем особые случаи
        if result == 10:
            message_result = "🎳 🎉 Страйк! Вы сбили все 10 кеглей! Отличный бросок!"
        elif result == 0:
            message_result = "🎳 😢 Вы не сбили ни одной кегли! Попробуйте ещё раз."
        else:
            message_result = f"🎳 Вы сбили **{result} из 10 кеглей!**"

        # Отправляем сообщение с результатом пользователю
        bot.send_message(
            message.chat.id,
            message_result,
            parse_mode="Markdown"
        )
