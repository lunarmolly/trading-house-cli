import random
import json
from typing import List
from models.city import City

# Корни для генерации латинских названий городов
LATIN_ROOTS = ["Brund", "Cap", "Nerv", "Flor", "Agr", "Tar", "Lug", "Vent", "Aqua", "Tric", "Claud", "Mar", "Luc"]

def generate_city_name(existing_names: List[str]) -> str:
    """
    Генерация уникального названия города.

    Args:
        existing_names (List[str]): Уже сгенерированные названия.

    Returns:
        str: Уникальное латинизированное имя города.
    """
    while True:
        root = random.choice(LATIN_ROOTS)
        suffix = random.choice(["ium", "a", "um", "ona", "ensis"])
        name = root + suffix
        if name not in existing_names:
            return name

def generate_world(config: dict, city_count: int = 7) -> List[City]:
    """
    Генерация мира: создаёт список городов.

    Args:
        config (dict): Конфигурационные данные из balance_config.json.
        city_count (int): Сколько городов создать (по умолчанию 7).

    Returns:
        List[City]: Список объектов City.
    """
    goods_names = [item["name"] for item in config["goods"]]
    cities = []
    used_names = set()

    for _ in range(city_count):
        # Имя и расстояние
        name = generate_city_name(list(used_names))
        used_names.add(name)
        distance = random.randint(3, 12)

        # Спрос: 2 повышенных, 2 пониженных
        demand_modifiers = {good: 1.0 for good in goods_names}
        high_demand = random.sample(goods_names, 2)
        low_demand = random.sample([g for g in goods_names if g not in high_demand], 2)

        for good in high_demand:
            demand_modifiers[good] = 1.2
        for good in low_demand:
            demand_modifiers[good] = 0.8

        # Создание города (ивент пока не задан)
        city = City(
            name=name,
            distance=distance,
            demand_modifiers=demand_modifiers,
            current_event=None  # будет назначено динамически
        )
        cities.append(city)

    return cities

def load_balance_config(path: str = "data/balance_config.json") -> dict:
    """
    Загружает конфигурацию баланса из JSON-файла.

    Args:
        path (str): Путь до конфигурационного файла.

    Returns:
        dict: Конфигурационные данные.
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)
