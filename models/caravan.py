from dataclasses import dataclass
from typing import Dict, Optional
from .courier import Courier
from .wagon import Wagon
from .city import City

@dataclass
class Caravan:
    """
    Торговая миссия.

    Атрибуты:
        courier (Courier): Курьер.
        wagon (Wagon): Повозка.
        goods (Dict[str, int]): Груз.
        destination (City): Город.
        days_to_travel (int): Время в пути.
        event_occurred (Optional[str]): Событие.
    """
    courier: Courier
    wagon: Wagon
    goods: Dict[str, int]
    destination: City
    days_to_travel: int
    event_occurred: Optional[str] = None

    def total_goods(self) -> int:
        """
        Всего товаров.

        Returns:
            int: Сумма всех единиц.
        """
        return sum(self.goods.values())

    def is_over_capacity(self) -> bool:
        """
        Повозка перегружена?

        Returns:
            bool: Да или нет.
        """
        return self.total_goods() > self.wagon.capacity
