from core.world import load_balance_config, generate_world
from core.goods import load_goods
from models.player import Player
from models.courier import Courier
from models.wagon import Wagon
from ui.cli import show_main_menu
from core.game import Game

def main():
    print("=== Добро пожаловать в Торговый Дом! ===")

    # Загрузка конфигурации
    config = load_balance_config()

    # Генерация мира и товаров
    cities = generate_world(config)
    goods = load_goods(config)

    # Создание игрока
    player = Player(
        balance=config["player"]["starting_balance"],
        couriers=[
            Courier(
                name=courier_data["name"],
                endurance=courier_data["endurance"],
                illness_resistance=courier_data["illness_resistance"]
            ) for courier_data in config["player"]["starting_couriers"]
        ],
        wagons=[
            Wagon(
                name=wagon_data["name"],
                capacity=wagon_data["capacity"],
                durability=wagon_data["durability"]
            ) for wagon_data in config["player"]["starting_wagons"]
        ]
    )

    # Создание игры
    game = Game(player=player, cities=cities, goods=goods, config=config)

    # Запуск CLI-интерфейса
    show_main_menu(game)

if __name__ == "__main__":
    main()
