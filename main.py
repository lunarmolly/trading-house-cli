import os
from core.world import load_balance_config, generate_world
from core.goods import load_goods
from models.player import Player
from models.courier import Courier
from models.wagon import Wagon
from core.game import Game
from ui.cli import show_main_menu, select_difficulty


def load_game_config(difficulty: str) -> dict:
    """Загрузка и проверка конфигурации с учетом сложности"""
    config_path = "data/balance_config.json"
    if not os.path.exists(config_path):
        config_path = "balance_config.json"

    try:
        config = load_balance_config(path=config_path, difficulty=difficulty)

        if "player" not in config:
            print("Ошибка: Конфигурационный файл не содержит раздела 'player'")
            raise RuntimeError("Отсутствует раздел 'player' в конфигурации")

        return config
    except Exception as e:
        print(f"Ошибка: Не удалось загрузить конфигурацию: {str(e)}")
        raise


def create_player(config: dict, difficulty: str) -> Player:
    """Создание игрока с учетом уровня сложности"""
    # Настройки баланса
    starting_balance = config["player"]["starting_balance"]
    if "difficulty_settings" in config and difficulty in config["difficulty_settings"]:
        settings = config["difficulty_settings"][difficulty]
        starting_balance = int(starting_balance * settings.get("starting_balance_multiplier", 1.0))

    # Создание курьеров
    couriers = []
    for courier_data in config["player"].get("starting_couriers", []):
        illness_resistance = courier_data.get("illness_resistance", 1.0)
        if "difficulty_settings" in config and difficulty in config["difficulty_settings"]:
            settings = config["difficulty_settings"][difficulty]
            illness_resistance *= settings.get("illness_resistance_multiplier", 1.0)

        couriers.append(Courier(
            name=courier_data["name"],
            endurance=courier_data.get("endurance", 0),
            illness_resistance=illness_resistance
        ))

    # Создание повозок
    wagons = [
        Wagon(
            name=wagon_data["name"],
            capacity=wagon_data["capacity"],
            durability=wagon_data.get("durability", 0.75)
        ) for wagon_data in config["player"].get("starting_wagons", [])
    ]

    return Player(
        balance=starting_balance,
        couriers=couriers,
        wagons=wagons
    )


def main():
    # Выбор сложности через CLI
    difficulty = select_difficulty()

    # Загрузка конфигурации
    try:
        config = load_game_config(difficulty)
    except:
        return

    # Генерация мира и товаров
    cities = generate_world(config)
    goods = load_goods(config)

    # Создание игрока
    player = create_player(config, difficulty)

    # Инициализация игры
    game = Game(player=player, cities=cities, goods=goods, config=config, difficulty=difficulty)

    # Запуск CLI интерфейса
    show_main_menu(game)


if __name__ == "__main__":
    main()