import argparse

from core.world import load_balance_config, generate_world
from core.goods import load_goods
from models.player import Player
from models.courier import Courier
from models.wagon import Wagon
from core.game import Game
from ui.gui import TradeHouseGUI


def main():
    print("=== ДОБРО ПОЖАЛОВАТЬ В ТОРГОВЫЙ ДОМ! ===")

    config = load_balance_config()
    #Генерация мира и товаров
    cities = generate_world(config)
    goods = load_goods(config)

    #Создание игрока
    player = Player(
        balance=config["player"]["starting_balance"],
        couriers=[
            Courier(**courier_data) for courier_data in config["player"]["starting_couriers"]
        ],
        wagons=[
            Wagon(**wagon_data) for wagon_data in config["player"]["starting_wagons"]
        ]
    )

    #Инициализация игры
    game = Game(player=player, cities=cities, goods=goods, config=config)

    #Запуск GUI
    app = TradeHouseGUI(game)
    app.mainloop()


if __name__ == "__main__":
    main()