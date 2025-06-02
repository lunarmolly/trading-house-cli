"""
Экран выбора сложности для игры "Торговый дом"
Стилизован под Древний Рим
"""

import customtkinter as ctk
from typing import Callable, Optional


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
    
    # Шрифты
    FONT_FAMILY = "Georgia"
    FONT_TITLE = ("Georgia", 28, "bold")
    FONT_HEADER = ("Georgia", 20, "bold")
    FONT_TEXT = ("Georgia", 14)
    FONT_BUTTON = ("Georgia", 16, "bold")
    FONT_SMALL = ("Georgia", 12)


class DifficultyScreen(ctk.CTkFrame):
    """Экран выбора уровня сложности"""
    
    def __init__(self, parent, on_difficulty_selected: Callable[[str], None], on_back: Optional[Callable[[], None]] = None):
        super().__init__(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        self.on_difficulty_selected = on_difficulty_selected
        self.on_back = on_back
        
        self.create_widgets()
    
    def create_widgets(self):
        """Создание виджетов экрана"""
        
        # Заголовок (фиксированный)
        header_frame = ctk.CTkFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            height=150
        )
        header_frame.pack(fill="x", pady=(20, 0))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚖️ ВЫБОР УРОВНЯ СЛОЖНОСТИ ⚖️",
            font=RomanTheme.FONT_TITLE,
            text_color=RomanTheme.ACCENT
        )
        title_label.pack(pady=(20, 10))
        
        # Подзаголовок с античной тематикой
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Выберите испытание для вашего торгового пути",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.TEXT
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Создаем прокручиваемую область для основного контента
        scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            scrollbar_button_color=RomanTheme.BUTTON,
            scrollbar_button_hover_color=RomanTheme.BUTTON_HOVER
        )
        scrollable_frame.pack(fill="both", expand=True, padx=50, pady=(10, 10))
        
        # Основной фрейм для кнопок сложности внутри прокручиваемой области
        difficulty_frame = ctk.CTkFrame(
            scrollable_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        difficulty_frame.pack(fill="x", pady=20, padx=20)
        
        # Конфигурация уровней сложности с римскими символами
        difficulties = [
            {
                "name": "🛡️ ЛЕГКИЙ",
                "level": "easy",
                "subtitle": "Путь Новичка",
                "description": "• Больше стартовых ресурсов\n• Меньше рисков в путешествиях\n• Благоприятные торговые условия\n• Идеально для изучения игры",
                "latin": "Via Facilior"
            },
            {
                "name": "⚔️ СРЕДНИЙ", 
                "level": "normal",
                "subtitle": "Путь Торговца",
                "description": "• Стандартный баланс ресурсов\n• Умеренные риски и награды\n• Классический игровой опыт\n• Для опытных стратегов",
                "latin": "Via Mercatoris"
            },
            {
                "name": "🔥 СЛОЖНЫЙ",
                "level": "hard", 
                "subtitle": "Путь Императора",
                "description": "• Ограниченные стартовые ресурсы\n• Высокие риски, большие награды\n• Суровые условия торговли\n• Только для мастеров",
                "latin": "Via Imperatoris"
            }
        ]
          # Создание карточек уровней сложности
        for i, diff in enumerate(difficulties):
            self.create_difficulty_card(difficulty_frame, diff, i)
        
        # Нижняя панель с кнопкой назад и мотивирующим текстом (фиксированная)
        bottom_frame = ctk.CTkFrame(
            self,
            fg_color=RomanTheme.BACKGROUND,
            height=100
        )
        bottom_frame.pack(side="bottom", fill="x", pady=10)
        bottom_frame.pack_propagate(False)
        
        # Мотивирующий текст
        motivation_label = ctk.CTkLabel(
            bottom_frame,
            text="\"Audentes fortuna iuvat\" — Фортуна благоволит смелым",
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.NEUTRAL,
            justify="center"
        )
        motivation_label.pack(pady=(10, 5))
        
        # Кнопка назад (если предоставлен callback)
        if self.on_back:
            back_button = ctk.CTkButton(
                bottom_frame,
                text="← Назад",
                font=RomanTheme.FONT_TEXT,
                fg_color=RomanTheme.NEUTRAL,
                hover_color="#999999",
                text_color=RomanTheme.TEXT,
                corner_radius=8,
                width=120,
                height=40,
                command=self.on_back
            )
            back_button.pack(pady=(0, 10))
    def create_difficulty_card(self, parent, difficulty_data: dict, index: int):
        """Создание карточки уровня сложности"""
        
        # Основной фрейм карточки с бронзовой рамкой
        card_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=3,
            corner_radius=15
        )
        card_frame.pack(pady=15, padx=20, fill="x")
        
        # Верхняя часть с названием и латинским текстом
        header_frame = ctk.CTkFrame(
            card_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        header_frame.pack(fill="x", padx=15, pady=(15, 8))
        
        # Название уровня
        name_label = ctk.CTkLabel(
            header_frame,
            text=difficulty_data["name"],
            font=("Georgia", 18, "bold"),
            text_color=RomanTheme.ACCENT
        )
        name_label.pack()
        
        # Подзаголовок
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=difficulty_data["subtitle"],
            font=("Georgia", 15),
            text_color=RomanTheme.TEXT
        )
        subtitle_label.pack(pady=(3, 0))
        
        # Латинское название
        latin_label = ctk.CTkLabel(
            header_frame,
            text=f"({difficulty_data['latin']})",
            font=("Georgia", 11, "italic"),
            text_color=RomanTheme.NEUTRAL
        )
        latin_label.pack(pady=(2, 0))
        
        # Центральная часть с описанием
        description_frame = ctk.CTkFrame(
            card_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        description_frame.pack(fill="x", padx=15, pady=8)
        
        description_label = ctk.CTkLabel(
            description_frame,
            text=difficulty_data["description"],
            font=("Georgia", 13),
            text_color=RomanTheme.TEXT,
            justify="left"
        )
        description_label.pack(pady=8)
        
        # Кнопка выбора
        select_button = ctk.CTkButton(
            card_frame,
            text=f"ВЫБРАТЬ {difficulty_data['subtitle'].upper()}",
            font=("Georgia", 15, "bold"),
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=2,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=10,
            width=250,
            height=45,
            command=lambda level=difficulty_data["level"]: self.select_difficulty(level)
        )
        select_button.pack(pady=(8, 15))
        
        # Добавляем эффект наведения на всю карточку
        self.add_card_hover_effect(card_frame, select_button)
    
    def add_card_hover_effect(self, card_frame, button):
        """Добавляет эффект наведения на карточку"""
        original_border_color = card_frame.cget("border_color")
        
        def on_enter(event):
            card_frame.configure(border_color=RomanTheme.ACCENT)
        
        def on_leave(event):
            card_frame.configure(border_color=original_border_color)
        
        # Привязываем события к фрейму карточки
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        
        # Рекурсивно привязываем к дочерним виджетам
        def bind_to_children(widget):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            for child in widget.winfo_children():
                try:
                    bind_to_children(child)
                except:
                    pass
        
        bind_to_children(card_frame)
    
    def select_difficulty(self, difficulty: str):
        """Обработка выбора уровня сложности"""
        self.on_difficulty_selected(difficulty)


# Пример использования для тестирования
if __name__ == "__main__":
    def test_difficulty_selected(difficulty):
        print(f"Выбран уровень сложности: {difficulty}")
    
    def test_back():
        print("Возврат назад")
    
    # Создаем тестовое окно
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.title("Тест экрана сложности")
    root.geometry("1000x700")  # Уменьшили размер для тестирования прокрутки
    root.configure(fg_color=RomanTheme.BACKGROUND)
    
    # Создаем экран
    screen = DifficultyScreen(
        parent=root,
        on_difficulty_selected=test_difficulty_selected,
        on_back=test_back
    )
    screen.pack(fill="both", expand=True)
    
    root.mainloop()
