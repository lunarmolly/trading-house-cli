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
        
        # Фрейм для списка товаров с прокруткой
        self.goods_container = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=2,
            corner_radius=10
        )
        self.goods_container.pack(fill="x", pady=(0, 20), padx=20)
        
        # Заголовки таблицы (фиксированные)
        headers_frame = ctk.CTkFrame(
            self.goods_container,
            fg_color=RomanTheme.BUTTON,
            corner_radius=8,
            height=45
        )
        headers_frame.pack(fill="x", pady=(15, 10), padx=15)
        headers_frame.pack_propagate(False)
        
        # Создание заголовков с фиксированными столбцами
        self.create_table_header(headers_frame)
        
        # Контейнер для строк товаров
        self.goods_rows_frame = ctk.CTkFrame(
            self.goods_container,
            fg_color=RomanTheme.BACKGROUND
        )
        self.goods_rows_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Список товаров
        for i, good in enumerate(self.game.goods):
            self.create_goods_row(self.goods_rows_frame, good, i)
    def create_table_header(self, parent):
        """Создание заголовков таблицы товаров с фиксированной шириной"""
        
        # Настройка grid для равномерного распределения
        parent.grid_columnconfigure(0, weight=3, minsize=200)  # Товар
        parent.grid_columnconfigure(1, weight=2, minsize=150)  # Категория
        parent.grid_columnconfigure(2, weight=2, minsize=150)  # Цена
        parent.grid_columnconfigure(3, weight=2, minsize=120)  # Действие
        
        headers = [
            "Товар",
            "Категория", 
            "Цена за ед.",
            "Действие"
        ]
        
        for i, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(
                parent,
                text=header_text,
                font=RomanTheme.FONT_BUTTON,
                text_color=RomanTheme.BACKGROUND
            )
            header_label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
    
    def create_goods_row(self, parent, good: GoodsItem, row_index: int):
        """Создание строки с товаром с inline формой покупки"""
        
        # Основной контейнер строки
        row_container = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND
        )
        row_container.pack(fill="x", pady=2)
        
        # Основная строка товара
        main_row_frame = ctk.CTkFrame(
            row_container,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.NEUTRAL,
            border_width=1,
            corner_radius=5,
            height=45
        )
        main_row_frame.pack(fill="x", side="top")
        main_row_frame.pack_propagate(False)
        
        # Настройка сетки точно как в заголовке
        main_row_frame.grid_columnconfigure(0, weight=3, minsize=200)
        main_row_frame.grid_columnconfigure(1, weight=2, minsize=150)
        main_row_frame.grid_columnconfigure(2, weight=2, minsize=150)
        main_row_frame.grid_columnconfigure(3, weight=2, minsize=120)
        
        # Название товара
        name_label = ctk.CTkLabel(
            main_row_frame,
            text=good.name,
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT,
            anchor="w"
        )
        name_label.grid(row=0, column=0, padx=10, pady=8, sticky="ew")
        
        # Категория
        category_label = ctk.CTkLabel(
            main_row_frame,
            text=good.category,
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.NEUTRAL,
            anchor="center"
        )
        category_label.grid(row=0, column=1, padx=5, pady=8, sticky="ew")
        
        # Цена
        price_label = ctk.CTkLabel(
            main_row_frame,
            text=f"{good.base_price:,} ден.",
            font=RomanTheme.FONT_PRICE,
            text_color=RomanTheme.ACCENT,
            anchor="center"
        )
        price_label.grid(row=0, column=2, padx=5, pady=8, sticky="ew")
        
        # Кнопка покупки
        buy_button = ctk.CTkButton(
            main_row_frame,
            text="🛒 Купить",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=5,
            width=100,
            height=30,
            command=lambda g=good, container=row_container: self.toggle_purchase_form(g, container)
        )
        buy_button.grid(row=0, column=3, padx=5, pady=8)
        
        # Скрытая форма покупки (изначально не показана)
        purchase_form = ctk.CTkFrame(
            row_container,
            fg_color=RomanTheme.ACCENT,
            corner_radius=8,
            height=80
        )
        # Не показываем сразу - будет показана при клике на кнопку
        
        # Сохраняем ссылки для управления
        setattr(row_container, 'purchase_form', purchase_form)
        setattr(row_container, 'good', good)
        setattr(row_container, 'is_form_shown', False)
    
    def toggle_purchase_form(self, good: GoodsItem, row_container):
        """Показать/скрыть форму покупки для конкретной строки"""
        
        # Скрываем все другие формы покупки
        for widget in self.goods_rows_frame.winfo_children():
            if hasattr(widget, 'purchase_form') and hasattr(widget, 'is_form_shown'):
                if widget != row_container and widget.is_form_shown:
                    widget.purchase_form.pack_forget()
                    widget.is_form_shown = False
        
        # Переключаем текущую форму
        if not row_container.is_form_shown:
            self.show_purchase_form(good, row_container)
        else:
            self.hide_purchase_form(row_container)
    
    def show_purchase_form(self, good: GoodsItem, row_container):
        """Показать форму покупки для товара"""
        purchase_form = row_container.purchase_form
        
        # Очищаем предыдущее содержимое
        for widget in purchase_form.winfo_children():
            widget.destroy()
        
        # Настройка формы покупки
        purchase_form.pack(fill="x", pady=(5, 0))
        purchase_form.pack_propagate(False)
        
        # Создаем grid layout для формы
        purchase_form.grid_columnconfigure(0, weight=1)
        purchase_form.grid_columnconfigure(1, weight=1)
        purchase_form.grid_columnconfigure(2, weight=1)
        purchase_form.grid_columnconfigure(3, weight=1)
        
        # Информация о покупке
        info_label = ctk.CTkLabel(
            purchase_form,
            text=f"Покупка: {good.name} ({good.base_price:,} ден./ед.)",
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.BACKGROUND
        )
        info_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        
        # Поле ввода количества
        quantity_label = ctk.CTkLabel(
            purchase_form,
            text="Кол-во:",
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.BACKGROUND
        )
        quantity_label.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="e")
        
        quantity_entry = ctk.CTkEntry(
            purchase_form,
            font=RomanTheme.FONT_SMALL,
            width=60,
            height=25,
            placeholder_text="1"
        )
        quantity_entry.grid(row=1, column=1, padx=(0, 10), pady=(0, 10), sticky="w")
        
        # Кнопка подтверждения
        confirm_button = ctk.CTkButton(
            purchase_form,
            text="✓ OK",
            font=RomanTheme.FONT_SMALL,
            fg_color=RomanTheme.SUCCESS,
            hover_color="#5a7c1f",
            text_color=RomanTheme.BACKGROUND,
            corner_radius=5,
            width=50,
            height=25,
            command=lambda: self.confirm_purchase_inline(good, quantity_entry, row_container)
        )
        confirm_button.grid(row=1, column=2, padx=5, pady=(0, 10))
        
        # Кнопка отмены
        cancel_button = ctk.CTkButton(
            purchase_form,
            text="✗",
            font=RomanTheme.FONT_SMALL,
            fg_color=RomanTheme.WARNING,
            hover_color="#b8762f",
            text_color=RomanTheme.BACKGROUND,
            corner_radius=5,
            width=30,
            height=25,
            command=lambda: self.hide_purchase_form(row_container)
        )
        cancel_button.grid(row=1, column=3, padx=(0, 10), pady=(0, 10))
        
        # Фокус на поле ввода
        quantity_entry.focus()
        
        # Отмечаем, что форма показана
        row_container.is_form_shown = True
        self.selected_good = good
        self.quantity_entry = quantity_entry
    
    def hide_purchase_form(self, row_container):
        """Скрыть форму покупки"""
        row_container.purchase_form.pack_forget()
        row_container.is_form_shown = False
        self.selected_good = None
        self.quantity_entry = None
    
    def confirm_purchase_inline(self, good: GoodsItem, quantity_entry: ctk.CTkEntry, row_container):
        """Подтвердить покупку из inline формы"""
        try:
            quantity_text = quantity_entry.get().strip()
            if not quantity_text:
                self.show_error("Введите количество товара")
                return
            
            quantity = int(quantity_text)
            if quantity <= 0:
                self.show_error("Количество должно быть положительным числом")
                return
            
            total_price = good.base_price * quantity
            
            if total_price > self.game.player.balance:
                self.show_error(f"Недостаточно средств!\nТребуется: {total_price:,} денариев\nДоступно: {self.game.player.balance:,} денариев")
                return
            
            # Выполняем покупку
            self.game.player.add_goods(good, quantity)
            self.game.player.adjust_balance(-total_price)
            
            # Показываем успешное сообщение
            self.show_success(f"Успешно куплено!\n{quantity} ед. '{good.name}' за {total_price:,} денариев")
            
            # Скрываем форму покупки
            self.hide_purchase_form(row_container)
            
            # Обновляем интерфейс
            self.refresh_screen()
            
        except ValueError:
            self.show_error("Введите корректное число")
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
        game=mock_game,  # type: ignore
        on_back=test_back
    )
    screen.pack(fill="both", expand=True)
    
    root.mainloop()
