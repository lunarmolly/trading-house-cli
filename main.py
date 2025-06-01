import os
import tkinter as tk
from tkinter import messagebox
from core.world import load_balance_config, generate_world
from core.goods import load_goods
from models.player import Player
from models.courier import Courier
from models.wagon import Wagon
from core.game import Game
from ui.gui import TradeHouseGUI


class DifficultySelectionWindow:
    """Окно выбора уровня сложности"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Выбор сложности")
        self.root.geometry("300x200")
        self.difficulty = None

        tk.Label(self.root, text="Выберите уровень сложности:").pack(pady=10)

        tk.Button(self.root, text="Легкий (меньше рисков, больше ресурсов)",
                  command=lambda: self.set_difficulty("easy")).pack(fill=tk.X, padx=20, pady=5)
        tk.Button(self.root, text="Средний (стандартный баланс)",
                  command=lambda: self.set_difficulty("normal")).pack(fill=tk.X, padx=20, pady=5)
        tk.Button(self.root, text="Сложный (высокие риски, меньше ресурсов)",
                  command=lambda: self.set_difficulty("hard")).pack(fill=tk.X, padx=20, pady=5)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.root.destroy()

    def get_difficulty(self):
        self.root.mainloop()
        return self.difficulty


def load_game_config(difficulty: str) -> dict:
    """Загрузка и проверка конфигурации с учетом сложности"""
    config_path = "data/balance_config.json"
    if not os.path.exists(config_path):
        config_path = "balance_config.json"

    try:
        config = load_balance_config(path=config_path, difficulty=difficulty)

        if "player" not in config:
            messagebox.showerror("Ошибка", "Конфигурационный файл не содержит раздела 'player'")
            raise RuntimeError("Отсутствует раздел 'player' в конфигурации")

        return config
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить конфигурацию: {str(e)}")
        raise


def create_player(config: dict, difficulty: str) -> Player:
    """Создание игрока с учетом уровня сложности"""
    # Настройки баланса
    starting_balance = config["player"]["starting_balance"]
    if "difficulty_settings" in config and difficulty in config["difficulty_settings"]:
        settings = config["difficulty_settings"][difficulty]
        starting_balance *= settings.get("starting_balance_multiplier", 1.0)

    # Создание курьеров
    couriers = []
    for courier_data in config["player"].get("starting_couriers", []):
        illness_resistance = courier_data.get("illness_resistance", 1.0)
        if "difficulty_settings" in config and difficulty in config["difficulty_settings"]:
            settings = config["difficulty_settings"][difficulty]
            illness_resistance *= settings.get("illness_resistance_multiplier", 1.0)

        couriers.append(Courier(
            name=courier_data["name"],
            endurance=courier_data.get("endurance", 0),
            illness_resistance=illness_resistance
        ))

    # Создание повозок
    wagons = [
        Wagon(
            name=wagon_data["name"],
            capacity=wagon_data["capacity"],
            durability=wagon_data.get("durability", 0.75)
        ) for wagon_data in config["player"].get("starting_wagons", [])
    ]

    return Player(
        balance=starting_balance,
        couriers=couriers,
        wagons=wagons
    )


def main():
    # Выбор сложности через GUI
    diff_window = DifficultySelectionWindow()
    difficulty = diff_window.get_difficulty()

    if not difficulty:
        return  # Пользователь закрыл окно

    # Загрузка конфигурации
    try:
        config = load_game_config(difficulty)
    except:
        return

    # Генерация мира и товаров
    cities = generate_world(config)
    goods = load_goods(config)

    # Создание игрока
    player = create_player(config, difficulty)

    # Инициализация игры
    game = Game(player=player, cities=cities, goods=goods, config=config, difficulty=difficulty)

    # Запуск основного GUI
    app = TradeHouseGUI(game)
    app.mainloop()


if __name__ == "__main__":
    main()