"""
Экран просмотра городов для игры "Торговый дом" - Древний Рим
"""

import customtkinter as ctk
from typing import Callable
from core.game import Game
from models.city import City


class RomanTheme:
    """Римская цветовая тема для единообразия"""
    BACKGROUND = "#f0e5d1"  # Светло-бежевый фон
    BUTTON = "#947153"      # Коричневая кнопка
    BUTTON_HOVER = "#8b6946"  # Темнее при наведении
    ACCENT = "#b8762f"      # Золотисто-коричневый акцент
    TEXT = "#372e29"        # Темно-коричневый текст
    SUCCESS = "#6b8e23"     # Зеленый для успеха
    WARNING = "#cd853f"     # Оранжевый для предупреждений
    ERROR = "#8b4513"       # Красно-коричневый для ошибок
    NEUTRAL = "#8a7968"     # Нейтральный серо-коричневый
    FRAME_BORDER = "#372e29"  # Границы фреймов
    
    # Шрифты
    FONT_TITLE = ("Georgia", 32, "bold")
    FONT_HEADER = ("Georgia", 18, "bold")
    FONT_BUTTON = ("Georgia", 14, "bold")
    FONT_TEXT = ("Georgia", 12)
    FONT_SMALL = ("Georgia", 10)


class CitiesOverviewScreen(ctk.CTkFrame):
    """Экран просмотра городов"""
    
    def __init__(self, parent, game: Game, on_back: Callable):
        super().__init__(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        self.game = game
        self.on_back = on_back
        
        self.create_widgets()
    
    def create_widgets(self):
        """Создание виджетов экрана"""
        
        # Заголовок
        header_frame = ctk.CTkFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            height=120
        )
        header_frame.pack(fill="x", pady=(20, 0))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏛️ ОБЗОР ГОРОДОВ ИМПЕРИИ 🏛️",
            font=RomanTheme.FONT_TITLE,
            text_color=RomanTheme.ACCENT
        )
        title_label.pack(pady=(20, 10))
        
        # Информация о текущем цикле
        info_label = ctk.CTkLabel(
            header_frame,
            text=f"📅 Цикл: {self.game.current_cycle}/{self.game.max_cycles} | 🏛️ Доступные города: {len(self.game.cities)}",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        info_label.pack(pady=(0, 10))
        
        # Основная прокручиваемая область
        main_scrollable = ctk.CTkScrollableFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            scrollbar_button_color=RomanTheme.BUTTON,
            scrollbar_button_hover_color=RomanTheme.BUTTON_HOVER
        )
        main_scrollable.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Создаем таблицу городов
        self.create_cities_table(main_scrollable)
        
        # Нижняя панель
        self.create_bottom_panel()
    
    def create_cities_table(self, parent):
        """Создание таблицы городов"""
        
        # Заголовок таблицы
        table_header_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.ACCENT,
            corner_radius=10,
            height=50
        )
        table_header_frame.pack(fill="x", pady=(20, 15), padx=20)
        table_header_frame.pack_propagate(False)
        
        header_title_label = ctk.CTkLabel(
            table_header_frame,
            text="🗺️ КАРТА ТОРГОВЫХ ГОРОДОВ 🗺️",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.BACKGROUND
        )
        header_title_label.pack(expand=True)
        
        # Контейнер для таблицы
        table_container = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=2,
            corner_radius=10
        )
        table_container.pack(fill="x", pady=(0, 20), padx=20)
        
        # Заголовки столбцов
        headers_frame = ctk.CTkFrame(
            table_container,
            fg_color=RomanTheme.NEUTRAL,
            corner_radius=8,
            height=45
        )
        headers_frame.pack(fill="x", pady=15, padx=15)
        headers_frame.pack_propagate(False)
        
        # Настройка сетки заголовков
        headers_frame.grid_columnconfigure(0, weight=3)  # Название города
        headers_frame.grid_columnconfigure(1, weight=2)  # Расстояние
        headers_frame.grid_columnconfigure(2, weight=3)  # Текущее событие
        headers_frame.grid_columnconfigure(3, weight=4)  # Спрос на товары
        headers_frame.grid_columnconfigure(4, weight=2)  # Статус караванов
        
        headers = ["🏛️ Город", "📏 Расстояние", "🎭 Событие", "📈 Высокий спрос", "🚛 Караваны"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=RomanTheme.FONT_BUTTON,
                text_color=RomanTheme.BACKGROUND
            )
            label.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
        
        # Строки с городами
        cities_rows_frame = ctk.CTkFrame(
            table_container,
            fg_color=RomanTheme.BACKGROUND
        )
        cities_rows_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Создаем строки для каждого города
        for i, city in enumerate(self.game.cities):
            self.create_city_row(cities_rows_frame, city, i)
    
    def create_city_row(self, parent, city: City, row_index: int):
        """Создание строки с информацией о городе"""
        
        # Основная строка города
        city_row_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND if row_index % 2 == 0 else "#ebe0d3",
            border_color=RomanTheme.NEUTRAL,
            border_width=1,
            corner_radius=5,
            height=60
        )
        city_row_frame.pack(fill="x", pady=2)
        city_row_frame.pack_propagate(False)
        
        # Настройка сетки строки
        city_row_frame.grid_columnconfigure(0, weight=3)
        city_row_frame.grid_columnconfigure(1, weight=2)
        city_row_frame.grid_columnconfigure(2, weight=3)
        city_row_frame.grid_columnconfigure(3, weight=4)
        city_row_frame.grid_columnconfigure(4, weight=2)
        
        # Название города
        city_name_label = ctk.CTkLabel(
            city_row_frame,
            text=f"🏛️ {city.name}",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT,
            anchor="w"
        )
        city_name_label.grid(row=0, column=0, padx=10, pady=8, sticky="ew")
        
        # Расстояние
        distance_label = ctk.CTkLabel(
            city_row_frame,
            text=f"{city.distance} дней",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        distance_label.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        
        # Текущее событие
        event_text = city.current_event or "Нет события"
        event_color = RomanTheme.WARNING if city.current_event else RomanTheme.NEUTRAL
        event_label = ctk.CTkLabel(
            city_row_frame,
            text=f"🎭 {event_text}",
            font=RomanTheme.FONT_SMALL,
            text_color=event_color
        )
        event_label.grid(row=0, column=2, padx=10, pady=8, sticky="ew")
        
        # Спрос на товары (показываем товары с высоким спросом)
        high_demand_goods = self.get_high_demand_goods(city)
        demand_text = ", ".join(high_demand_goods) if high_demand_goods else "Обычный спрос"
        demand_label = ctk.CTkLabel(
            city_row_frame,
            text=demand_text,
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.SUCCESS if high_demand_goods else RomanTheme.NEUTRAL,
            wraplength=200
        )
        demand_label.grid(row=0, column=3, padx=10, pady=8, sticky="ew")
        
        # Статус караванов
        caravan_status = self.get_caravan_status_for_city(city)
        caravan_color = RomanTheme.ACCENT if caravan_status != "Свободен" else RomanTheme.SUCCESS
        caravan_label = ctk.CTkLabel(
            city_row_frame,
            text=caravan_status,
            font=RomanTheme.FONT_SMALL,
            text_color=caravan_color
        )
        caravan_label.grid(row=0, column=4, padx=10, pady=8, sticky="ew")
    
    def get_high_demand_goods(self, city: City) -> list[str]:
        """Получить список товаров с высоким спросом в городе"""
        high_demand = []
        
        # Проверяем модификаторы спроса города
        for good_name, modifier in city.demand_modifiers.items():
            if modifier > 1.2:  # Если спрос больше 120%
                high_demand.append(good_name)
        
        # Также проверяем влияние текущего события
        if city.current_event and city.current_event in self.game.config.get("event_modifiers", {}):
            event_modifiers = self.game.config["event_modifiers"][city.current_event]
            for good_name, modifier in event_modifiers.items():
                if modifier > 1.3 and good_name not in high_demand:  # Если событие дает большой бонус
                    high_demand.append(f"{good_name}*")  # Помечаем звездочкой товары под влиянием события
        
        return high_demand[:3]  # Возвращаем максимум 3 товара для компактности
    
    def get_caravan_status_for_city(self, city: City) -> str:
        """Получить статус караванов для города"""
        # Проверяем активные караваны
        active_caravans_to_city = [
            caravan for caravan in self.game.active_caravans 
            if caravan.destination.name == city.name
        ]
        
        if not active_caravans_to_city:
            return "Свободен"
        
        # Проверяем караваны отправленные в текущем цикле
        current_cycle_caravans = [
            caravan for caravan in active_caravans_to_city
            if caravan.departure_cycle == self.game.current_cycle
        ]
        
        if current_cycle_caravans:
            return "Занят (цикл)"
        
        # Проверяем караваны в пути
        traveling_caravans = [
            caravan for caravan in active_caravans_to_city
            if caravan.arrival_cycle > self.game.current_cycle
        ]
        
        if traveling_caravans:
            caravan = traveling_caravans[0]
            days_left = caravan.arrival_cycle - self.game.current_cycle
            return f"В пути ({days_left}д)"
        
        # Проверяем караваны в городе
        in_city_caravans = [
            caravan for caravan in active_caravans_to_city
            if caravan.arrival_cycle <= self.game.current_cycle < caravan.return_cycle
        ]
        
        if in_city_caravans:
            caravan = in_city_caravans[0]
            days_left = caravan.return_cycle - self.game.current_cycle
            return f"В городе ({days_left}д)"
        
        return "Возвращается"
    
    def create_bottom_panel(self):
        """Создание нижней панели с кнопкой возврата"""
        bottom_frame = ctk.CTkFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            height=80
        )
        bottom_frame.pack(side="bottom", fill="x", pady=10)
        bottom_frame.pack_propagate(False)
        
        back_button = ctk.CTkButton(
            bottom_frame,
            text="← Вернуться в главное меню",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=8,
            width=250,
            height=50,
            command=self.on_back
        )
        back_button.pack(expand=True)


# Тестирование (если запускается напрямую)
if __name__ == "__main__":
    import sys
    import os
    
    # Добавляем корневую папку в путь
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from core.world import load_balance_config, generate_world
    from core.goods import load_goods
    from models.player import Player
    from models.courier import Courier
    from models.wagon import Wagon
    
    class MockGame:
        def __init__(self):
            # Загружаем реальную конфигурацию
            config = load_balance_config()
            cities = generate_world(config)
            goods = load_goods(config)
            
            # Создаем игрока
            courier = Courier(name="Маркус", endurance=0, illness_resistance=0.9)
            wagon = Wagon(name="Стандартная повозка", capacity=200, durability=0.9)
            
            player = Player(balance=5000)
            player.couriers = [courier]
            player.wagons = [wagon]
            
            # Настраиваем игру
            self.player = player
            self.cities = cities
            self.goods = goods
            self.config = config
            self.difficulty = "normal"
            self.current_cycle = 1
            self.max_cycles = 20
            self.active_caravans = []
    
    def test_back():
        print("Возврат в главное меню")
    
    # Создаем тестовое приложение
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.title("Тест экрана просмотра городов")
    root.geometry("1400x900")
    root.configure(fg_color=RomanTheme.BACKGROUND)
    
    # Создаем мок-игру
    mock_game = MockGame()
    
    # Создаем экран
    screen = CitiesOverviewScreen(
        parent=root,
        game=mock_game,  # type: ignore
        on_back=test_back
    )
    screen.pack(fill="both", expand=True)
    
    root.mainloop()
