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

# Импорты экранов из подпапки screens
from ui.screens.difficulty_screen import DifficultyScreen, RomanTheme
from ui.screens.main_menu_screen import MainMenuScreen
from ui.screens.shop_inventory_screen import ShopInventoryScreen
from ui.screens.send_caravan_screen import SendCaravanScreen

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
            ))        # Создание повозок
        wagons = [
            Wagon(
                name=wagon_data["name"],
                capacity=wagon_data["capacity"],
                durability=wagon_data.get("durability", 0.75)
            ) for wagon_data in config["player"].get("starting_wagons", [])
        ]        # Создаем игрока с начальными параметрами
        player = Player(starting_balance)
        player.couriers = couriers
        player.wagons = wagons
        
        return player
    
    def show_main_menu(self):
        """Показать главное меню игры"""
        if not self.game:
            self.show_error("Ошибка: игра не инициализирована")
            return
            
        self.clear_screen()
          # Создаем callbacks для действий меню
        menu_callbacks = {
            "show_cities": self.show_cities_placeholder,
            "show_caravans": self.show_caravans_placeholder,
            "send_caravan": self.send_caravan_screen,
            "buy_goods": self.buy_goods_placeholder,
            # "show_inventory": self.show_inventory_placeholder,
            "next_cycle": self.next_cycle_action,
            "quit_game": self.quit_to_start_screen
        }
        
        # Создаем экран главного меню
        main_menu_screen = MainMenuScreen(
            parent=self.root,
            game=self.game,
            callbacks=menu_callbacks
        )
        main_menu_screen.pack(fill="both", expand=True)
        self.current_frame = main_menu_screen
    
    # Заглушки для действий меню (будут реализованы позже)
    def show_cities_placeholder(self):
        """Заглушка для просмотра городов"""
        self.show_placeholder("Просмотр городов", "Список доступных городов для торговли")    
        
    def show_caravans_placeholder(self):
        """Заглушка для просмотра караванов"""
        self.show_placeholder("Активные караваны", "Статус отправленных караванов")
    
    def send_caravan_screen(self):
        """Экран отправки каравана"""
        if not self.game:
            self.show_error("Ошибка: игра не инициализирована")
            return
            
        self.clear_screen()
        
        # Создаем экран отправки каравана
        send_caravan_screen = SendCaravanScreen(
            parent=self.root,
            game=self.game,
            on_back=self.show_main_menu
        )
        send_caravan_screen.pack(fill="both", expand=True)
        self.current_frame = send_caravan_screen
    
    def buy_goods_placeholder(self):
        """Экран покупки товаров"""
        self.show_shop_inventory()
    
    # def show_inventory_placeholder(self):
    #     """Экран просмотра склада (объединен с покупкой товаров)"""
    #     self.show_shop_inventory()
    
    def show_shop_inventory(self):
        """Показать экран покупки товаров и склада"""
        if not self.game:
            self.show_error("Ошибка: игра не инициализирована")
            return
            
        self.clear_screen()
        
        # Создаем экран магазина и склада
        shop_screen = ShopInventoryScreen(
            parent=self.root,
            game=self.game,
            on_back=self.show_main_menu
        )
        shop_screen.pack(fill="both", expand=True)
        self.current_frame = shop_screen
    
    def next_cycle_action(self):
        """Переход к следующему циклу"""
        if not self.game:
            return
            
        self.game.next_cycle()
        self.game.update_caravans()
        
        # Проверяем, не закончилась ли игра
        if self.game.is_game_over():
            self.show_game_over()
        else:
            # Обновляем главное меню
            self.show_main_menu()
    
    def quit_to_start_screen(self):
        """Возврат к стартовому экрану"""
        self.game = None
        self.create_start_screen()
    
    def show_placeholder(self, title: str, description: str):
        """Показать заглушку для экрана"""
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
            text=f"🏛️ {title.upper()} 🏛️",
            font=RomanTheme.FONT_TITLE,
            text_color=RomanTheme.ACCENT
        )
        title_label.pack(pady=50)
        
        # Описание
        desc_label = ctk.CTkLabel(
            main_frame,
            text=f"🚧 {description} 🚧\n\nЭтот экран еще в разработке",
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT,
            justify="center"
        )
        desc_label.pack(pady=30, expand=True)
        
        # Кнопка возврата
        back_button = ctk.CTkButton(
            main_frame,
            text="← Вернуться в главное меню",
            font=RomanTheme.FONT_TEXT,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=8,
            width=250,
            height=40,
            command=self.show_main_menu
        )
        back_button.pack(pady=20)
    
    def show_game_over(self):
        """Показать экран окончания игры"""
        if not self.game:
            return
            
        self.clear_screen()
        
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = main_frame
        
        if self.game.has_won():
            # Победа
            title = "🏆 VICTORIA! 🏆"
            message = f"Поздравляем! Вы достигли цели!\n\nВаш итоговый баланс: {self.game.player.balance:,} денариев\nЦиклов потрачено: {self.game.current_cycle}\n\nВы стали владельцем роскошной виллы у моря!"
            color = "#6b8e23"  # SUCCESS color
        else:
            # Поражение
            title = "💀 GAME OVER 💀"
            message = f"Время истекло!\n\nВаш итоговый баланс: {self.game.player.balance:,} денариев\nЦель не достигнута.\n\nФортуна была не на вашей стороне..."
            color = "#cd853f"  # WARNING color
        
        # Заголовок
        title_label = ctk.CTkLabel(
            main_frame,
            text=title,
            font=RomanTheme.FONT_TITLE,
            text_color=color
        )
        title_label.pack(pady=50)
        
        # Сообщение
        message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=RomanTheme.FONT_TEXT,
            text_color=RomanTheme.TEXT,
            justify="center"
        )
        message_label.pack(pady=30, expand=True)
        
        # Кнопки
        button_frame = ctk.CTkFrame(
            main_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        button_frame.pack(pady=30)
        
        # Новая игра
        new_game_button = ctk.CTkButton(
            button_frame,
            text="🎮 Новая игра",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=8,
            width=200,
            height=50,
            command=self.show_difficulty_selection
        )
        new_game_button.pack(side="left", padx=10)
        
        # Главное меню
        menu_button = ctk.CTkButton(
            button_frame,
            text="🏛️ Главное меню",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.NEUTRAL,
            hover_color="#999999",
            text_color=RomanTheme.TEXT,
            corner_radius=8,
            width=200,
            height=50,
            command=self.create_start_screen
        )
        menu_button.pack(side="left", padx=10)
    
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
