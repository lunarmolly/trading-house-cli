"""
Экран отправки караванов для игры "Торговый дом" - Древний Рим
"""

import customtkinter as ctk
from typing import Callable, Optional, Dict
from core.game import Game
from models.city import City
from models.goods_item import GoodsItem


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


class SendCaravanScreen(ctk.CTkFrame):
    """Экран отправки караванов"""
    
    def __init__(self, parent, game: Game, on_back: Callable):
        super().__init__(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        self.game = game
        self.on_back = on_back
        
        # Состояние экрана
        self.selected_city: Optional[City] = None
        self.selected_goods: Dict[str, int] = {}
        self.current_capacity = 0
        
        # Элементы интерфейса
        self.city_buttons = {}
        self.goods_rows = {}
        self.capacity_label: Optional[ctk.CTkLabel] = None
        self.send_button: Optional[ctk.CTkButton] = None
        
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
            text="🚛 ОТПРАВКА КАРАВАНА 🚛",
            font=RomanTheme.FONT_TITLE,
            text_color=RomanTheme.ACCENT
        )
        title_label.pack(pady=(20, 10))
        
        # Информация о доступных ресурсах
        info_label = ctk.CTkLabel(
            header_frame,
            text=f"💰 Баланс: {self.game.player.balance:,} денариев | 🚛 Курьеры: {len(self.game.player.couriers)} | 🛠️ Повозки: {len(self.game.player.wagons)}",
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
        
        # Проверка возможности отправки караванов
        if not self.can_send_caravan():
            self.create_no_caravan_message(main_scrollable)
            self.create_bottom_panel()
            return
        
        # Секция выбора города
        self.create_city_selection(main_scrollable)
        
        # Секция выбора товаров
        self.create_goods_selection(main_scrollable)
        
        # Информация о вместимости
        self.create_capacity_info(main_scrollable)
        
        # Кнопка отправки
        self.create_send_button(main_scrollable)
        
        # Нижняя панель
        self.create_bottom_panel()
    
    def can_send_caravan(self) -> bool:
        """Проверка возможности отправки каравана"""
        # Проверяем наличие курьеров
        if not self.game.player.couriers:
            return False
        
        # Проверяем наличие повозок
        if not self.game.player.wagons:
            return False
        
        # Проверяем наличие товаров на складе
        if not any(qty > 0 for qty in self.game.player.inventory.values()):
            return False
        
        # Проверяем наличие доступных городов (не все города заняты караванами в текущем цикле)
        available_cities = self.get_available_cities()
        if not available_cities:
            return False
        
        return True
    
    def get_available_cities(self) -> list[City]:
        """Получить список городов, в которые можно отправить караван"""
        # Города, в которые уже отправлены караваны в текущем цикле
        occupied_cities = set()
        for caravan in self.game.active_caravans:
            if caravan.departure_cycle == self.game.current_cycle:
                occupied_cities.add(caravan.destination.name)
        
        # Возвращаем доступные города
        return [city for city in self.game.cities if city.name not in occupied_cities]
    
    def create_no_caravan_message(self, parent):
        """Создание сообщения о невозможности отправки каравана"""
        message_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.WARNING,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=2,
            corner_radius=10
        )
        message_frame.pack(fill="x", pady=50, padx=50)
        
        # Определяем причину невозможности отправки
        reasons = []
        if not self.game.player.couriers:
            reasons.append("📝 Нет доступных курьеров")
        if not self.game.player.wagons:
            reasons.append("🛠️ Нет доступных повозок")
        if not any(qty > 0 for qty in self.game.player.inventory.values()):
            reasons.append("📦 Нет товаров на складе")
        
        available_cities = self.get_available_cities()
        if not available_cities:
            reasons.append("🏛️ Все города уже заняты караванами в этом цикле")
        
        warning_label = ctk.CTkLabel(
            message_frame,
            text="⚠️ НЕВОЗМОЖНО ОТПРАВИТЬ КАРАВАН ⚠️",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.BACKGROUND
        )
        warning_label.pack(pady=(20, 10))
        
        reasons_text = "\n".join(reasons)
        reasons_label = ctk.CTkLabel(
            message_frame,
            text=f"Причины:\n\n{reasons_text}\n\nВернитесь в главное меню для решения проблем.",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.BACKGROUND,
            justify="center"
        )
        reasons_label.pack(pady=(0, 20))
    
    def create_city_selection(self, parent):
        """Создание секции выбора города"""
        city_section_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.ACCENT,
            corner_radius=10,
            height=50
        )
        city_section_frame.pack(fill="x", pady=(20, 15), padx=20)
        city_section_frame.pack_propagate(False)
        
        city_title_label = ctk.CTkLabel(
            city_section_frame,
            text="🏛️ ВЫБЕРИТЕ ГОРОД НАЗНАЧЕНИЯ 🏛️",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.BACKGROUND
        )
        city_title_label.pack(expand=True)
        
        # Контейнер для городов
        cities_container = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=2,
            corner_radius=10
        )
        cities_container.pack(fill="x", pady=(0, 20), padx=20)
        
        available_cities = self.get_available_cities()
        
        if not available_cities:
            no_cities_label = ctk.CTkLabel(
                cities_container,
                text="🚫 Все города заняты караванами в этом цикле\n\nПерейдите к следующему циклу для освобождения городов",
                font=RomanTheme.FONT_TEXT,
                text_color=RomanTheme.NEUTRAL,
                justify="center"
            )
            no_cities_label.pack(pady=40)
            return
        
        # Создаем кнопки для доступных городов
        for i, city in enumerate(available_cities):
            self.create_city_button(cities_container, city, i)
    
    def create_city_button(self, parent, city: City, index: int):
        """Создание кнопки выбора города"""
        city_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=1,
            corner_radius=8
        )
        city_frame.pack(fill="x", pady=5, padx=15)
        
        # Информация о городе
        city_info_frame = ctk.CTkFrame(
            city_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        city_info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        city_name_label = ctk.CTkLabel(
            city_info_frame,
            text=f"🏛️ {city.name}",
            font=RomanTheme.FONT_BUTTON,
            text_color=RomanTheme.TEXT,
            anchor="w"
        )
        city_name_label.pack(anchor="w")
        
        distance_label = ctk.CTkLabel(
            city_info_frame,
            text=f"📏 Расстояние: {city.distance} дней",
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.NEUTRAL,
            anchor="w"
        )
        distance_label.pack(anchor="w")
        
        event_text = f"🎭 Событие: {city.current_event or 'Нет события'}"
        event_label = ctk.CTkLabel(
            city_info_frame,
            text=event_text,
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.NEUTRAL,
            anchor="w"
        )
        event_label.pack(anchor="w")
        
        # Кнопка выбора
        select_button = ctk.CTkButton(
            city_frame,
            text="⚡ Выбрать",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=8,
            width=120,
            height=40,
            command=lambda c=city: self.select_city(c)
        )
        select_button.pack(side="right", padx=10, pady=10)
        
        self.city_buttons[city.name] = (city_frame, select_button)
    
    def select_city(self, city: City):
        """Выбор города для отправки каравана"""
        self.selected_city = city
        
        # Обновляем визуальное состояние кнопок
        for city_name, (frame, button) in self.city_buttons.items():
            if city_name == city.name:
                frame.configure(border_color=RomanTheme.ACCENT, border_width=3)
                button.configure(text="✅ Выбран", fg_color=RomanTheme.SUCCESS)
            else:
                frame.configure(border_color=RomanTheme.FRAME_BORDER, border_width=1)
                button.configure(text="⚡ Выбрать", fg_color=RomanTheme.BUTTON)
        
        # Обновляем секцию товаров
        self.update_goods_section()
    
    def create_goods_selection(self, parent):
        """Создание секции выбора товаров"""
        self.goods_section_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BUTTON,
            corner_radius=10,
            height=50
        )
        self.goods_section_frame.pack(fill="x", pady=(20, 15), padx=20)
        self.goods_section_frame.pack_propagate(False)
        
        goods_title_label = ctk.CTkLabel(
            self.goods_section_frame,
            text="📦 ВЫБЕРИТЕ ТОВАРЫ ДЛЯ ОТПРАВКИ 📦",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.BACKGROUND
        )
        goods_title_label.pack(expand=True)
        
        # Контейнер для товаров
        self.goods_container = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=2,
            corner_radius=10
        )
        self.goods_container.pack(fill="x", pady=(0, 20), padx=20)
        
        if not self.selected_city:
            placeholder_label = ctk.CTkLabel(
                self.goods_container,
                text="👆 Сначала выберите город назначения",
                font=RomanTheme.FONT_TEXT,
                text_color=RomanTheme.NEUTRAL
            )
            placeholder_label.pack(pady=40)
    
    def update_goods_section(self):
        """Обновление секции выбора товаров"""
        # Очищаем контейнер
        for widget in self.goods_container.winfo_children():
            widget.destroy()
        
        if not self.selected_city:
            return
        
        # Создаем заголовки таблицы
        headers_frame = ctk.CTkFrame(
            self.goods_container,
            fg_color=RomanTheme.NEUTRAL,
            corner_radius=8,
            height=40
        )
        headers_frame.pack(fill="x", pady=15, padx=15)
        headers_frame.pack_propagate(False)
        
        # Настройка сетки заголовков
        headers_frame.grid_columnconfigure(0, weight=3)  # Название товара
        headers_frame.grid_columnconfigure(1, weight=2)  # На складе
        headers_frame.grid_columnconfigure(2, weight=2)  # Ожидаемая цена
        headers_frame.grid_columnconfigure(3, weight=2)  # Количество
        headers_frame.grid_columnconfigure(4, weight=1)  # Действие
        
        headers = ["Товар", "На складе", "Ожидаемая цена", "Количество", ""]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=RomanTheme.FONT_BUTTON,
                text_color=RomanTheme.BACKGROUND
            )
            label.grid(row=0, column=i, padx=10, pady=8, sticky="ew")
        
        # Создаем строки для товаров
        goods_dict = {g.name: g for g in self.game.goods}
        available_goods = [(name, qty) for name, qty in self.game.player.inventory.items() if qty > 0]
        
        if not available_goods:
            no_goods_label = ctk.CTkLabel(
                self.goods_container,
                text="📦 Нет товаров на складе\n\nПосетите торговую площадь для закупки товаров",
                font=RomanTheme.FONT_TEXT,
                text_color=RomanTheme.NEUTRAL,
                justify="center"
            )
            no_goods_label.pack(pady=40)
            return
        
        for i, (name, available_qty) in enumerate(available_goods):
            good_obj = goods_dict.get(name)
            if good_obj:
                self.create_goods_row(self.goods_container, good_obj, available_qty, i)
    
    def create_goods_row(self, parent, good: GoodsItem, available_qty: int, row_index: int):
        """Создание строки с товаром"""
        row_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND if row_index % 2 == 0 else "#ebe0d3",
            corner_radius=5
        )
        row_frame.pack(fill="x", pady=2, padx=15)
        
        # Настройка сетки строки
        row_frame.grid_columnconfigure(0, weight=3)
        row_frame.grid_columnconfigure(1, weight=2)
        row_frame.grid_columnconfigure(2, weight=2)
        row_frame.grid_columnconfigure(3, weight=2)
        row_frame.grid_columnconfigure(4, weight=1)
        
        # Название товара
        name_label = ctk.CTkLabel(
            row_frame,
            text=f"📦 {good.name}",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT,
            anchor="w"
        )
        name_label.grid(row=0, column=0, padx=10, pady=8, sticky="ew")
        
        # Количество на складе
        stock_label = ctk.CTkLabel(
            row_frame,
            text=f"{available_qty} ед.",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        stock_label.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        
        # Расчет ожидаемой цены в выбранном городе
        expected_price = self.calculate_expected_price(good, self.selected_city)
        price_label = ctk.CTkLabel(
            row_frame,
            text=f"{expected_price:,} ден./ед.",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.SUCCESS if expected_price > good.base_price else RomanTheme.TEXT
        )
        price_label.grid(row=0, column=2, padx=10, pady=8, sticky="ew")
        
        # Поле ввода количества
        current_qty = self.selected_goods.get(good.name, 0)
        quantity_entry = ctk.CTkEntry(
            row_frame,
            placeholder_text="0",
            font=RomanTheme.FONT_TEXT,
            width=60,
            height=25
        )
        quantity_entry.grid(row=0, column=3, padx=10, pady=8, sticky="ew")
        
        if current_qty > 0:
            quantity_entry.delete(0, "end")
            quantity_entry.insert(0, str(current_qty))
        
        # Кнопка добавления
        add_button = ctk.CTkButton(
            row_frame,
            text="✓",
            font=RomanTheme.FONT_SMALL,
            fg_color=RomanTheme.SUCCESS,
            hover_color="#5a7c1f",
            text_color=RomanTheme.BACKGROUND,
            corner_radius=5,
            width=40,
            height=25,
            command=lambda: self.add_goods_to_caravan(good, quantity_entry, available_qty)
        )
        add_button.grid(row=0, column=4, padx=10, pady=8)
        
        self.goods_rows[good.name] = (row_frame, quantity_entry, add_button)
    
    def calculate_expected_price(self, good: GoodsItem, city: City) -> int:
        """Расчет ожидаемой цены товара в городе"""
        # Модификатор города
        city_mod = city.demand_modifiers.get(good.name, 1.0) - 1.0
        
        # Модификатор события
        event = city.current_event or "Нет события"
        event_mod = self.game.config["event_modifiers"].get(event, {}).get(good.name, 1.0) - 1.0
        
        # Модификатор расстояния
        distance_mod = city.distance * 0.02
        
        # Итоговый модификатор
        total_percent = city_mod + event_mod + distance_mod
        final_modifier = 1.0 + total_percent
        
        return int(good.base_price * final_modifier)
    
    def add_goods_to_caravan(self, good: GoodsItem, quantity_entry: ctk.CTkEntry, max_qty: int):
        """Добавление товара к караване"""
        try:
            quantity = int(quantity_entry.get() or "0")
            
            if quantity <= 0:
                self.show_error("Количество должно быть больше 0")
                return
            
            if quantity > max_qty:
                self.show_error(f"Недостаточно товара на складе (доступно: {max_qty})")
                return
            
            # Проверяем вместимость повозки
            wagon = self.game.player.wagons[0]  # Берем первую доступную повозку
            
            # Подсчитываем текущую загрузку
            current_load = sum(self.selected_goods.values())
            new_load = current_load - self.selected_goods.get(good.name, 0) + quantity
            
            if new_load > wagon.capacity:
                self.show_error(f"Превышена вместимость повозки!\nВместимость: {wagon.capacity}, попытка загрузить: {new_load}")
                return
            
            # Добавляем товар
            if quantity > 0:
                self.selected_goods[good.name] = quantity
            else:
                self.selected_goods.pop(good.name, None)
            
            # Обновляем информацию о вместимости
            self.update_capacity_info()
            
            # Обновляем кнопку отправки
            self.update_send_button()
            
            self.show_success(f"Добавлено: {quantity} ед. '{good.name}'")
            
        except ValueError:
            self.show_error("Введите корректное число")
    
    def create_capacity_info(self, parent):
        """Создание информации о вместимости"""
        self.capacity_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.NEUTRAL,
            corner_radius=10
        )
        self.capacity_frame.pack(fill="x", pady=(10, 20), padx=20)
        
        self.update_capacity_info()
    
    def update_capacity_info(self):
        """Обновление информации о вместимости"""
        # Очищаем фрейм
        for widget in self.capacity_frame.winfo_children():
            widget.destroy()
        
        if not self.game.player.wagons:
            return
        
        wagon = self.game.player.wagons[0]
        current_load = sum(self.selected_goods.values())
        
        capacity_text = f"🛠️ Повозка: {wagon.name} | Загружено: {current_load}/{wagon.capacity} ед."
        
        # Определяем цвет в зависимости от загрузки
        if current_load == 0:
            color = RomanTheme.NEUTRAL
        elif current_load <= wagon.capacity * 0.7:
            color = RomanTheme.SUCCESS
        elif current_load <= wagon.capacity:
            color = RomanTheme.WARNING
        else:
            color = RomanTheme.ERROR
        
        self.capacity_label = ctk.CTkLabel(
            self.capacity_frame,
            text=capacity_text,
            font=RomanTheme.FONT_HEADER,
            text_color=color
        )
        self.capacity_label.pack(pady=15)
        
        # Показываем выбранные товары
        if self.selected_goods:
            goods_text = " | ".join([f"{name}: {qty} ед." for name, qty in self.selected_goods.items()])
            selected_label = ctk.CTkLabel(
                self.capacity_frame,
                text=f"📦 Выбрано: {goods_text}",
                font=RomanTheme.FONT_TEXT,
                text_color=RomanTheme.BACKGROUND
            )
            selected_label.pack(pady=(0, 15))
    
    def create_send_button(self, parent):
        """Создание кнопки отправки каравана"""
        self.send_button_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND
        )
        self.send_button_frame.pack(fill="x", pady=20, padx=20)
        
        self.update_send_button()
    
    def update_send_button(self):
        """Обновление кнопки отправки"""
        # Очищаем фрейм
        for widget in self.send_button_frame.winfo_children():
            widget.destroy()
        
        can_send = (
            self.selected_city is not None and 
            bool(self.selected_goods) and 
            sum(self.selected_goods.values()) <= self.game.player.wagons[0].capacity
        )
        
        if can_send:
            self.send_button = ctk.CTkButton(
                self.send_button_frame,
                text=f"🚀 ОТПРАВИТЬ КАРАВАН В {self.selected_city.name.upper()}",
                font=RomanTheme.FONT_BUTTON,
                fg_color=RomanTheme.SUCCESS,
                hover_color="#5a7c1f",
                text_color=RomanTheme.BACKGROUND,
                corner_radius=10,
                width=400,
                height=60,
                command=self.send_caravan
            )
            self.send_button.pack(pady=20)
        else:
            placeholder_label = ctk.CTkLabel(
                self.send_button_frame,
                text="👆 Выберите город и товары для отправки каравана",
                font=RomanTheme.FONT_TEXT,
                text_color=RomanTheme.NEUTRAL
            )
            placeholder_label.pack(pady=20)
    
    def send_caravan(self):
        """Отправка каравана"""
        if not self.selected_city or not self.selected_goods:
            self.show_error("Выберите город и товары")
            return
        
        try:
            # Получаем курьера и повозку
            courier = self.game.player.couriers[0]
            wagon = self.game.player.wagons[0]
            
            # Проверяем еще раз вместимость
            total_goods = sum(self.selected_goods.values())
            if total_goods > wagon.capacity:
                self.show_error("Превышена вместимость повозки")
                return
            
            # Убираем товары со склада
            goods_dict = {g.name: g for g in self.game.goods}
            for name, qty in self.selected_goods.items():
                good_obj = goods_dict[name]
                self.game.player.remove_goods(good_obj, qty)
            
            # Создаем караван
            caravan = self.game.form_caravan(
                courier=courier,
                wagon=wagon,
                goods_selection=self.selected_goods.copy(),
                city=self.selected_city
            )
            
            # Показываем успешное сообщение
            goods_list = ", ".join([f"{name} ({qty} ед.)" for name, qty in self.selected_goods.items()])
            success_message = f"✅ Караван успешно отправлен!\n\nНазначение: {self.selected_city.name}\nТовары: {goods_list}\nПрибытие: цикл {caravan.arrival_cycle}\nВозврат: цикл {caravan.return_cycle}"
            
            self.show_success_message(success_message)
            
        except Exception as e:
            self.show_error(f"Ошибка при отправке каравана: {str(e)}")
    
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
    
    def show_error(self, message: str):
        """Показать сообщение об ошибке"""
        self.show_message(message, RomanTheme.ERROR, "⚠️ ОШИБКА")
    
    def show_success(self, message: str):
        """Показать сообщение об успехе"""
        self.show_message(message, RomanTheme.SUCCESS, "✅ УСПЕХ")
    
    def show_message(self, message: str, color: str, title: str):
        """Показать временное сообщение"""
        message_frame = ctk.CTkFrame(
            self,
            fg_color=color,
            corner_radius=10,
            height=100
        )
        message_frame.pack(fill="x", pady=(0, 10), padx=50)
        message_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            message_frame,
            text=title,
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.BACKGROUND
        )
        title_label.pack(pady=(10, 5))
        
        message_label = ctk.CTkLabel(
            message_frame,
            text=message,
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.BACKGROUND,
            justify="center"
        )
        message_label.pack(pady=(0, 10))
        
        # Автоматически скрываем сообщение через 3 секунды
        self.after(3000, lambda: message_frame.destroy())
    
    def show_success_message(self, message: str):
        """Показать сообщение об успешной отправке каравана"""
        message_frame = ctk.CTkFrame(
            self,
            fg_color=RomanTheme.SUCCESS,
            corner_radius=10,
            height=200
        )
        message_frame.pack(fill="x", pady=(0, 10), padx=50)
        message_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            message_frame,
            text="🚀 КАРАВАН ОТПРАВЛЕН",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.BACKGROUND
        )
        title_label.pack(pady=(20, 10))
        
        message_label = ctk.CTkLabel(
            message_frame,
            text=message,
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.BACKGROUND,
            justify="center"
        )
        message_label.pack(pady=(0, 10))
        
        # Кнопка возврата в главное меню
        return_button = ctk.CTkButton(
            message_frame,
            text="🏛️ Вернуться в главное меню",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.BACKGROUND,
            hover_color="#e0d5c8",
            text_color=RomanTheme.SUCCESS,
            corner_radius=8,
            width=250,
            height=40,
            command=self.on_back
        )
        return_button.pack(pady=(10, 20))


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
            
            player = Player(balance=5000, max_cycles=20)
            player.couriers = [courier]
            player.wagons = [wagon]
            player.inventory = {
                "Шелк": 15,
                "Специи": 10,
                "Вино": 8,
                "Зерно": 20,
                "Оливковое масло": 5
            }
            
            # Настраиваем игру
            self.player = player
            self.cities = cities
            self.goods = goods
            self.config = config
            self.difficulty = "normal"
            self.current_cycle = 1
            self.max_cycles = 20
            self.active_caravans = []
        
        def form_caravan(self, courier, wagon, goods_selection, city):
            from models.caravan import Caravan
            caravan = Caravan(
                courier=courier,
                wagon=wagon,
                goods=goods_selection,
                destination=city,
                days_to_travel=city.distance,
                departure_cycle=self.current_cycle,
                arrival_cycle=self.current_cycle + city.distance,
                return_cycle=self.current_cycle + city.distance * 2 + 1
            )
            self.active_caravans.append(caravan)
            return caravan
    
    def test_back():
        print("Возврат в главное меню")
    
    # Создаем тестовое приложение
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.title("Тест экрана отправки караванов")
    root.geometry("1200x800")
    root.configure(fg_color=RomanTheme.BACKGROUND)
    
    # Создаем мок-игру
    mock_game = MockGame()
    
    # Создаем экран
    screen = SendCaravanScreen(
        parent=root,
        game=mock_game,  # type: ignore
        on_back=test_back
    )
    screen.pack(fill="both", expand=True)
    
    root.mainloop()
