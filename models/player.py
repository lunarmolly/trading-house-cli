from dataclasses import dataclass, field
from typing import Dict, List
from .courier import Courier
from .wagon import Wagon
from .goods_item import GoodsItem

@dataclass
class Player:
    """
    Состояние игрока.

    Атрибуты:
        balance (int): Денежный баланс.
        inventory (Dict[str, int]): Склад товаров.
        couriers (List[Courier]): Курьеры.
        wagons (List[Wagon]): Повозки.
    """
    balance: intSW
    inventory: Dict[str, int] = field(default_factory=dict)
    couriers: List[Courier] = field(default_factory=list)
    wagons: List[Wagon] = field(default_factory=list)

    def add_goods(self, item: GoodsItem, quantity: int) -> None:
        """
        Добавить товар.

        Args:
            item (GoodsItem): Товар.
            quantity (int): Кол-во.
        """
        self.inventory[item.name] = self.inventory.get(item.name, 0) + quantity

    def remove_goods(self, item: GoodsItem, quantity: int) -> bool:
        """
        Удалить товар.

        Args:
            item (GoodsItem): Товар.
            quantity (int): Кол-во.

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
        Есть ли товар в нужном кол-ве?

        Args:
            item (GoodsItem): Товар.
            quantity (int): Кол-во.

        Returns:
            bool: Да или нет.
        """
        return self.inventory.get(item.name, 0) >= quantity

    def adjust_balance(self, amount: int) -> None:
        """
        Изменить баланс.

        Args:
            amount (int): Сумма (может быть отрицательной).
        """
        self.balance += amount
