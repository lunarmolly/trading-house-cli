import random
from typing import Tuple, Dict, Optional
from models.caravan import Caravan
from models.player import Player
from models.goods_item import GoodsItem
from core.events import choose_travel_event
from core.finance import calculate_trip_expenses, calculate_sale_profit, generate_report

def update_caravan_event_once(caravan: Caravan, current_cycle: int, config: dict) -> Optional[str]:
    """
    Генерирует единственное событие для каравана, если ещё не было.

    Args:
        caravan (Caravan): Караван в пути.
        current_cycle (int): Текущий цикл.
        config (dict): Конфигурация.

    Returns:
        Optional[str]: Название события, если произошло в этом цикле.
    """
    if caravan.event_occurred:
        return None

    if caravan.departure_cycle <= current_cycle <= caravan.return_cycle:
        event = choose_travel_event(config)
        if event != "Ничего не произошло":
            caravan.event_occurred = event
            return event
    return None


def process_completed_caravan(
    caravan: Caravan,
    player: Player,
    current_cycle: int,
    goods_dict: Dict[str, GoodsItem],
    config: dict
) -> Tuple[Dict, bool]:
    """
    Обрабатывает караван, завершивший миссию (достиг return_cycle).

    Args:
        caravan (Caravan): Завершённый караван.
        player (Player): Игрок.
        current_cycle (int): Текущий цикл.
        goods_dict (Dict[str, GoodsItem]): Товары по имени.
        config (dict): Баланс.

    Returns:
        Tuple[Dict, bool]: Финансовый отчёт и флаг завершения.
    """
    if current_cycle < caravan.return_cycle:
        return {}, False

    event = caravan.event_occurred or "Ничего не произошло"
    loss_ratio = 0.0
    extra_cost = 0

    # === Обработка события ===
    if event == "Набег разбойников":
        loss_ratio = random.uniform(0.3, 0.5)
    elif event == "Поломка повозки":
        extra_cost += random.randint(10, 20)
    elif event == "Болезнь курьера":
        extra_cost += random.randint(5, 10)
    elif event == "Смерть курьера":
        caravan.goods = {}
        report = generate_report(0, 0, "Курьер погиб (в пути)", caravan.destination.current_event or "Нет события")
        return report, True

    # === Применение потерь от разбойников ===
    if loss_ratio > 0:
        for name in caravan.goods:
            lost = int(caravan.goods[name] * loss_ratio)
            caravan.goods[name] -= lost

    # === Продажа товаров ===
    profit, breakdown = calculate_sale_profit(
        caravan=caravan,
        goods=goods_dict,
        config=config
    )

    # === Расходы ===
    total_days = caravan.days_to_travel * 2 + 1
    base_expense = calculate_trip_expenses(total_days, config)
    total_expense = base_expense + extra_cost

    # === Баланс игрока ===
    net = profit - total_expense
    player.adjust_balance(net)

    # === Финальный отчёт ===
    report = generate_report(
        profit=profit,
        expenses=total_expense,
        event_path=event,
        event_city=caravan.destination.current_event or "Нет события",
        sale_breakdown=breakdown
    )
    return report, True
