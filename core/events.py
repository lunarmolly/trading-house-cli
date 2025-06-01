import random
from typing import List, Dict


def choose_event(event_pool: List[Dict], difficulty: str = "normal") -> str:
    """
    Выбирает случайное событие из пула с учетом уровня сложности.

    Args:
        event_pool: Список словарей событий, каждый должен содержать ключи:
                   'name' (str) - название события,
                   'probability' (float) - исходная вероятность
        difficulty: Уровень сложности ('easy', 'normal' или 'hard')

    Returns:
        Название выбранного события

    Пример события:
        {"name": "Болезнь курьера", "probability": 0.1}
    """
    # Проверка входных данных
    if not event_pool:
        raise ValueError("Пустой пул событий")

    if difficulty not in ('easy', 'normal', 'hard'):
        raise ValueError(f"Недопустимый уровень сложности: {difficulty}")

    # Извлекаем названия событий
    event_names = [event["name"] for event in event_pool]

    # Применяем модификаторы сложности
    if difficulty == 'easy':
        # Уменьшаем вероятность негативных событий
        weights = [event["probability"] * 0.7 for event in event_pool]
    elif difficulty == 'hard':
        # Увеличиваем вероятность негативных событий
        weights = [event["probability"] * 1.3 for event in event_pool]
    else:  # normal
        weights = [event["probability"] for event in event_pool]

    # Нормализуем веса, чтобы сумма была равна 1.0
    total_weight = sum(weights)
    if total_weight <= 0:
        raise ValueError("Сумма вероятностей событий должна быть положительной")

    normalized_weights = [w / total_weight for w in weights]

    # Выбираем случайное событие
    return random.choices(event_names, weights=normalized_weights, k=1)[0]



def choose_city_event(config: dict, difficulty: str = "normal") -> str:
    """
    Выбирает городское событие с учетом уровня сложности.

    Args:
        config: Конфигурация игры (должна содержать ключ 'city_events')
        difficulty: Уровень сложности ('easy', 'normal' или 'hard')

    Returns:
        Название выбранного городского события
    """
    if 'city_events' not in config:
        raise KeyError("В конфигурации отсутствует ключ 'city_events'")

    return choose_event(config['city_events'], difficulty)



def choose_travel_event(config: dict, difficulty: str = "normal") -> str:
    """
    Выбирает событие в пути с учетом уровня сложности.

    Args:
        config: Конфигурация игры (должна содержать ключ 'travel_events')
        difficulty: Уровень сложности ('easy', 'normal' или 'hard')

    Returns:
        Название выбранного события путешествия
    """
    if 'travel_events' not in config:
        raise KeyError("В конфигурации отсутствует ключ 'travel_events'")

    return choose_event(config['travel_events'], difficulty)
