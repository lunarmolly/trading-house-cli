"""
Экран покупки товаров и просмотра склада для игры "Торговый дом"
Стилизован под Древний Рим
"""

import customtkinter as ctk
from typing import Callable, Optional
from core.game import Game
from models.goods_item import GoodsItem


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
    ERROR = "#8b4513"           # Цвет ошибки (коричневый)
    
    # Шрифты
    FONT_FAMILY = "Georgia"
    FONT_TITLE = ("Georgia", 28, "bold")
    FONT_HEADER = ("Georgia", 20, "bold")
    FONT_TEXT = ("Georgia", 14)
    FONT_BUTTON = ("Georgia", 16, "bold")
    FONT_SMALL = ("Georgia", 12)
    FONT_INFO = ("Georgia", 16)
    FONT_PRICE = ("Georgia", 14, "bold")


class ShopInventoryScreen(ctk.CTkFrame):
    """Экран покупки товаров и просмотра склада"""
    
    def __init__(self, parent, game: Game, on_back: Callable):
        super().__init__(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        self.game = game
        self.on_back = on_back
        
        # Состояние покупки
        self.selected_good: Optional[GoodsItem] = None
        self.quantity_entry: Optional[ctk.CTkEntry] = None
        self.purchase_frame: Optional[ctk.CTkFrame] = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Создание виджетов экрана"""
        
        # Заголовок (фиксированный)
        header_frame = ctk.CTkFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            height=120
        )
        header_frame.pack(fill="x", pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Основной заголовок
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏪 ТОРГОВАЯ ПЛОЩАДЬ 🏪",
            font=RomanTheme.FONT_TITLE,
            text_color=RomanTheme.ACCENT
        )
        title_label.pack(pady=(20, 10))
        
        # Баланс игрока
        balance_label = ctk.CTkLabel(
            header_frame,
            text=f"💰 Ваш баланс: {self.game.player.balance:,} денариев",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.SUCCESS if self.game.player.balance >= 1000 else RomanTheme.TEXT
        )
        balance_label.pack(pady=(0, 10))
        
        # Основная область с прокруткой
        main_scrollable = ctk.CTkScrollableFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            scrollbar_button_color=RomanTheme.BUTTON,
            scrollbar_button_hover_color=RomanTheme.BUTTON_HOVER
        )
        main_scrollable.pack(fill="both", expand=True, padx=20, pady=(10, 10))
        
        # Создание секций
        self.create_shop_section(main_scrollable)
        self.create_inventory_section(main_scrollable)
        self.create_bottom_panel()
    
    def create_shop_section(self, parent):
        """Создание секции покупки товаров"""
        
        # Заголовок секции магазина
        shop_title_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.ACCENT,
            corner_radius=10,
            height=50
        )
        shop_title_frame.pack(fill="x", pady=(20, 15), padx=20)
        shop_title_frame.pack_propagate(False)
        
        shop_title_label = ctk.CTkLabel(
            shop_title_frame,
            text="⚖️ ДОСТУПНЫЕ ТОВАРЫ ⚖️",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.BACKGROUND
        )
        shop_title_label.pack(expand=True)
        
        # Фрейм для списка товаров
        goods_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=2,
            corner_radius=10
        )
        goods_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        # Заголовки таблицы
        headers_frame = ctk.CTkFrame(
            goods_frame,
            fg_color=RomanTheme.BUTTON,
            corner_radius=8
        )
        headers_frame.pack(fill="x", pady=15, padx=15)
        
        # Создание заголовков
        self.create_table_header(headers_frame)
        
        # Список товаров
        for good in self.game.goods:
            self.create_goods_row(goods_frame, good)
        
        # Область для покупки (изначально скрыта)
        self.purchase_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.ACCENT,
            border_width=2,
            corner_radius=10
        )
        # Не показываем сразу
    
    def create_table_header(self, parent):
        """Создание заголовков таблицы товаров"""
        
        headers = [
            ("Товар", 0.3),
            ("Категория", 0.2),
            ("Цена за ед.", 0.2),
            ("Действие", 0.3)
        ]
        
        for i, (header_text, width_ratio) in enumerate(headers):
            header_label = ctk.CTkLabel(
                parent,
                text=header_text,
                font=RomanTheme.FONT_BUTTON,
                text_color=RomanTheme.BACKGROUND
            )
            header_label.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            parent.grid_columnconfigure(i, weight=int(width_ratio * 10))
    
    def create_goods_row(self, parent, good: GoodsItem):
        """Создание строки с товаром"""
        
        row_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.NEUTRAL,
            border_width=1,
            corner_radius=5
        )
        row_frame.pack(fill="x", pady=5, padx=15)
        
        # Название товара
        name_label = ctk.CTkLabel(
            row_frame,
            text=good.name,
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT,
            anchor="w"
        )
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Категория
        category_label = ctk.CTkLabel(
            row_frame,
            text=good.category,
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.NEUTRAL,
            anchor="center"
        )
        category_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Цена
        price_label = ctk.CTkLabel(
            row_frame,
            text=f"{good.base_price:,} ден.",
            font=RomanTheme.FONT_PRICE,
            text_color=RomanTheme.ACCENT,
            anchor="center"
        )
        price_label.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Кнопка покупки
        buy_button = ctk.CTkButton(
            row_frame,
            text="🛒 Купить",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=5,
            width=120,
            height=35,
            command=lambda g=good: self.start_purchase(g)
        )
        buy_button.grid(row=0, column=3, padx=10, pady=10)
        
        # Настройка сетки
        for i in range(4):
            row_frame.grid_columnconfigure(i, weight=[3, 2, 2, 3][i])
    
    def start_purchase(self, good: GoodsItem):
        """Начать процесс покупки товара"""
        self.selected_good = good
        
        # Показываем область покупки
        self.purchase_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        # Очищаем предыдущее содержимое
        for widget in self.purchase_frame.winfo_children():
            widget.destroy()
        
        # Заголовок покупки
        purchase_title = ctk.CTkLabel(
            self.purchase_frame,
            text=f"🛒 Покупка: {good.name}",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.ACCENT
        )
        purchase_title.pack(pady=(15, 10))
        
        # Информация о товаре
        info_frame = ctk.CTkFrame(
            self.purchase_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        info_frame.pack(pady=10)
        
        info_text = f"Категория: {good.category} | Цена за единицу: {good.base_price:,} денариев"
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        info_label.pack(pady=10, padx=20)
        
        # Поле ввода количества
        input_frame = ctk.CTkFrame(
            self.purchase_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        input_frame.pack(pady=10)
        
        quantity_label = ctk.CTkLabel(
            input_frame,
            text="Количество:",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        quantity_label.pack(side="left", padx=(20, 10))
        
        self.quantity_entry = ctk.CTkEntry(
            input_frame,
            font=RomanTheme.FONT_TEXT,
            width=100,
            placeholder_text="1"
        )
        self.quantity_entry.pack(side="left", padx=(0, 20))
        
        # Кнопки действий
        buttons_frame = ctk.CTkFrame(
            self.purchase_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        buttons_frame.pack(pady=(10, 15))
        
        # Кнопка подтверждения
        confirm_button = ctk.CTkButton(
            buttons_frame,
            text="✅ Подтвердить покупку",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.SUCCESS,
            hover_color="#5a7c1f",
            text_color=RomanTheme.BACKGROUND,
            corner_radius=8,
            width=180,
            height=40,
            command=self.confirm_purchase
        )
        confirm_button.pack(side="left", padx=10)
        
        # Кнопка отмены
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="❌ Отмена",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.WARNING,
            hover_color="#b8762f",
            text_color=RomanTheme.BACKGROUND,
            corner_radius=8,
            width=120,
            height=40,
            command=self.cancel_purchase
        )
        cancel_button.pack(side="left", padx=10)
        
        # Фокус на поле ввода
        self.quantity_entry.focus()
    
    def confirm_purchase(self):
        """Подтвердить покупку"""
        if not self.selected_good or not self.quantity_entry:
            return
        
        try:
            quantity_text = self.quantity_entry.get().strip()
            if not quantity_text:
                self.show_error("Введите количество товара")
                return
            
            quantity = int(quantity_text)
            if quantity <= 0:
                self.show_error("Количество должно быть положительным числом")
                return
            
            total_price = self.selected_good.base_price * quantity
            
            if total_price > self.game.player.balance:
                self.show_error(f"Недостаточно средств!\nТребуется: {total_price:,} денариев\nДоступно: {self.game.player.balance:,} денариев")
                return
            
            # Выполняем покупку
            self.game.player.add_goods(self.selected_good, quantity)
            self.game.player.adjust_balance(-total_price)
            
            # Показываем успешное сообщение
            self.show_success(f"Успешно куплено!\n{quantity} ед. '{self.selected_good.name}'\nза {total_price:,} денариев")
            
            # Обновляем интерфейс
            self.refresh_screen()
            self.cancel_purchase()
            
        except ValueError:
            self.show_error("Введите корректное число")
    
    def cancel_purchase(self):
        """Отменить покупку"""
        if self.purchase_frame:
            self.purchase_frame.pack_forget()
        self.selected_good = None
        self.quantity_entry = None
    
    def create_inventory_section(self, parent):
        """Создание секции склада"""
        
        # Заголовок секции склада
        inventory_title_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BUTTON,
            corner_radius=10,
            height=50
        )
        inventory_title_frame.pack(fill="x", pady=(20, 15), padx=20)
        inventory_title_frame.pack_propagate(False)
        
        inventory_title_label = ctk.CTkLabel(
            inventory_title_frame,
            text="🗃️ ВАШ СКЛАД 🗃️",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.BACKGROUND
        )
        inventory_title_label.pack(expand=True)
        
        # Фрейм для склада
        warehouse_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=2,
            corner_radius=10
        )
        warehouse_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        # Проверяем, есть ли товары на складе
        if not self.game.player.inventory or all(qty == 0 for qty in self.game.player.inventory.values()):
            empty_label = ctk.CTkLabel(
                warehouse_frame,
                text="📦 Склад пуст\n\nПриобретите товары для начала торговли",
                font=RomanTheme.FONT_TEXT,
                text_color=RomanTheme.NEUTRAL,
                justify="center"
            )
            empty_label.pack(pady=40)
        else:
            # Заголовки таблицы склада
            warehouse_headers_frame = ctk.CTkFrame(
                warehouse_frame,
                fg_color=RomanTheme.NEUTRAL,
                corner_radius=8
            )
            warehouse_headers_frame.pack(fill="x", pady=15, padx=15)
            
            # Заголовки для склада
            name_header = ctk.CTkLabel(
                warehouse_headers_frame,
                text="Товар",
                font=RomanTheme.FONT_BUTTON,
                text_color=RomanTheme.BACKGROUND
            )
            name_header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            
            qty_header = ctk.CTkLabel(
                warehouse_headers_frame,
                text="Количество",
                font=RomanTheme.FONT_BUTTON,
                text_color=RomanTheme.BACKGROUND
            )
            qty_header.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            
            warehouse_headers_frame.grid_columnconfigure(0, weight=7)
            warehouse_headers_frame.grid_columnconfigure(1, weight=3)
            
            # Строки со складскими товарами
            for item_name, quantity in self.game.player.inventory.items():
                if quantity > 0:  # Показываем только товары с количеством > 0
                    self.create_inventory_row(warehouse_frame, item_name, quantity)
    
    def create_inventory_row(self, parent, item_name: str, quantity: int):
        """Создание строки склада"""
        
        row_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.NEUTRAL,
            border_width=1,
            corner_radius=5
        )
        row_frame.pack(fill="x", pady=3, padx=15)
        
        # Название товара
        name_label = ctk.CTkLabel(
            row_frame,
            text=item_name,
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT,
            anchor="w"
        )
        name_label.grid(row=0, column=0, padx=15, pady=8, sticky="ew")
        
        # Количество
        quantity_label = ctk.CTkLabel(
            row_frame,
            text=f"{quantity:,} ед.",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.ACCENT,
            anchor="center"
        )
        quantity_label.grid(row=0, column=1, padx=15, pady=8, sticky="ew")
        
        # Настройка сетки
        row_frame.grid_columnconfigure(0, weight=7)
        row_frame.grid_columnconfigure(1, weight=3)
    
    def create_bottom_panel(self):
        """Создание нижней панели с кнопкой возврата"""
        
        bottom_frame = ctk.CTkFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            height=80
        )
        bottom_frame.pack(side="bottom", fill="x", pady=10)
        bottom_frame.pack_propagate(False)
        
        # Кнопка возврата
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
        """Показать сообщение об ошибке в самом экране"""
        self.show_message(message, RomanTheme.ERROR, "⚠️ ОШИБКА ⚠️")
    
    def show_success(self, message: str):
        """Показать сообщение об успехе в самом экране"""
        self.show_message(message, RomanTheme.SUCCESS, "✅ УСПЕХ ✅")
    
    def show_message(self, message: str, color: str, title: str):
        """Показать сообщение в верхней части экрана"""
        # Создаем временное сообщение
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
    
    def refresh_screen(self):
        """Обновление экрана после покупки"""
        # Пересоздаем виджеты для обновления данных
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()


# Пример использования для тестирования
if __name__ == "__main__":
    # Заглушка для тестирования без полной игры
    class MockGoodsItem:
        def __init__(self, name, base_price, category):
            self.name = name
            self.base_price = base_price
            self.category = category
    
    class MockPlayer:
        def __init__(self):
            self.balance = 5000
            self.inventory = {
                "Шелк": 10,
                "Специи": 5,
                "Вино": 8,
                "Золото": 2
            }
        
        def add_goods(self, item, quantity):
            self.inventory[item.name] = self.inventory.get(item.name, 0) + quantity
        
        def adjust_balance(self, amount):
            self.balance += amount
    
    class MockGame:
        def __init__(self):
            self.player = MockPlayer()
            self.goods = [
                MockGoodsItem("Шелк", 100, "Ткани"),
                MockGoodsItem("Специи", 80, "Пища"),
                MockGoodsItem("Вино", 60, "Напитки"),
                MockGoodsItem("Золото", 500, "Металлы"),
                MockGoodsItem("Керамика", 40, "Изделия"),
                MockGoodsItem("Оливковое масло", 70, "Пища")
            ]
    
    def test_back():
        print("Возврат в главное меню")
    
    # Создаем тестовое окно
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.title("Тест экрана магазина и склада")
    root.geometry("1200x800")
    root.configure(fg_color=RomanTheme.BACKGROUND)
    
    # Создаем мок-игру
    mock_game = MockGame()
    
    # Создаем экран
    screen = ShopInventoryScreen(
        parent=root,
        game=mock_game,
        on_back=test_back
    )
    screen.pack(fill="both", expand=True)
    
    root.mainloop()
