from dataclasses import dataclass

@dataclass
class Wagon:
    """
    Модель повозки.

    Атрибуты:
        name (str): Название модели.
        capacity (int): Вместимость.
        durability (float): Снижение вероятности поломки.
    """
    name: str
    capacity: int
    durability: float = 1.0

    def get_actual_break_chance(self, base_chance: float) -> float:
        """
        Получить фактический шанс поломки.

        Args:
            base_chance (float): Базовый шанс.

        Returns:
            float: Актуальный шанс.
        """
        return base_chance * self.durability
