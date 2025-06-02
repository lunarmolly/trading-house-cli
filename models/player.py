from dataclasses import dataclass, field
from typing import Dict, List
from models.courier import Courier
from models.wagon import Wagon
from models.goods_item import GoodsItem
from models.caravan import Caravan

@dataclass
class Player:
    """
    Состояние игрока.

    Атрибуты:
        balance (int): Баланс в денариях.
        inventory (Dict[str, int]): Товары на складе (название → количество).
        couriers (List[Courier]): Курьеры, доступные игроку.
        wagons (List[Wagon]): Повозки, доступные игроку.
        completed_caravans (List[Caravan]): История завершённых миссий.
    """
    balance: int
    inventory: Dict[str, int] = field(default_factory=dict)
    couriers: List[Courier] = field(default_factory=list)
    wagons: List[Wagon] = field(default_factory=list)
    completed_caravans: List[Caravan] = field(default_factory=list)

    def add_goods(self, item: GoodsItem, quantity: int) -> None:
        """
        Добавляет товар на склад.

        Args:
            item (GoodsItem): Товар.
            quantity (int): Количество.
        """
        self.inventory[item.name] = self.inventory.get(item.name, 0) + quantity

    def remove_goods(self, item: GoodsItem, quantity: int) -> bool:
        """
        Удаляет товар со склада, если достаточно.

        Args:
            item (GoodsItem): Товар.
            quantity (int): Количество.

        Returns:
            bool: Удалено успешно или нет.
        """
        if self.inventory.get(item.name, 0) >= quantity:
            self.inventory[item.name] -= quantity
            if self.inventory[item.name] == 0:
                del self.inventory[item.name]
            return True
        return False

    def has_goods(self, item: GoodsItem, quantity: int) -> bool:
        """
        Проверяет наличие товара.

        Args:
            item (GoodsItem): Товар.
            quantity (int): Требуемое количество.

        Returns:
            bool: Есть ли достаточно.
        """
        return self.inventory.get(item.name, 0) >= quantity

    def adjust_balance(self, amount: int) -> None:
        """
        Изменяет баланс игрока.

        Args:
            amount (int): Сумма (может быть отрицательной).
        """
        self.balance += amount
