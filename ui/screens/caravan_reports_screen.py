"""
Экран отчетов о завершенных караванах
"""

import customtkinter as ctk
from ui.screens.difficulty_screen import RomanTheme


class CaravanReportsScreen(ctk.CTkFrame):
    """Экран отображения отчетов о завершенных караванах"""
    
    def __init__(self, parent, reports: list, on_continue=None):
        super().__init__(parent, fg_color=RomanTheme.BACKGROUND, corner_radius=0)
        
        self.reports = reports
        self.on_continue = on_continue
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        # Заголовок
        title_label = ctk.CTkLabel(
            self,
            text="🏛️ ОТЧЕТЫ О КАРАВАНАХ 🏛️",
            font=RomanTheme.FONT_TITLE,
            text_color=RomanTheme.ACCENT
        )
        title_label.pack(pady=(30, 20))
        
        # Подзаголовок
        subtitle_label = ctk.CTkLabel(
            self,
            text="Сводка завершенных экспедиций",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.TEXT
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Основная область с отчетами
        reports_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=10,
            border_width=2,
            border_color=RomanTheme.FRAME_BORDER
        )
        reports_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        if not self.reports:
            # Если нет отчетов
            no_reports_label = ctk.CTkLabel(
                reports_frame,
                text="🏺 В этом цикле караваны не завершились 🏺",
                font=RomanTheme.FONT_TEXT,
                text_color=RomanTheme.NEUTRAL
            )
            no_reports_label.pack(pady=50)
        else:
            # Отображаем отчеты
            for i, report in enumerate(self.reports):
                self.create_report_widget(reports_frame, report, i + 1)
        
        # Кнопка продолжения
        continue_button = ctk.CTkButton(
            self,
            text="⚔️ ПРОДОЛЖИТЬ ⚔️",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=8,
            width=250,
            height=50,
            command=self.continue_game
        )
        continue_button.pack(pady=20)
    
    def create_report_widget(self, parent, report: dict, caravan_num: int):
        """Создает виджет для одного отчета о караване"""
        # Фрейм для отчета
        report_frame = ctk.CTkFrame(
            parent,
            fg_color="#f8f5f0",
            corner_radius=10,
            border_width=1,
            border_color=RomanTheme.FRAME_BORDER
        )
        report_frame.pack(fill="x", padx=10, pady=10)
        
        # Заголовок каравана
        caravan_title = ctk.CTkLabel(
            report_frame,
            text=f"🚛 КАРАВАН #{caravan_num} ЗАВЕРШЕН",
            font=("Georgia", 18, "bold"),
            text_color=RomanTheme.ACCENT
        )
        caravan_title.pack(pady=(15, 10))
        
        # События
        events_frame = ctk.CTkFrame(
            report_frame,
            fg_color="#f0ede7",
            corner_radius=8
        )
        events_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        event_path_label = ctk.CTkLabel(
            events_frame,
            text=f"🛤️ Событие в пути: {report['event_path']}",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        event_path_label.pack(pady=(10, 5), anchor="w", padx=15)
        
        event_city_label = ctk.CTkLabel(
            events_frame,
            text=f"🏛️ Событие в городе: {report['event_city']}",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        event_city_label.pack(pady=(0, 10), anchor="w", padx=15)
        
        # Товары
        if report['sale_breakdown']:
            goods_frame = ctk.CTkFrame(
                report_frame,
                fg_color="#ebe8e1",
                corner_radius=8
            )
            goods_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            goods_title = ctk.CTkLabel(
                goods_frame,
                text="📦 ПРОДАННЫЕ ТОВАРЫ:",
                font=("Georgia", 14, "bold"),
                text_color=RomanTheme.TEXT
            )
            goods_title.pack(pady=(10, 5))
            
            for name, data in report['sale_breakdown'].items():
                # Название товара и основная информация
                goods_info = ctk.CTkLabel(
                    goods_frame,
                    text=f"• {name}: {data['qty']} ед. × {data['unit_price']} денариев (базовая цена: {data['base_price']})",
                    font=RomanTheme.FONT_TEXT,
                    text_color=RomanTheme.TEXT
                )
                goods_info.pack(anchor="w", padx=20, pady=2)
                
                # Модификаторы
                modifiers_text = f"   Модификаторы: город {data['city_mod']:+.2f}, событие {data['event_mod']:+.2f}, дальность {data['dist_mod']:+.2f}"
                modifiers_label = ctk.CTkLabel(
                    goods_frame,
                    text=modifiers_text,
                    font=("Consolas", 12),
                    text_color=RomanTheme.NEUTRAL
                )
                modifiers_label.pack(anchor="w", padx=20, pady=1)
                
                # Итоговый множитель
                multiplier_label = ctk.CTkLabel(
                    goods_frame,
                    text=f"   Итоговый множитель: {data['final_mod']:.2f}",
                    font=("Consolas", 12, "bold"),
                    text_color=RomanTheme.TEXT
                )
                multiplier_label.pack(anchor="w", padx=20, pady=(1, 8))
        
        # Финансовая сводка
        finance_frame = ctk.CTkFrame(
            report_frame,
            fg_color="#e6e2db",
            corner_radius=8
        )
        finance_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        finance_title = ctk.CTkLabel(
            finance_frame,
            text="💰 ФИНАНСОВЫЙ ИТОГ:",
            font=("Georgia", 14, "bold"),
            text_color=RomanTheme.TEXT
        )
        finance_title.pack(pady=(10, 5))
        
        # Определяем цвет для чистого дохода
        net_color = "#228B22" if report['net'] > 0 else "#DC143C" if report['net'] < 0 else RomanTheme.TEXT
        
        profit_label = ctk.CTkLabel(
            finance_frame,
            text=f"📈 Прибыль: {report['profit']} денариев",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        profit_label.pack(anchor="w", padx=20, pady=2)
        
        expenses_label = ctk.CTkLabel(
            finance_frame,
            text=f"📉 Расходы: {report['expenses']} денариев",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT
        )
        expenses_label.pack(anchor="w", padx=20, pady=2)
        
        net_label = ctk.CTkLabel(
            finance_frame,
            text=f"💵 Чистый доход: {report['net']} денариев",
            font=("Georgia", 14, "bold"),
            text_color=net_color
        )
        net_label.pack(anchor="w", padx=20, pady=(2, 10))
    
    def continue_game(self):
        """Продолжить игру"""
        if self.on_continue:
            self.on_continue()
