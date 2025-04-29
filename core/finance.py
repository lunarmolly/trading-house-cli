from typing import Dict, Tuple
from models.caravan import Caravan
from models.goods_item import GoodsItem
from models.player import Player

def calculate_trip_expenses(days: int, config: dict) -> int:
    """
    Считает стандартные расходы в пути (еда, ночлег, охрана).

    Args:
        days (int): Сколько длился путь в днях.
        config (dict): Конфигурация с travel_costs.

    Returns:
        int: Общая сумма расходов.
    """
    food = config["travel_costs"]["food_per_day"] * days
    lodging = config["travel_costs"]["lodging_per_2_days"] * (days // 2)
    guard = config["travel_costs"]["guard_cost_per_trip"]
    return food + lodging + guard


def calculate_sale_profit(caravan: Caravan, goods: Dict[str, GoodsItem], config: dict) -> int:
    """
    Считает выручку от продажи товаров с учётом спроса в городе.

    Args:
        caravan (Caravan): Завершённый караван.
        goods (Dict[str, GoodsItem]): Словарь товаров по имени.
        config (dict): Конфигурация с event_modifiers.

    Returns:
        int: Общая сумма дохода от продажи.
    """
    profit = 0
    current_event = caravan.destination.current_event or "Нет события"
    modifiers = config["event_modifiers"].get(current_event, {})

    for name, quantity in caravan.goods.items():
        item = goods.get(name)
        modifier = modifiers.get(name, 1.0)
        final_price = int(item.base_price * modifier)
        profit += final_price * quantity

    return profit


def generate_report(profit: int, expenses: int, event_path: str, event_city: str) -> Dict:
    """
    Формирует итоговый отчёт по рейсу.

    Args:
        profit (int): Доход от продажи.
        expenses (int): Расходы в пути.
        event_path (str): Событие в пути.
        event_city (str): Событие в городе продажи.

    Returns:
        Dict: Отчёт по рейсу.
    """
    return {
        "profit": profit,
        "expenses": expenses,
        "net": profit - expenses,
        "event_path": event_path,
        "event_city": event_city,
        "success": profit > expenses
    }

