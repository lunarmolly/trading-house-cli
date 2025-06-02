"""
Экран статуса караванов для игры "Торговый дом"
Отображает информацию о караванах в пути и завершённых караванах
"""

import customtkinter as ctk
from typing import Optional, Dict, List, Callable

from core.game import Game
from ui.screens.difficulty_screen import RomanTheme


class CaravansStatusScreen(ctk.CTkFrame):
    """
    Экран отображения статуса караванов:
    - Активные караваны (в пути)
    - Завершённые караваны
    """
    
    def __init__(self, parent, game: Game, on_back: Callable[[], None]):
        super().__init__(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        self.game = game
        self.on_back = on_back
        
        self.create_widgets()
        
    def create_widgets(self):
        """Создание виджетов экрана караванов"""
        
        # Главный контейнер
        main_container = ctk.CTkFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок
        title_label = ctk.CTkLabel(
            main_container,
            text="🏛️ КАРАВАНЫ И ТОРГОВЫЕ МИССИИ 🏛️",
            font=RomanTheme.FONT_TITLE,
            text_color=RomanTheme.ACCENT
        )
        title_label.pack(pady=(20, 30))
        
        # Создаем прокручиваемый фрейм для содержимого
        scrollable_container = ctk.CTkScrollableFrame(
            main_container,
            fg_color=RomanTheme.BACKGROUND,
            scrollbar_fg_color=RomanTheme.BUTTON,
            scrollbar_button_color=RomanTheme.BUTTON_HOVER,
            scrollbar_button_hover_color=RomanTheme.BUTTON_HOVER
        )
        scrollable_container.pack(fill="both", expand=True, padx=10, pady=10)        # Разделение караванов на активные и завершенные
        active_caravans = []
        completed_reports = []
        
        # Активные караваны - те, что еще не завершились
        for caravan in self.game.active_caravans:
            if self.game.current_cycle < caravan.return_cycle:
                active_caravans.append(caravan)
                
        # Завершенные караваны - берем из отчетов
        completed_reports = self.game.caravan_reports[-10:]  # Показываем последние 10 отчетов
        
        # Отладочная информация
        print(f"DEBUG: Активных караванов: {len(active_caravans)}")
        print(f"DEBUG: Всего караванов в игре: {len(self.game.active_caravans)}")
        print(f"DEBUG: Отчетов о завершенных: {len(completed_reports)}")
        print(f"DEBUG: Всего отчетов: {len(self.game.caravan_reports)}")
        print(f"DEBUG: Текущий цикл: {self.game.current_cycle}")
                
        # Блок активных караванов
        if active_caravans:
            self.create_caravans_section(
                scrollable_container,
                "💠 КАРАВАНЫ В ПУТИ",
                active_caravans,
                is_active=True
            )
        else:
            # Сообщение, если нет активных караванов
            no_active_label = ctk.CTkLabel(
                scrollable_container,
                text="У вас нет караванов в пути",
                font=RomanTheme.FONT_TEXT,
                text_color=RomanTheme.TEXT
            )
            no_active_label.pack(pady=20)
            
        # Разделитель
        separator = ctk.CTkFrame(
            scrollable_container,
            height=2,
            fg_color=RomanTheme.NEUTRAL
        )
        separator.pack(fill="x", padx=30, pady=20)
              # Блок завершенных караванов
        if completed_reports:
            self.create_completed_reports_section(
                scrollable_container,
                "🏁 ЗАВЕРШЁННЫЕ КАРАВАНЫ",
                completed_reports
            )
        else:
            # Сообщение, если нет завершенных караванов
            no_completed_label = ctk.CTkLabel(
                scrollable_container,
                text="У вас нет завершённых караванов",
                font=RomanTheme.FONT_TEXT,
                text_color=RomanTheme.TEXT
            )
            no_completed_label.pack(pady=20)
        
        # Информационный текст
        info_text = "Караваны возвращаются в Рим после продажи товаров. Прибыль зависит от событий в пути и на рынках городов."
        info_label = ctk.CTkLabel(
            main_container,
            text=info_text,
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.TEXT
        )
        info_label.pack(pady=10)
        
        # Кнопка возврата
        back_button = ctk.CTkButton(
            main_container,
            text="← Вернуться в главное меню",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=10,
            width=250,
            height=40,
            command=self.on_back
        )
        back_button.pack(pady=20)
    
    def create_caravans_section(self, parent, title: str, caravans: list, is_active: bool):
        """
        Создаёт секцию с караванами (активными или завершёнными)
        
        Args:
            parent: Родительский виджет
            title: Заголовок секции
            caravans: Список караванов
            is_active: True для активных караванов, False для завершённых
        """
        # Контейнер секции
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_width=2,
            border_color=RomanTheme.FRAME_BORDER,
            corner_radius=10
        )
        section_frame.pack(fill="x", padx=10, pady=10, ipady=10)
        
        # Заголовок секции
        section_label = ctk.CTkLabel(
            section_frame,
            text=title,
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.ACCENT
        )
        section_label.pack(pady=(10, 15))
        
        # Перебираем все караваны в секции
        for idx, caravan in enumerate(caravans):
            self.create_caravan_card(section_frame, caravan, is_active)
              # Добавляем разделитель между карточками (кроме последней)
            if idx < len(caravans) - 1:
                separator = ctk.CTkFrame(
                    section_frame,
                    height=1,
                    fg_color=RomanTheme.NEUTRAL
                )
                separator.pack(fill="x", padx=60, pady=10)
    
    def create_caravan_card(self, parent, caravan, is_active: bool):
        """
        Создаёт карточку для отображения информации о караване
        
        Args:
            parent: Родительский виджет
            caravan: Объект каравана
            is_active: True для активных караванов, False для завершённых
        """
        # Контейнер карточки
        card_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=5
        )
        card_frame.pack(fill="x", padx=20, pady=10)
        
        # Главная информация
        header_frame = ctk.CTkFrame(card_frame, fg_color=RomanTheme.BACKGROUND)
        header_frame.pack(fill="x", pady=5, padx=10)
        
        # Название города
        city_name = ctk.CTkLabel(
            header_frame,
            text=f"🏙️ {caravan.destination.name}",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        city_name.pack(side="left", padx=(0, 20))
        
        # Статус
        status_text = "В пути" if is_active else "Завершён"
        status_color = "#6d6923" if is_active else "#8b6f47"  # Оливковый для активных, бронза для завершенных
        status_label = ctk.CTkLabel(
            header_frame,
            text=f"Статус: {status_text}",
            font=RomanTheme.FONT_TEXT,
            text_color=status_color
        )
        status_label.pack(side="right", padx=10)
        
        # Информация о циклах
        cycles_frame = ctk.CTkFrame(card_frame, fg_color=RomanTheme.BACKGROUND)
        cycles_frame.pack(fill="x", pady=5, padx=10)
        
        cycles_text = f"Отправка: {caravan.departure_cycle} ⟶ Возврат: {caravan.return_cycle}"
        cycles_label = ctk.CTkLabel(
            cycles_frame,
            text=cycles_text,
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.TEXT
        )
        cycles_label.pack(side="left")
        
        # Событие в пути
        event_text = caravan.event_occurred if caravan.event_occurred else "Событий не было"
        event_label = ctk.CTkLabel(
            cycles_frame,
            text=f"Событие: {event_text}",
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.ACCENT
        )
        event_label.pack(side="right", padx=10)
        
        # Таблица товаров
        goods_frame = ctk.CTkFrame(
            card_frame, 
            fg_color=RomanTheme.BACKGROUND,
            border_width=1,
            border_color=RomanTheme.NEUTRAL,
            corner_radius=5
        )
        goods_frame.pack(fill="x", pady=10, padx=20)
        
        # Заголовки таблицы товаров
        headers_frame = ctk.CTkFrame(goods_frame, fg_color=RomanTheme.BACKGROUND)
        headers_frame.pack(fill="x", pady=(5, 0), padx=5)
        
        col_widths = [250, 60]
        headers = ["Товар", "Кол-во"]
        
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=(RomanTheme.FONT_FAMILY, 12, "bold"),
                width=col_widths[i] if i < len(col_widths) else 0,
                text_color=RomanTheme.TEXT
            )
            header_label.pack(side="left", padx=5)
        
        # Тонкий разделитель
        separator = ctk.CTkFrame(goods_frame, height=1, fg_color=RomanTheme.NEUTRAL)
        separator.pack(fill="x", padx=5, pady=(2, 5))
          # Строки таблицы с товарами
        total_cost = 0  # Для подсчета общей стоимости
        goods_dict = {g.name: g for g in self.game.goods}
        
        for name, quantity in caravan.goods.items():
            # Считаем стоимость товара
            if name in goods_dict:
                item_cost = goods_dict[name].base_price * quantity
                total_cost += item_cost
            else:
                item_cost = 0
                
            # Каждый товар - отдельная строка таблицы
            item_frame = ctk.CTkFrame(goods_frame, fg_color=RomanTheme.BACKGROUND)
            item_frame.pack(fill="x", pady=1, padx=5)
            
            # Название товара
            name_label = ctk.CTkLabel(
                item_frame,
                text=name,
                font=RomanTheme.FONT_SMALL,
                width=col_widths[0],
                anchor="w",
                text_color=RomanTheme.TEXT
            )
            name_label.pack(side="left", padx=5)
            
            # Количество
            qty_label = ctk.CTkLabel(
                item_frame,
                text=str(quantity),
                font=RomanTheme.FONT_SMALL,
                width=col_widths[1],
                text_color=RomanTheme.TEXT
            )
            qty_label.pack(side="left", padx=5)
            
            # Стоимость (если известна)
            if item_cost > 0:
                cost_label = ctk.CTkLabel(
                    item_frame,
                    text=f"{item_cost} 🪙",
                    font=RomanTheme.FONT_SMALL,
                    text_color=RomanTheme.TEXT
                )
                cost_label.pack(side="left", padx=5)
        
        # Дополнительная информация для завершенных караванов
        if not is_active:
            # Ищем отчет для этого каравана
            report = self.find_caravan_report(caravan)
            if report:
                # Информация о прибыли
                finance_frame = ctk.CTkFrame(card_frame, fg_color=RomanTheme.BACKGROUND)
                finance_frame.pack(fill="x", pady=5, padx=20)
                
                # Прибыль
                profit_text = f"Прибыль: {report['profit']} 🪙"
                profit_label = ctk.CTkLabel(
                    finance_frame,
                    text=profit_text,
                    font=RomanTheme.FONT_TEXT,
                    text_color="#6b8e23"  # Зеленоватый цвет для прибыли
                )
                profit_label.pack(side="left", padx=5)
                
                # Расходы
                expenses_text = f"Расходы: {report['expenses']} 🪙"
                expenses_label = ctk.CTkLabel(
                    finance_frame,
                    text=expenses_text,
                    font=RomanTheme.FONT_TEXT,
                    text_color="#cd853f"  # Коричневатый цвет для расходов
                )
                expenses_label.pack(side="left", padx=20)
                
                # Чистая прибыль
                net_color = "#6b8e23" if report["net"] >= 0 else "#cd5c5c"  # Зеленый или красный
                net_text = f"Чистая прибыль: {report['net']} 🪙"
                net_label = ctk.CTkLabel(
                    finance_frame,
                    text=net_text,
                    font=(RomanTheme.FONT_FAMILY, 14, "bold"),
                    text_color=net_color
                )
                net_label.pack(side="right", padx=5)
    def find_caravan_report(self, caravan):
        """
        Поиск финансового отчета для завершенного каравана
        
        Args:
            caravan: Объект каравана
            
        Returns:
            Dict: Финансовый отчет или None
        """
        # Получаем словарь товаров из игры для расчета стоимости
        goods_dict = {g.name: g for g in self.game.goods}
        
        # Рассчитываем примерную закупочную стоимость товаров
        total_purchase_cost = 0
        for name, quantity in caravan.goods.items():
            if name in goods_dict:
                total_purchase_cost += goods_dict[name].base_price * quantity
                
        # Определяем влияние событий на прибыль
        event_mod = 1.0
        extra_expenses = 0
        
        if caravan.event_occurred:
            if "разбойник" in caravan.event_occurred.lower():
                event_mod = 0.6  # Потеряли 40% товаров
            elif "поломка" in caravan.event_occurred.lower():
                extra_expenses = 30
            elif "болезнь" in caravan.event_occurred.lower():
                extra_expenses = 15
            elif "смерть" in caravan.event_occurred.lower():
                event_mod = 0.0  # Полная потеря товаров

        # Рассчитываем прибыль от продажи товаров с учетом расстояния
        # и спроса в городе назначения
        city_mod = 1.0 + (caravan.destination.duration * 0.02)
        profit = int(total_purchase_cost * city_mod * event_mod)
        
        # Базовые расходы на путешествие
        travel_days = caravan.days_to_travel * 2 + 1  # туда, обратно + день в городе
        expenses = int(10 * travel_days) + extra_expenses  # базовые расходы + дополнительные

        # Формируем отчет
        return {
            "profit": profit,
            "expenses": expenses,
            "net": profit - expenses,
            "event_path": caravan.event_occurred or "Нет событий",
            "event_city": caravan.destination.current_event or "Нет событий",
            "sale_breakdown": {},  # Детализация будет добавлена в будущем
            "success": profit > expenses
        }
    
    def create_completed_reports_section(self, parent, title: str, reports: list):
        """
        Создаёт секцию с завершёнными караванами из отчетов
        
        Args:
            parent: Родительский виджет
            title: Заголовок секции
            reports: Список отчетов о завершенных караванах
        """
        # Контейнер секции
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_width=2,
            border_color=RomanTheme.FRAME_BORDER,
            corner_radius=10
        )
        section_frame.pack(fill="x", padx=10, pady=10, ipady=10)
        
        # Заголовок секции
        section_label = ctk.CTkLabel(
            section_frame,
            text=title,
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.ACCENT
        )
        section_label.pack(pady=(10, 15))
        
        # Перебираем все отчеты в секции (в обратном порядке - сначала последние)
        for idx, report in enumerate(reversed(reports)):
            self.create_completed_report_card(section_frame, report)
            
            # Добавляем разделитель между карточками (кроме последней)
            if idx < len(reports) - 1:
                separator = ctk.CTkFrame(
                    section_frame,
                    height=1,
                    fg_color=RomanTheme.NEUTRAL
                )
                separator.pack(fill="x", padx=60, pady=10)

    def create_completed_report_card(self, parent, report):
        """
        Создаёт карточку для отображения отчета о завершенном караване
        
        Args:
            parent: Родительский виджет
            report: Отчет о завершенном караване
        """
        # Контейнер карточки
        card_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=5
        )
        card_frame.pack(fill="x", padx=20, pady=10)
        
        # Главная информация
        header_frame = ctk.CTkFrame(card_frame, fg_color=RomanTheme.BACKGROUND)
        header_frame.pack(fill="x", pady=5, padx=10)
        
        # Название города
        city_name = ctk.CTkLabel(
            header_frame,
            text=f"🏙️ {report['destination']}",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        city_name.pack(side="left", padx=(0, 20))
        
        # Статус
        status_label = ctk.CTkLabel(
            header_frame,
            text="Статус: Завершён",
            font=RomanTheme.FONT_TEXT,
            text_color="#8b6f47"  # Бронза для завершенных
        )
        status_label.pack(side="right", padx=10)
        
        # Информация о циклах
        cycles_frame = ctk.CTkFrame(card_frame, fg_color=RomanTheme.BACKGROUND)
        cycles_frame.pack(fill="x", pady=5, padx=10)
        
        cycles_text = f"Отправка: {report['departure_cycle']} ⟶ Возврат: {report['return_cycle']} ⟶ Завершён: {report['completion_cycle']}"
        cycles_label = ctk.CTkLabel(
            cycles_frame,
            text=cycles_text,
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.TEXT
        )
        cycles_label.pack(side="left")
        
        # События
        events_frame = ctk.CTkFrame(card_frame, fg_color=RomanTheme.BACKGROUND)
        events_frame.pack(fill="x", pady=5, padx=10)
        
        event_path = report.get("event_path", "Нет событий")
        event_city = report.get("event_city", "Нет событий")
        
        path_label = ctk.CTkLabel(
            events_frame,
            text=f"Событие в пути: {event_path}",
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.ACCENT
        )
        path_label.pack(side="left", padx=(0, 20))
        
        city_label = ctk.CTkLabel(
            events_frame,
            text=f"Событие в городе: {event_city}",
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.ACCENT
        )
        city_label.pack(side="left")
        
        # Таблица товаров
        goods_frame = ctk.CTkFrame(
            card_frame, 
            fg_color=RomanTheme.BACKGROUND,
            border_width=1,
            border_color=RomanTheme.NEUTRAL,
            corner_radius=5
        )
        goods_frame.pack(fill="x", pady=10, padx=20)
        
        # Заголовки таблицы товаров
        headers_frame = ctk.CTkFrame(goods_frame, fg_color=RomanTheme.BACKGROUND)
        headers_frame.pack(fill="x", pady=(5, 0), padx=5)
        
        col_widths = [200, 60, 100, 100]
        headers = ["Товар", "Кол-во", "Цена ед.", "Общая цена"]
        
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=(RomanTheme.FONT_FAMILY, 12, "bold"),
                width=col_widths[i] if i < len(col_widths) else 0,
                text_color=RomanTheme.TEXT
            )
            header_label.pack(side="left", padx=5)
        
        # Тонкий разделитель
        separator = ctk.CTkFrame(goods_frame, height=1, fg_color=RomanTheme.NEUTRAL)
        separator.pack(fill="x", padx=5, pady=(2, 5))
        
        # Строки таблицы с товарами
        sale_breakdown = report.get("sale_breakdown", {})
        goods_data = report.get("goods", {})
        
        for name, quantity in goods_data.items():
            # Каждый товар - отдельная строка таблицы
            item_frame = ctk.CTkFrame(goods_frame, fg_color=RomanTheme.BACKGROUND)
            item_frame.pack(fill="x", pady=1, padx=5)
            
            # Название товара
            name_label = ctk.CTkLabel(
                item_frame,
                text=name,
                font=RomanTheme.FONT_SMALL,
                width=col_widths[0],
                anchor="w",
                text_color=RomanTheme.TEXT
            )
            name_label.pack(side="left", padx=5)
            
            # Количество
            qty_label = ctk.CTkLabel(
                item_frame,
                text=str(quantity),
                font=RomanTheme.FONT_SMALL,
                width=col_widths[1],
                text_color=RomanTheme.TEXT
            )
            qty_label.pack(side="left", padx=5)
            
            # Цена за единицу и общая цена (если есть данные)
            if name in sale_breakdown:
                unit_price = sale_breakdown[name]["unit_price"]
                total_price = unit_price * quantity
                
                unit_price_label = ctk.CTkLabel(
                    item_frame,
                    text=f"{unit_price} 🪙",
                    font=RomanTheme.FONT_SMALL,
                    width=col_widths[2],
                    text_color=RomanTheme.TEXT
                )
                unit_price_label.pack(side="left", padx=5)
                
                total_price_label = ctk.CTkLabel(
                    item_frame,
                    text=f"{total_price} 🪙",
                    font=RomanTheme.FONT_SMALL,
                    width=col_widths[3],
                    text_color=RomanTheme.TEXT
                )
                total_price_label.pack(side="left", padx=5)
            else:
                # Заглушки, если нет данных
                unit_price_label = ctk.CTkLabel(
                    item_frame,
                    text="—",
                    font=RomanTheme.FONT_SMALL,
                    width=col_widths[2],
                    text_color=RomanTheme.NEUTRAL
                )
                unit_price_label.pack(side="left", padx=5)
                
                total_price_label = ctk.CTkLabel(
                    item_frame,
                    text="—",
                    font=RomanTheme.FONT_SMALL,
                    width=col_widths[3],
                    text_color=RomanTheme.NEUTRAL
                )
                total_price_label.pack(side="left", padx=5)
        
        # Финансовая информация
        finance_frame = ctk.CTkFrame(card_frame, fg_color=RomanTheme.BACKGROUND)
        finance_frame.pack(fill="x", pady=5, padx=20)
        
        # Прибыль
        profit_text = f"Прибыль: {report['profit']} 🪙"
        profit_label = ctk.CTkLabel(
            finance_frame,
            text=profit_text,
            font=RomanTheme.FONT_TEXT,
            text_color="#6b8e23"  # Зеленоватый цвет для прибыли
        )
        profit_label.pack(side="left", padx=5)
        
        # Расходы
        expenses_text = f"Расходы: {report['expenses']} 🪙"
        expenses_label = ctk.CTkLabel(
            finance_frame,
            text=expenses_text,
            font=RomanTheme.FONT_TEXT,
            text_color="#cd853f"  # Коричневатый цвет для расходов
        )
        expenses_label.pack(side="left", padx=20)
        
        # Чистая прибыль
        net_value = report.get('net', 0)
        net_color = "#6b8e23" if net_value >= 0 else "#cd5c5c"  # Зеленый или красный
        net_text = f"Чистая прибыль: {net_value} 🪙"
        net_label = ctk.CTkLabel(
            finance_frame,
            text=net_text,
            font=(RomanTheme.FONT_FAMILY, 14, "bold"),
            text_color=net_color
        )
        net_label.pack(side="right", padx=5)