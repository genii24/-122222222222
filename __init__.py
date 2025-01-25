from .start import register_start_handler
from .main_menu import register_main_menu_handler
from .slots import register_slots_handler
from .lobby import register_lobby_handler
from .bowling import register_bowling_handler  # Добавляем боулинг
from .football import register_football_handler  # Добавляем футбол
from .basketball import register_basketball_handler  # Добавляем баскетбол
from .dice import register_dice_handler  # Добавляем кубик
from .darts import register_darts_handler  # Добавляем дартс
from .pvp import register_pvp_handler  # Добавляем PvP


def register_handlers(bot):
    """
    Центральный метод для регистрации всех обработчиков.
    Он вызывается из main.py для подключения всех функций.
    """
    register_start_handler(bot)  # Обработчик стартового меню
    register_main_menu_handler(bot)  # Главное меню
    register_slots_handler(bot)  # Обработчик для слотов
    register_lobby_handler(bot)  # Лобби
    register_bowling_handler(bot)  # Боулинг
    register_football_handler(bot)  # Футбол
    register_basketball_handler(bot)  # Баскетбол
    register_dice_handler(bot)  # Кубик
    register_darts_handler(bot)  # Дартс
    register_pvp_handler(bot)  # PvP битвы