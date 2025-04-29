from dataclasses import dataclass
from typing import Dict

@dataclass
class City:
    """
    Модель города.

    Атрибуты:
        name (str): Название города.
        distance (int): Расстояние от столицы (в днях).
        demand_modifiers (Dict[str, float]): Модификаторы спроса по товарам.
    """
    name: str
    distance: int
    demand_modifiers: Dict[str, float]

    def get_price_modifier(self, goods_name: str) -> float:
        """
        Получить модификатор цены для конкретного товара.

        Args:
            goods_name (str): Название товара.

        Returns:
            float: Коэффициент спроса.
        """
        return self.demand_modifiers.get(goods_name, 1.0)
