from dataclasses import dataclass
from typing import Dict, Optional
from models.courier import Courier
from models.wagon import Wagon
from models.city import City


@dataclass
class Caravan:
    """
    Торговая миссия (караван), отправленная из столицы в другой город.

    Атрибуты:
        courier (Courier): Курьер, сопровождающий повозку.
        wagon (Wagon): Повозка.
        goods (Dict[str, int]): Груз (название товара → количество).
        destination (City): Город назначения.
        days_to_travel (int): Длительность пути в циклах (в одну сторону).
        departure_cycle (int): Игровой цикл, когда караван был отправлен.
        arrival_cycle (int): Игровой цикл, когда он прибудет в город.
        return_cycle (int): Игровой цикл, когда он вернётся обратно.
        event_occurred (Optional[str]): Событие, произошедшее в пути (туда или обратно).
        resolved (bool): Флаг, указывающий, был ли караван уже обработан при возвращении.
    """
    courier: Courier
    wagon: Wagon
    goods: Dict[str, int]
    destination: City
    days_to_travel: int  # путь туда, в циклах
    departure_cycle: int
    arrival_cycle: int
    return_cycle: int
    event_occurred: Optional[str] = None  # общее событие, можно расширить для "туда"/"обратно"
    resolved: bool = False  # флаг для предотвращения повторной обработки

    @property
    def goods_carried(self) -> Dict[str, int]:
        """
        Свойство для обратной совместимости с GUI.

        Returns:
            Dict[str, int]: Товары в караване.
        """
        return self.goods

    def total_goods(self) -> int:
        """
        Подсчитывает общее количество товаров в караване.

        Returns:
            int: Общее количество единиц.
        """
        return sum(self.goods.values())

    def is_over_capacity(self) -> bool:
        """
        Проверяет, превышает ли объём товаров вместимость повозки.

        Returns:
            bool: True, если перегрузка.
        """
        return self.total_goods() > self.wagon.capacity

    def is_rome_expedition(self) -> bool:
        """Проверяет, является ли экспедиция поездкой в Рим."""
        return self.destination.name == "Рим"