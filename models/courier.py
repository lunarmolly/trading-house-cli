from dataclasses import dataclass

@dataclass
class Courier:
    """
    Модель курьера.

    Атрибуты:
        name (str): Имя.
        endurance (int): Выносливость.
        illness_resistance (float): Снижение вероятности болезни (0.8 = -20%).
    """
    name: str
    endurance: int
    illness_resistance: float = 1.0

    def get_actual_illness_chance(self, base_chance: float) -> float:
        """
        Получить фактический шанс болезни.

        Args:
            base_chance (float): Базовый шанс.

        Returns:
            float: Актуальный шанс.
        """
        return base_chance * self.illness_resistance
