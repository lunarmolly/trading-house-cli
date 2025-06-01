import os
from core.world import load_balance_config, generate_world
from core.goods import load_goods
from models.player import Player
from models.courier import Courier
from models.wagon import Wagon
from ui.cli import show_main_menu
from core.game import Game


def select_difficulty() -> str:
    print("\nВыберите уровень сложности:")
    print("1. Легкий (меньше рисков, больше ресурсов)")
    print("2. Средний (стандартный баланс)")
    print("3. Сложный (высокие риски, меньше ресурсов)")

    while True:
        choice = input("Введите номер (1-3): ")
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "normal"
        elif choice == "3":
            return "hard"
        print("Ошибка: введите 1, 2 или 3")



def main():
    print("=== Добро пожаловать в Торговый Дом! ===")

    # Выбор сложности
    difficulty = select_difficulty()

    # Проверка пути к конфигурации
    config_path = "data/balance_config.json"
    if not os.path.exists(config_path):
        print(f"Предупреждение: файл {config_path} не найден, пробую корневую директорию...")
        config_path = "balance_config.json"

    # Загрузка конфигурации
    config = load_balance_config(path=config_path, difficulty=difficulty)

    # Проверка наличия необходимых ключей
    if "player" not in config:
        raise RuntimeError("Конфигурационный файл не содержит раздела 'player'")

    if "difficulty_settings" not in config:
        print("Предупреждение: в конфигурации отсутствуют настройки сложности")

    # Создание игрока с проверкой наличия множителей
    starting_balance = config["player"]["starting_balance"]
    if "difficulty_settings" in config and difficulty in config["difficulty_settings"]:
        settings = config["difficulty_settings"][difficulty]
        if "starting_balance_multiplier" in settings:
            starting_balance *= settings["starting_balance_multiplier"]

    couriers = []
    for courier_data in config["player"].get("starting_couriers", []):
        illness_resistance = courier_data.get("illness_resistance", 1.0)
        if "difficulty_settings" in config and difficulty in config["difficulty_settings"]:
            settings = config["difficulty_settings"][difficulty]
            if "illness_resistance_multiplier" in settings:
                illness_resistance *= settings["illness_resistance_multiplier"]


        couriers.append(Courier(
            name=courier_data["name"],
            endurance=courier_data.get("endurance", 0),
            illness_resistance=illness_resistance
        ))

    # Генерация мира и товаров
    cities = generate_world(config)
    goods = load_goods(config)

    # Создание игрока
    player = Player(
        balance=starting_balance,
        couriers=couriers,
        wagons=[
            Wagon(
                name=wagon_data["name"],
                capacity=wagon_data["capacity"],
                durability=wagon_data.get("durability", 0.75)
            ) for wagon_data in config["player"].get("starting_wagons", [])
        ]
    )

    # Создание игры
    game = Game(player=player, cities=cities, goods=goods, config=config, difficulty=difficulty)

    # Запуск CLI-интерфейса
    show_main_menu(game)


if __name__ == "__main__":
    main()