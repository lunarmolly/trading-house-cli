from typing import Dict
from models.caravan import Caravan
from models.goods_item import GoodsItem

def calculate_trip_expenses(days: int, config: dict) -> int:
    """
    Считает расходы на еду, ночлег и охрану за поездку.

    Args:
        days (int): Общее количество дней в пути.
        config (dict): Конфигурация игры.

    Returns:
        int: Общая сумма расходов.
    """
    food = config["travel_costs"]["food_per_day"] * days
    lodging = config["travel_costs"]["lodging_per_2_days"] * (days // 2)
    guard = config["travel_costs"]["guard_cost_per_trip"]
    return food + lodging + guard


def calculate_sale_profit(caravan: Caravan, goods: Dict[str, GoodsItem], config: dict) -> int:
    """
    Считает прибыль от продажи товаров после рейса каравана.

    Args:
        caravan (Caravan): Завершивший миссию караван.
        goods (Dict[str, GoodsItem]): Словарь товаров по имени.
        config (dict): Конфигурация игры.

    Returns:
        int: Общая сумма выручки.
    """
    profit = 0
    destination = caravan.destination
    event_name = destination.current_event or "Нет события"
    sale_breakdown = {}

    for name, quantity in caravan.goods.items():
        item = goods.get(name)

        city_mod = destination.demand_modifiers.get(name, 1.0) - 1.0
        event_mod = config["event_modifiers"].get(event_name, {}).get(name, 1.0) - 1.0
        dist_mod = destination.distance * 0.02
        total = city_mod + event_mod + dist_mod
        final_modifier = 1.0 + total

        price = int(item.base_price * final_modifier)
        total_price = price * quantity
        profit += total_price

        sale_breakdown[name] = {
            "base_price": item.base_price,
            "qty": quantity,
            "city_mod": round(city_mod, 2),
            "event_mod": round(event_mod, 2),
            "dist_mod": round(dist_mod, 2),
            "final_mod": round(final_modifier, 2),
            "unit_price": price,
            "total": total_price
        }

    return profit, sale_breakdown


def generate_report(profit: int, expenses: int, event_path: str, event_city: str, sale_breakdown) -> Dict:
    """
    Генерирует финансовый отчёт по завершению миссии каравана.

    Args:
        profit (int): Доход от продажи товаров.
        expenses (int): Расходы на поездку.
        event_path (str): Событие в пути.
        event_city (str): Событие в городе продажи.

    Returns:
        Dict: Итоговый отчёт.
    """
    return {
        "profit": profit,
        "expenses": expenses,
        "net": profit - expenses,
        "event_path": event_path,
        "event_city": event_city,
        "sale_breakdown": sale_breakdown,
        "success": profit > expenses
    }
