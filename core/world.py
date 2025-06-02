import random
import json
from typing import List
from models.city import City

# Корни для генерации латинских названий городов
LATIN_ROOTS = ["Brund", "Cap", "Nerv", "Flor", "Agr", "Tar", "Lug", "Vent", "Aqua", "Tric", "Claud", "Mar", "Luc"]


def generate_city_name(existing_names: List[str]) -> str:
    """Генерация уникального названия города."""
    while True:
        root = random.choice(LATIN_ROOTS)
        suffix = random.choice(["ium", "a", "um", "ona", "ensis"])
        name = root + suffix
        if name not in existing_names:
            return name


def generate_world(config: dict, city_count: int = 7) -> List[City]:
    """Генерация мира: создаёт список городов."""
    goods_names = [item["name"] for item in config["goods"]]
    cities = []
    used_names = set()

    # Добавляем Рим первым городом
    rome_duration = 0
    rome_demand_modifiers = {good: 1.0 for good in goods_names}
    rome = City(
        name="Рим",
        duration=rome_duration,
        demand_modifiers=rome_demand_modifiers,
        current_event=None
    )
    cities.append(rome)
    used_names.add("Рим")

    # Генерируем остальные города
    for _ in range(city_count - 1):
        # Имя и длительность экспедиции
        name = generate_city_name(list(used_names))
        used_names.add(name)
        duration = random.choice([2, 4, 6])  # Длительность от 1 до 3 дней

        # Спрос: 2 повышенных, 2 пониженных
        demand_modifiers = {good: 1.0 for good in goods_names}
        high_demand = random.sample(goods_names, 2)
        low_demand = random.sample([g for g in goods_names if g not in high_demand], 2)

        for good in high_demand:
            demand_modifiers[good] = 1.2
        for good in low_demand:
            demand_modifiers[good] = 0.8

        # Создание города
        city = City(
            name=name,
            duration=duration,
            demand_modifiers=demand_modifiers,
            current_event=None
        )
        cities.append(city)

    return cities


def load_balance_config(
        path: str = "data/balance_config.json",
        difficulty: str = "normal"
) -> dict:
    with open(path, encoding="utf-8") as f:
        config = json.load(f)

    # Применяем настройки сложности, если они есть
    if "difficulty_settings" in config and "player" in config:
        settings = config["difficulty_settings"].get(difficulty, {})

        # Модифицируем стартовый баланс игрока
        if "starting_balance_multiplier" in settings:
            config["player"]["starting_balance"] = int(
                config["player"]["starting_balance"] * settings["starting_balance_multiplier"]
            )

        # Модифицируем сопротивляемость болезням курьеров
        if "illness_resistance_multiplier" in settings and "starting_couriers" in config["player"]:
            for courier in config["player"]["starting_couriers"]:
                if "illness_resistance" in courier:
                    courier["illness_resistance"] *= settings["illness_resistance_multiplier"]

    return config
