import random
from typing import List, Optional
from models.city import City
from models.goods_item import GoodsItem
from models.player import Player
from models.caravan import Caravan
from models.courier import Courier
from models.wagon import Wagon

class Game:
    """
    Класс для управления основным игровым процессом.
    """

    def __init__(self, player: Player, cities: List[City], goods: List[GoodsItem], config: dict):
        """
        Инициализация игры.

        Args:
            player (Player): Игрок.
            cities (List[City]): Города мира.
            goods (List[GoodsItem]): Все доступные товары.
            config (dict): Конфигурационные данные.
        """
        self.player = player
        self.cities = cities
        self.goods = goods
        self.config = config
        self.current_cycle = 1
        self.max_cycles = config["player"]["cycles_to_win"]
        self.victory_goal = config["player"]["victory_goal"]
        self.active_caravans: List[Caravan] = []

    def next_cycle(self) -> None:
        """
        Переход к следующему игровому циклу.
        """
        self.current_cycle += 1
        self.update_city_events()

    def update_city_events(self) -> None:
        """
        Обновляет события для всех городов.
        """
        names = [e["name"] for e in self.config["city_events"]]
        weights = [e["probability"] for e in self.config["city_events"]]
        for city in self.cities:
            city.current_event = random.choices(names, weights=weights, k=1)[0]

    def is_game_over(self) -> bool:
        """
        Проверяет завершение игры.

        Returns:
            bool: True, если достигнута цель или исчерпаны циклы.
        """
        return self.current_cycle > self.max_cycles or self.player.balance >= self.victory_goal

    def has_won(self) -> bool:
        """
        Проверяет, достиг ли игрок цели.

        Returns:
            bool: True при победе.
        """
        return self.player.balance >= self.victory_goal

    def form_caravan(
        self,
        courier: Courier,
        wagon: Wagon,
        goods_selection: dict,
        city: City
    ) -> Caravan:
        """
        Создаёт караван, рассчитывает циклы прибытия и возврата.

        Args:
            courier (Courier): Курьер.
            wagon (Wagon): Повозка.
            goods_selection (dict): Товары.
            city (City): Город назначения.

        Returns:
            Caravan: Новый караван.
        """
        departure_cycle = self.current_cycle
        travel_time = city.distance
        arrival_cycle = departure_cycle + travel_time
        return_cycle = arrival_cycle + 1 + travel_time

        caravan = Caravan(
            courier=courier,
            wagon=wagon,
            goods=goods_selection,
            destination=city,
            days_to_travel=travel_time,
            departure_cycle=departure_cycle,
            arrival_cycle=arrival_cycle,
            return_cycle=return_cycle
        )

        self.active_caravans.append(caravan)
        return caravan

    def update_caravans(self) -> None:
        """
        Обновляет все активные караваны: применяет события, завершает миссии.
        """
        from core.caravan import update_caravan_event_once, process_completed_caravan
        goods_dict = {g.name: g for g in self.goods}
        finished = []

        for caravan in self.active_caravans:
            update_caravan_event_once(caravan, self.current_cycle, self.config)

            report, done = process_completed_caravan(
                caravan=caravan,
                player=self.player,
                current_cycle=self.current_cycle,
                goods_dict=goods_dict,
                config=self.config
            )

            if done:
                print("Караван завершён:")
                print("  Событие в пути:", report["event_path"])
                print("  Событие в городе:", report["event_city"])
                for name, data in report["sale_breakdown"].items():
                    print(f"  - {name}:")
                    print(f"     {data['qty']} ед. × {data['unit_price']} (баз. {data['base_price']})")
                    print(f"     Модификаторы: город {data['city_mod']:+.2f}, ивент {data['event_mod']:+.2f}, дальность {data['dist_mod']:+.2f}")
                    print(f"     Итоговый множитель: {data['final_mod']:.2f}")
                print(f"  Прибыль: {report['profit']}")
                print(f"  Расходы: {report['expenses']}")
                print(f"  Чистый доход: {report['net']}")

        for c in finished:
            self.active_caravans.remove(c)
