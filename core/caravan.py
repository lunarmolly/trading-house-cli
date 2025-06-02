import random
from typing import Tuple, Dict, Optional
from models.caravan import Caravan
from models.player import Player
from models.goods_item import GoodsItem
from core.events import choose_travel_event
from core.finance import calculate_trip_expenses, calculate_sale_profit, generate_report
def update_caravan_event_once(
    caravan: Caravan,
    current_cycle: int,
    config: dict,
    difficulty: str
) -> Optional[str]:
    """Генерирует событие для каравана."""
    if caravan.event_occurred or caravan.is_rome_expedition():
        return None  # Пропускаем для Рима

    if caravan.departure_cycle <= current_cycle <= caravan.return_cycle:
        event = choose_travel_event(config, difficulty)
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
    """Обрабатывает завершённый караван."""
    if current_cycle < caravan.return_cycle:
        return {}, False

    # Специальная обработка для Рима
    if caravan.is_rome_expedition():
        total_days = 0
        event = "Продажа в Риме"
    else:
        total_days = caravan.days_to_travel * 2 + 1
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
        report = generate_report(
            profit=0,
            expenses=0,
            event_path="Курьер погиб (в пути)",
            event_city=caravan.destination.current_event or "Нет события",
            sale_breakdown={}
        )
        return report, True

    # === Применение потерь от разбойников ===
    if loss_ratio > 0:
        caravan.goods = {
            name: int(qty * (1 - loss_ratio))
            for name, qty in caravan.goods.items()
        }


    # === Продажа товаров и расчёт прибыли ===
    profit, sale_breakdown = calculate_sale_profit(
        caravan=caravan,
        goods=goods_dict,
        config=config
    )

    # === Расходы ===
    total_days = caravan.days_to_travel * 2 + 1
    total_expense = calculate_trip_expenses(total_days, config) + extra_cost

    # === Обновление баланса ===
    player.adjust_balance(profit - total_expense)

    # === Финальный отчёт ===
    report = generate_report(
        profit=profit,
        expenses=total_expense,
        event_path=event,
        event_city=caravan.destination.current_event or "Нет события",
        sale_breakdown=sale_breakdown
    )
    return report, True