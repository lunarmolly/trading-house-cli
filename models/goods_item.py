from dataclasses import dataclass

@dataclass
class GoodsItem:
    """
    Модель товара.

    Атрибуты:
        name (str): Название товара.
        base_price (int): Базовая цена.
        category (str): Категория товара.
    """
    name: str
    base_price: int
    category: str

    def calculate_price(self, modifier: float) -> int:
        """
        Вычислить цену с учётом модификатора спроса.

        Args:
            modifier (float): Модификатор спроса.

        Returns:
            int: Итоговая цена.
        """
        return int(self.base_price * modifier)
