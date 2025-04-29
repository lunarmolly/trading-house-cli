from typing import List, Optional
from models.goods_item import GoodsItem


def load_goods(config: dict) -> List[GoodsItem]:
    """
    Загружает список товаров из конфигурации.

    Args:
        config (dict): Конфигурация из balance_config.json.

    Returns:
        List[GoodsItem]: Список объектов товаров.
    """
    goods = []
    for item in config["goods"]:
        goods.append(GoodsItem(
            name=item["name"],
            base_price=item["base_price"],
            category=item["category"]
        ))
    return goods


def get_goods_by_name(name: str, goods_list: List[GoodsItem]) -> Optional[GoodsItem]:
    """
    Находит товар по имени.

    Args:
        name (str): Название товара.
        goods_list (List[GoodsItem]): Список товаров.

    Returns:
        Optional[GoodsItem]: Найденный товар или None.
    """
    for item in goods_list:
        if item.name == name:
            return item
    return None
