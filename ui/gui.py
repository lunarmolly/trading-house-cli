"""
GUI интерфейс для игры "Торговый дом" - Древний Рим
Использует customtkinter с античной римской тематикой
"""

import customtkinter as ctk
import sys
import os
from typing import Optional

# Добавляем корневую папку в путь для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.world import load_balance_config, generate_world
from core.goods import load_goods
from models.player import Player
from models.courier import Courier
from models.wagon import Wagon
from core.game import Game
from screens.difficulty_screen import DifficultyScreen, RomanTheme

__all__ = ['TradingHouseGUI', 'RomanTheme']


class TradingHouseGUI:
    """Главный класс GUI приложения"""
    
    def __init__(self):
        # Настройка темы customtkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Создание главного окна
        self.root = ctk.CTk()
        self.root.title("🏛️ Торговый Дом - Древний Рим")
        self.root.geometry("1920x1080")
        self.root.configure(fg_color=RomanTheme.BACKGROUND)
        
        # Центрирование окна
        self.center_window()
        
        # Игровые объекты
        self.game: Optional[Game] = None
        self.current_frame: Optional[ctk.CTkFrame] = None
        
        # Создание стартового экрана
        self.create_start_screen()
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = 1920
        height = 1080
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def clear_screen(self):
        """Очистка экрана от текущего фрейма"""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None
    
    def create_start_screen(self):
        """Создание стартового экрана"""
        self.clear_screen()
        
        # Основной фрейм
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = main_frame
        
        # Заголовок игры
        title_label = ctk.CTkLabel(
            main_frame,
            text="🏛️ ТОРГОВЫЙ ДОМ 🏛️",
            font=RomanTheme.FONT_TITLE,
            text_color=RomanTheme.ACCENT
        )
        title_label.pack(pady=(50, 20))
        
        # Подзаголовок
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Древний Рим • Торговая Империя",
            font=RomanTheme.FONT_HEADER,
            text_color=RomanTheme.TEXT
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Центральная текстовая область с описанием
        description_frame = ctk.CTkFrame(
            main_frame,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=3,
            corner_radius=15
        )
        description_frame.pack(pady=30, padx=100, fill="both", expand=True)
        
        description_text = """
Добро пожаловать в мир античной торговли!

Вы — владелец торгового дома в великой Римской империи. 
Ваша цель — построить торговую империю, отправляя караваны 
в дальние города, торгуя экзотическими товарами и накапливая 
богатство.

Управляйте курьерами, выбирайте товары с умом, учитывайте 
спрос в различных городах и остерегайтесь опасностей дорог.

Достигните цели в 10,000 денариев за ограниченное время 
и станьте владельцем роскошной виллы у моря!

Ave Caesar! Fortuna audaces iuvat!
        """
        
        description_label = ctk.CTkLabel(
            description_frame,
            text=description_text.strip(),
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT,
            justify="center",
            wraplength=800
        )
        description_label.pack(pady=40, padx=40, expand=True)
        
        # Кнопка "Начать игру"
        start_button = ctk.CTkButton(
            main_frame,
            text="⚔️ НАЧАТЬ ИГРУ ⚔️",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=2,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=10,
            width=300,
            height=60,
            command=self.show_difficulty_selection
        )
        start_button.pack(pady=40)
        
        # Дополнительные кнопки
        button_frame = ctk.CTkFrame(
            main_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        button_frame.pack(pady=20)
        
        # Кнопка выхода
        exit_button = ctk.CTkButton(
            button_frame,
            text="Выход",
            font=RomanTheme.FONT_TEXT,
            fg_color=RomanTheme.NEUTRAL,
            hover_color="#999999",
            text_color=RomanTheme.TEXT,
            corner_radius=8,
            width=120,
            height=40,
            command=self.exit_game
        )
        exit_button.pack(side="left", padx=10)
        
        # Информация о версии
        version_label = ctk.CTkLabel(
            main_frame,
            text="Версия 1.0 | Античная Торговая Симуляция",
            font=RomanTheme.FONT_SMALL,
            text_color=RomanTheme.NEUTRAL
        )
        version_label.pack(side="bottom", pady=20)
      def show_difficulty_selection(self):
        """Экран выбора сложности"""
        self.clear_screen()
        
        # Создаем экран выбора сложности
        difficulty_screen = DifficultyScreen(
            parent=self.root,
            on_difficulty_selected=self.start_game,
            on_back=self.create_start_screen
        )
        difficulty_screen.pack(fill="both", expand=True)
        self.current_frame = difficulty_screen
    
    def start_game(self, difficulty: str):
        """Запуск игры с выбранным уровнем сложности"""
        try:
            # Загрузка конфигурации
            config = self.load_game_config(difficulty)
            
            # Генерация мира и товаров
            cities = generate_world(config)
            goods = load_goods(config)
            
            # Создание игрока
            player = self.create_player(config, difficulty)
            
            # Инициализация игры
            self.game = Game(
                player=player,
                cities=cities,
                goods=goods,
                config=config,
                difficulty=difficulty
            )
            
            # Переход к главному меню игры
            self.show_main_menu()
            
        except Exception as e:
            self.show_error(f"Ошибка при запуске игры: {str(e)}")
    
    def load_game_config(self, difficulty: str) -> dict:
        """Загрузка конфигурации игры"""
        config_path = "data/balance_config.json"
        if not os.path.exists(config_path):
            config_path = "balance_config.json"
        
        return load_balance_config(path=config_path, difficulty=difficulty)
    
    def create_player(self, config: dict, difficulty: str) -> Player:
        """Создание игрока с учетом уровня сложности"""
        # Настройки баланса
        starting_balance = config["player"]["starting_balance"]
        if "difficulty_settings" in config and difficulty in config["difficulty_settings"]:
            settings = config["difficulty_settings"][difficulty]
            starting_balance = int(starting_balance * settings.get("starting_balance_multiplier", 1.0))

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
    
    def show_main_menu(self):
        """Показать главное меню игры"""
        # Здесь будет реализовано главное меню игры
        # Пока просто заглушка
        self.clear_screen()
        
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = main_frame
        
        # Заголовок
        title_label = ctk.CTkLabel(
            main_frame,
            text="🏛️ ТОРГОВЫЙ ДОМ 🏛️",
            font=RomanTheme.FONT_TITLE,
            text_color=RomanTheme.ACCENT
        )
        title_label.pack(pady=30)
        
        # Информация о игре
        if self.game:
            info_text = f"""
Цикл: {self.game.current_cycle} / {self.game.max_cycles}
Баланс: {self.game.player.balance} денариев
Уровень сложности: {self.game.difficulty.upper()}
            """
            
            info_label = ctk.CTkLabel(
                main_frame,
                text=info_text.strip(),
                font=RomanTheme.FONT_HEADER,
                text_color=RomanTheme.TEXT,
                justify="center"
            )
            info_label.pack(pady=20)
        
        # Заглушка - главное меню будет реализовано позже
        placeholder_label = ctk.CTkLabel(
            main_frame,
            text="🚧 Главное меню игры в разработке 🚧\n\nВозвращаемся к стартовому экрану...",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT,
            justify="center"
        )
        placeholder_label.pack(pady=50, expand=True)
        
        # Кнопка возврата
        back_button = ctk.CTkButton(
            main_frame,
            text="← Вернуться к началу",
            font=RomanTheme.FONT_TEXT,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=8,
            width=200,
            height=40,
            command=self.create_start_screen
        )
        back_button.pack(pady=20)
    
    def show_error(self, message: str):
        """Показать сообщение об ошибке"""
        self.clear_screen()
        
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = main_frame
        
        # Заголовок ошибки
        error_label = ctk.CTkLabel(
            main_frame,
            text="⚠️ ОШИБКА ⚠️",
            font=RomanTheme.FONT_TITLE,
            text_color="red"
        )
        error_label.pack(pady=50)
        
        # Сообщение об ошибке
        message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT,
            justify="center",
            wraplength=800
        )
        message_label.pack(pady=30, expand=True)
        
        # Кнопка возврата
        back_button = ctk.CTkButton(
            main_frame,
            text="← Вернуться к началу",
            font=RomanTheme.FONT_TEXT,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=8,
            width=200,
            height=40,
            command=self.create_start_screen
        )
        back_button.pack(pady=20)
    
    def exit_game(self):
        """Выход из игры"""
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Запуск GUI приложения"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nИгра завершена пользователем")
        except Exception as e:
            print(f"Критическая ошибка GUI: {e}")
        finally:
            try:
                self.root.destroy()
            except:
                pass


if __name__ == "__main__":
    app = TradingHouseGUI()
    app.run()
