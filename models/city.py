from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class City:
    """
    Модель города.

    Атрибуты:
        name (str): Название города.
        duration (int): Длительность экспедиции туда и обратно (в днях).
        demand_modifiers (Dict[str, float]): Модификаторы спроса на товары.
        current_event (Optional[str]): Текущее событие в городе (устанавливается каждый игровой год).
    """
    name: str
    duration: int
    demand_modifiers: Dict[str, float]
    current_event: Optional[str] = None

    def get_price_modifier(self, goods_name: str) -> float:
        """
        Получить модификатор цены для конкретного товара.

        Args:
            goods_name (str): Название товара.

        Returns:
            float: Коэффициент спроса.
        """
        return self.demand_modifiers.get(goods_name, 1.0)