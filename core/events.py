import random
from typing import List, Dict


def choose_event(event_pool: List[Dict]) -> str:
    """
    Выбирает одно событие на основе вероятностей.

    Args:
        event_pool (List[Dict]): Список событий, каждый с полями 'name' и 'probability'.

    Returns:
        str: Название выбранного события.
    """
    names = [event["name"] for event in event_pool]
    weights = [event["probability"] for event in event_pool]
    return random.choices(names, weights=weights, k=1)[0]


def choose_city_event(config: dict) -> str:
    """
    Выбирает событие в городе на текущий цикл.

    Args:
        config (dict): Конфигурация с полем city_events.

    Returns:
        str: Название события.
    """
    return choose_event(config["city_events"])


def choose_travel_event(config: dict) -> str:
    """
    Выбирает событие в пути.

    Args:
        config (dict): Конфигурация с полем travel_events.

    Returns:
        str: Название события.
    """
    return choose_event(config["travel_events"])
