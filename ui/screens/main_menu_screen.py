"""
Главное меню игрока для игры "Торговый дом"
Стилизован под Древний Рим
"""

import customtkinter as ctk
from typing import Callable, Optional
from core.game import Game


class RomanTheme:
    """Античная римская тема для GUI"""
    
    # Цветовая схема
    BACKGROUND = "#f0e5d1"      # Фон (цвет пергамента)
    ACCENT = "#6d6923"          # Акценты (оливковый)
    BUTTON = "#947153"          # Кнопки и бордюры (бронза)
    TEXT = "#372e29"            # Цвет текста (темно-коричневый)
    NEUTRAL = "#acacac"         # Нейтральные элементы
    
    # Дополнительные цвета
    BUTTON_HOVER = "#a0815e"    # Кнопки при наведении
    FRAME_BORDER = "#8b6f47"    # Бордюры рамок
    SUCCESS = "#6b8e23"         # Цвет успеха (оливково-зеленый)
    WARNING = "#cd853f"         # Цвет предупреждения (песочно-коричневый)
    
    # Шрифты
    FONT_FAMILY = "Georgia"
    FONT_TITLE = ("Georgia", 28, "bold")
    FONT_HEADER = ("Georgia", 20, "bold")
    FONT_TEXT = ("Georgia", 14)
    FONT_BUTTON = ("Georgia", 16, "bold")
    FONT_SMALL = ("Georgia", 12)
    FONT_INFO = ("Georgia", 16)


class MainMenuScreen(ctk.CTkFrame):
    """Экран главного меню игрока"""
    
    def __init__(self, parent, game: Game, callbacks: dict):
        super().__init__(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        self.game = game
        self.callbacks = callbacks
        
        self.create_widgets()
    
    def create_widgets(self):
        """Создание виджетов экрана"""
        
        # Заголовок (фиксированный)
        header_frame = ctk.CTkFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            height=180
        )
        header_frame.pack(fill="x", pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Основной заголовок
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏛️ ТОРГОВЫЙ ДОМ 🏛️",
            font=RomanTheme.FONT_TITLE,
            text_color=RomanTheme.ACCENT
        )
        title_label.pack(pady=(20, 10))
        
        # Информационная панель
        self.create_info_panel(header_frame)
        
        # Основная область с кнопками (прокручиваемая)
        scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            scrollbar_button_color=RomanTheme.BUTTON,
            scrollbar_button_hover_color=RomanTheme.BUTTON_HOVER
        )
        scrollable_frame.pack(fill="both", expand=True, padx=50, pady=(10, 10))
        
        # Фрейм для кнопок действий
        actions_frame = ctk.CTkFrame(
            scrollable_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        actions_frame.pack(fill="x", pady=20, padx=20)
        
        # Создание кнопок меню
        self.create_menu_buttons(actions_frame)
        
        # Нижняя панель со статусом игры (фиксированная)
        bottom_frame = ctk.CTkFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            height=80
        )
        bottom_frame.pack(side="bottom", fill="x", pady=10)
        bottom_frame.pack_propagate(False)
        
        # Статус игры и мотивирующий текст
        self.create_status_panel(bottom_frame)
    
    def create_info_panel(self, parent):
        """Создание информационной панели с данными игрока"""
        
        info_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=2,
            corner_radius=10
        )
        info_frame.pack(pady=(10, 20), padx=100, fill="x")
        
        # Верхняя строка с основной информацией
        main_info_frame = ctk.CTkFrame(
            info_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        main_info_frame.pack(fill="x", padx=15, pady=(15, 8))
        
        # Цикл
        cycle_label = ctk.CTkLabel(
            main_info_frame,
            text=f"⏳ Цикл: {self.game.current_cycle} / {self.game.max_cycles}",
            font=RomanTheme.FONT_INFO,
            text_color=RomanTheme.TEXT
        )
        cycle_label.pack(side="left", padx=(0, 30))
        
        # Баланс
        balance_color = RomanTheme.SUCCESS if self.game.player.balance >= 5000 else RomanTheme.TEXT
        balance_label = ctk.CTkLabel(
            main_info_frame,
            text=f"💰 Баланс: {self.game.player.balance:,} денариев",
            font=RomanTheme.FONT_INFO,
            text_color=balance_color
        )
        balance_label.pack(side="left", padx=(0, 30))
        
        # Уровень сложности
        difficulty_text = {
            "easy": "🛡️ Легкий",
            "normal": "⚔️ Средний", 
            "hard": "🔥 Сложный"
        }.get(self.game.difficulty, self.game.difficulty.upper())
        
        difficulty_label = ctk.CTkLabel(
            main_info_frame,
            text=f"Сложность: {difficulty_text}",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.NEUTRAL
        )
        difficulty_label.pack(side="right")
        
        # Дополнительная информация
        additional_info_frame = ctk.CTkFrame(
            info_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        additional_info_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Активные караваны
        active_caravans = len(self.game.active_caravans)
        caravans_label = ctk.CTkLabel(
            additional_info_frame,
            text=f"🚛 Активные караваны: {active_caravans}",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        caravans_label.pack(side="left", padx=(0, 30))
        
        # Товары на складе
        inventory_count = len([item for item, qty in self.game.player.inventory.items() if qty > 0])
        inventory_label = ctk.CTkLabel(
            additional_info_frame,
            text=f"📦 Товаров на складе: {inventory_count} видов",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        inventory_label.pack(side="left")
        
        # Цель игры
        goal_progress = (self.game.player.balance / 10000) * 100
        goal_color = RomanTheme.SUCCESS if goal_progress >= 100 else RomanTheme.WARNING
        goal_label = ctk.CTkLabel(
            additional_info_frame,
            text=f"🎯 Цель: {goal_progress:.1f}% (10,000 денариев)",
            font=RomanTheme.FONT_TEXT,
            text_color=goal_color
        )
        goal_label.pack(side="right")
    
    def create_menu_buttons(self, parent):
        """Создание кнопок главного меню"""
        
        # Заголовок секции
        section_label = ctk.CTkLabel(
            parent,
            text="⚖️ ДЕЙСТВИЯ ТОРГОВЦА ⚖️",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.ACCENT
        )
        section_label.pack(pady=(20, 30))
        
        # Конфигурация кнопок меню
        menu_buttons = [
            {
                "text": "🏛️ Посмотреть города",
                "description": "Изучите доступные города для торговли",
                "callback": "show_cities",
                "icon": "🏛️"
            },
            {
                "text": "🚛 Посмотреть активные караваны", 
                "description": "Проверьте статус отправленных караванов",
                "callback": "show_caravans",
                "icon": "🚛"
            },
            {
                "text": "📦 Отправить новый караван",
                "description": "Сформируйте и отправьте караван в город",
                "callback": "send_caravan",
                "icon": "📦"
            },
            {
                "text": "🏪 Купить товары",
                "description": "Закупите товары для торговли",
                "callback": "buy_goods",
                "icon": "🏪"
            },
            # {
            #     "text": "🗃️ Посмотреть склад",
            #     "description": "Просмотрите запасы на складе",
            #     "callback": "show_inventory",
            #     "icon": "🗃️"
            # },
            {
                "text": "⏭️ Перейти к следующему циклу",
                "description": "Завершите текущий цикл и перейдите к следующему",
                "callback": "next_cycle",
                "icon": "⏭️",
                "style": "accent"
            }
        ]
        
        # Создание кнопок
        for i, button_config in enumerate(menu_buttons):
            self.create_action_button(parent, button_config, i)
        
        # Разделитель
        separator = ctk.CTkFrame(
            parent,
            height=2,
            fg_color=RomanTheme.FRAME_BORDER
        )
        separator.pack(fill="x", pady=30, padx=100)
        
        # Кнопка завершения игры
        quit_button_config = {
            "text": "🚪 Завершить игру",
            "description": "Выйти из текущей игры и вернуться в главное меню",
            "callback": "quit_game",
            "icon": "🚪",
            "style": "warning"
        }
        self.create_action_button(parent, quit_button_config, len(menu_buttons), is_quit=True)
    
    def create_action_button(self, parent, config: dict, index: int, is_quit: bool = False):
        """Создание кнопки действия с описанием"""
        
        # Определяем стиль кнопки
        if config.get("style") == "accent":
            button_color = RomanTheme.ACCENT
            button_hover = "#5a5a1e"
        elif config.get("style") == "warning" or is_quit:
            button_color = RomanTheme.WARNING
            button_hover = "#b8762f"
        else:
            button_color = RomanTheme.BUTTON
            button_hover = RomanTheme.BUTTON_HOVER
        
        # Фрейм для кнопки с описанием
        button_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=1,
            corner_radius=10
        )
        button_frame.pack(pady=8, padx=40, fill="x")
        
        # Основная кнопка
        action_button = ctk.CTkButton(
            button_frame,
            text=config["text"],
            font=RomanTheme.FONT_BUTTON,
            fg_color=button_color,
            hover_color=button_hover,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=2,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=8,
            width=400,
            height=50,
            command=lambda: self.handle_action(config["callback"])
        )
        action_button.pack(pady=(15, 8), padx=20)
        
        # Описание действия
        description_label = ctk.CTkLabel(
            button_frame,
            text=config["description"],
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.NEUTRAL,
            justify="center"
        )
        description_label.pack(pady=(0, 15))
        
        # Добавляем эффект наведения на весь фрейм
        self.add_button_hover_effect(button_frame, action_button)
    
    def add_button_hover_effect(self, frame, button):
        """Добавляет эффект наведения на фрейм кнопки"""
        original_border_color = frame.cget("border_color")
        
        def on_enter(event):
            frame.configure(border_color=RomanTheme.ACCENT)
        
        def on_leave(event):
            frame.configure(border_color=original_border_color)
        
        # Привязываем события
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def create_status_panel(self, parent):
        """Создание панели статуса игры"""
        
        # Проверка состояния игры
        if self.game.is_game_over():
            if self.game.has_won():
                status_text = "🏆 ПОБЕДА! Вы достигли цели!"
                status_color = RomanTheme.SUCCESS
            else:
                status_text = "⏰ Время истекло. Игра окончена."
                status_color = RomanTheme.WARNING
        else:
            cycles_left = self.game.max_cycles - self.game.current_cycle
            if cycles_left <= 3:
                status_text = f"⚠️ Осталось циклов: {cycles_left}"
                status_color = RomanTheme.WARNING
            else:
                status_text = f"📅 Осталось циклов: {cycles_left}"
                status_color = RomanTheme.TEXT
        
        status_label = ctk.CTkLabel(
            parent,
            text=status_text,
            font=RomanTheme.FONT_TEXT,
            text_color=status_color
        )
        status_label.pack(pady=(10, 5))
        
        # Мотивирующая фраза
        motivation_texts = [
            "\"Fortuna audaces iuvat\" — Фортуна благоволит смелым",
            "\"Per aspera ad astra\" — Через тернии к звездам", 
            "\"Audentes fortuna juvat\" — Смелым помогает судьба",
            "\"Veni, vidi, vici\" — Пришел, увидел, победил"
        ]
        
        import random
        motivation_text = random.choice(motivation_texts)
        
        motivation_label = ctk.CTkLabel(
            parent,
            text=motivation_text,
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.NEUTRAL,
            justify="center"
        )
        motivation_label.pack(pady=(0, 10))
    
    def handle_action(self, action: str):
        """Обработка действий пользователя"""
        if action in self.callbacks and self.callbacks[action]:
            self.callbacks[action]()
        else:
            print(f"Действие '{action}' еще не реализовано")
    
    def refresh_info(self):
        """Обновление информации на экране"""
        # Пересоздаем виджеты для обновления данных
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()


# Пример использования для тестирования
if __name__ == "__main__":
    # Заглушка для тестирования без полной игры
    class MockGame:
        def __init__(self):
            self.current_cycle = 5
            self.max_cycles = 20
            self.difficulty = "normal"
            self.active_caravans = []
            
            class MockPlayer:
                def __init__(self):
                    self.balance = 7500
                    self.inventory = {"Шелк": 10, "Специи": 5, "Вино": 0}
            
            self.player = MockPlayer()
        
        def is_game_over(self):
            return False
        
        def has_won(self):
            return self.player.balance >= 10000
    
    def test_callback():
        print("Кнопка нажата!")
    
    # Создаем тестовое окно
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.title("Тест главного меню")
    root.geometry("1200x800")
    root.configure(fg_color=RomanTheme.BACKGROUND)
    
    # Создаем мок-игру
    mock_game = MockGame()
    
    # Создаем callbacks
    callbacks = {
        "show_cities": test_callback,
        "show_caravans": test_callback,
        "send_caravan": test_callback,
        "buy_goods": test_callback,
        "show_inventory": test_callback,
        "next_cycle": test_callback,
        "quit_game": test_callback
    }
    
    # Создаем экран
    screen = MainMenuScreen(
        parent=root,
        game=mock_game,
        callbacks=callbacks
    )
    screen.pack(fill="both", expand=True)
    
    root.mainloop()