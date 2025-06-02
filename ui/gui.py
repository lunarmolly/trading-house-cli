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
from models.audio import audio_manager
from core.game import Game

# Импорты экранов из подпапки screens
from ui.screens.difficulty_screen import DifficultyScreen, RomanTheme
from ui.screens.main_menu_screen import MainMenuScreen
from ui.screens.shop_inventory_screen import ShopInventoryScreen
from ui.screens.send_caravan_screen import SendCaravanScreen
from ui.screens.cities_overview_screen import CitiesOverviewScreen
from ui.screens.caravans_status_screen import CaravansStatusScreen

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
          # Получаем цель из конфигурации (по умолчанию 15000)
        config_path = "data/balance_config.json"
        if not os.path.exists(config_path):
            config_path = "balance_config.json"
            
        try:
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            victory_goal = config_data.get("player", {}).get("victory_goal", 15000)
        except:
            victory_goal = 15000
            
        description_text = f"""
Добро пожаловать в мир античной торговли!

Вы — владелец небольшого торгового дома в великой Римской империи. 
Однако судьба распорядилась так, что вы оказались в долгу перед 
влиятельным патрицием. Теперь ваша задача — заработать достаточно 
денариев, чтобы выплатить долг и вернуть свою честь.

Отправляйте караваны в дальние города, торгуйте редкими товарами 
и накапливайте богатство. Управляйте курьерами, выбирайте товары 
с умом, учитывайте спрос в различных городах и остерегайтесь 
опасностей дорог.

Сможете ли вы достичь цели в {victory_goal:,} денариев за 
ограниченное время и избежать позора? Или вас ждет судьба раба?

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
        
        # Панель управления аудио
        self.create_audio_controls(main_frame)
        
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
            player = self.create_player(config, difficulty)            # Инициализация игры
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
        ]        # Создаем игрока с начальными параметрами (баланс - позиционный аргумент)
        player = Player(starting_balance)
        player.couriers = couriers
        player.wagons = wagons
        
        return player
    
    def show_main_menu(self):
        """Показать главное меню игры"""
        if not self.game:
            self.show_error("Ошибка: игра не инициализирована")
            return
            
        self.clear_screen()        # Создаем callbacks для действий меню
        menu_callbacks = {
            "show_cities": self.show_cities_overview,
            "show_caravans": self.show_caravans_status,
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
    def show_cities_overview(self):
        """Экран просмотра городов"""
        if not self.game:
            self.show_error("Ошибка: игра не инициализирована")
            return
            
        self.clear_screen()
        
        # Создаем экран просмотра городов
        cities_screen = CitiesOverviewScreen(
            parent=self.root,
            game=self.game,
            on_back=self.show_main_menu
        )
        cities_screen.pack(fill="both", expand=True)
        self.current_frame = cities_screen
    def show_caravans_status(self):
        """Экран просмотра статуса караванов"""
        if not self.game:
            self.show_error("Ошибка: игра не инициализирована")
            return
            
        self.clear_screen()
        
        # Создаем экран статуса караванов
        caravans_screen = CaravansStatusScreen(
            parent=self.root,
            game=self.game,
            on_back=self.show_main_menu
        )
        caravans_screen.pack(fill="both", expand=True)
        self.current_frame = caravans_screen
    
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
        
        # Проверяем достижение цели победы или истечения времени, используя метод is_game_over из Game
        if self.game.is_game_over():
            print(f"DEBUG: Игра завершена! Проверка условия: баланс {self.game.player.balance} >= цель {self.game.victory_goal}? {self.game.player.balance >= self.game.victory_goal}")
            print(f"DEBUG: Или проверка цикла: текущий {self.game.current_cycle} > максимум {self.game.max_cycles}? {self.game.current_cycle > self.game.max_cycles}")
            self.show_game_over()
            return
        
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
        
        # Создаем основной фрейм
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color=RomanTheme.BACKGROUND,
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True)
        self.current_frame = main_frame
        
        # Определяем параметры в зависимости от исхода
        if self.game.has_won():
            # ПОБЕДА
            title = "🏆 ПОБЕДА 🏆"
            subtitle = "GLORIA ROMAE"
            message = f"Поздравляем, достойный гражданин Рима!\n\nВы накопили {self.game.player.balance:,} денариев и смогли выплатить\nдолг влиятельному патрицию!\n\nТеперь вы владеете прекрасной виллой на побережье и\nможете наслаждаться жизнью уважаемого торговца.\n\nSenatus Populusque Romanus приветствует вас!"
            color = "#6b8e23"  # Зелёный (успех)
            icon = "🏆"
        else:
            # ПОРАЖЕНИЕ
            title = "💀 ИГРА ОКОНЧЕНА 💀"
            subtitle = "INFAMIA ET SERVITUDO"
            message = f"Время истекло!\n\nВы не смогли заработать {self.game.victory_goal:,} денариев\nвлиятельному патрицию.\n\nВаш итоговый баланс: {self.game.player.balance:,} денариев\n\nВы стали рабом и будете отрабатывать долг годами.\nФортуна отвернулась от вас..."
            color = "#cd5c5c"  # Красноватый (опасность)
            icon = "💀"
        
        # Создаем верхний заголовок
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color=RomanTheme.BACKGROUND,
            height=100
        )
        header_frame.pack(fill="x", padx=50, pady=(30, 0))
        
        # Заголовок (крупный)
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=("Georgia", 52, "bold"),
            text_color=color
        )
        title_label.pack(pady=(10, 5))
        
        # Подзаголовок на латыни
        latin_label = ctk.CTkLabel(
            header_frame,
            text=subtitle,
            font=("Georgia", 32, "italic"),
            text_color=RomanTheme.ACCENT
        )
        latin_label.pack(pady=(0, 10))
        
        # Горизонтальная линия под заголовком
        separator = ctk.CTkFrame(
            main_frame,
            height=3,
            fg_color=color,
            corner_radius=0
        )
        separator.pack(fill="x", padx=150, pady=(5, 20))
        
        # Создаем центральный блок для сообщения
        message_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#f8f5f0",  # Светлый фон для контраста
            corner_radius=15,
            border_width=2,
            border_color=color
        )
        message_frame.pack(fill="both", expand=True, padx=150, pady=20)
        
        # Сообщение
        message_text = ctk.CTkTextbox(
            message_frame,
            fg_color="#f8f5f0",
            text_color="#2d2722",
            font=("Georgia", 24),
            activate_scrollbars=False,
            wrap="word",
            height=300
        )
        message_text.pack(fill="both", expand=True, padx=50, pady=40)
        message_text.insert("1.0", message)
        message_text.configure(state="disabled")  # Делаем только для чтения
        
        # Статистика
        stats_frame = ctk.CTkFrame(
            main_frame,
            fg_color=RomanTheme.BACKGROUND,
            height=40
        )
        stats_frame.pack(fill="x", padx=150, pady=(0, 20))
        
        stats_label = ctk.CTkLabel(
            stats_frame,
            text=f"{icon} Циклов прошло: {self.game.current_cycle} из {self.game.max_cycles} {icon}",
            font=("Georgia", 20, "bold"),
            text_color=color
        )
        stats_label.pack(pady=10)
        
        # Кнопки
        button_frame = ctk.CTkFrame(
            main_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        button_frame.pack(pady=30)
        
        # Кнопка "Новая игра"
        new_game_button = ctk.CTkButton(
            button_frame,
            text="🎮 Новая игра",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            text_color=RomanTheme.BACKGROUND,
            corner_radius=8,
            width=220,
            height=60,
            command=self.show_difficulty_selection
        )
        new_game_button.pack(side="left", padx=15)
        
        # Кнопка "Главное меню"
        menu_button = ctk.CTkButton(
            button_frame,
            text="🏛️ Главное меню",
            font=RomanTheme.FONT_BUTTON,
            fg_color=RomanTheme.NEUTRAL,
            hover_color="#999999",
            text_color=RomanTheme.TEXT,
            corner_radius=8,
            width=220,
            height=60,
            command=self.create_start_screen
        )
        menu_button.pack(side="left", padx=15)
    
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
        # Останавливаем музыку при выходе
        audio_manager.stop_music()
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
    
    def create_audio_controls(self, parent):
        """Создание панели управления аудио"""
        audio_frame = ctk.CTkFrame(
            parent,
            fg_color=RomanTheme.BACKGROUND,
            border_color=RomanTheme.FRAME_BORDER,
            border_width=1,
            corner_radius=8,
            height=60
        )
        audio_frame.pack(side="bottom", fill="x", padx=10, pady=5)
        audio_frame.pack_propagate(False)
        
        # Левая часть - кнопки управления
        controls_frame = ctk.CTkFrame(
            audio_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        controls_frame.pack(side="left", padx=10, pady=5)
          # Кнопка воспроизведения/паузы
        self.play_button = ctk.CTkButton(
            controls_frame,
            text="🎵" if not audio_manager.is_playing else "⏸️",
            font=("Arial", 16),
            width=40,
            height=30,
            fg_color=RomanTheme.BUTTON,
            hover_color=RomanTheme.BUTTON_HOVER,
            command=self.toggle_music
        )
        self.play_button.pack(side="left", padx=2)
        
        # Центральная часть - информация о треке
        info_frame = ctk.CTkFrame(
            audio_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        info_frame.pack(side="left", expand=True, fill="x", padx=10, pady=5)
        
        self.track_label = ctk.CTkLabel(
            info_frame,
            text=self.get_track_info(),
            font=("Arial", 12),
            text_color=RomanTheme.TEXT
        )
        self.track_label.pack(expand=True)
        
        # Правая часть - регулятор громкости
        volume_frame = ctk.CTkFrame(
            audio_frame,
            fg_color=RomanTheme.BACKGROUND
        )
        volume_frame.pack(side="right", padx=10, pady=5)
        
        volume_label = ctk.CTkLabel(
            volume_frame,
            text="🔊",
            font=("Arial", 14),
            text_color=RomanTheme.TEXT
        )
        volume_label.pack(side="left", padx=(0, 5))
        
        self.volume_slider = ctk.CTkSlider(
            volume_frame,
            from_=0,
            to=1,
            number_of_steps=20,
            width=100,
            height=20,
            progress_color=RomanTheme.ACCENT,
            button_color=RomanTheme.BUTTON,
            button_hover_color=RomanTheme.BUTTON_HOVER,
            command=self.change_volume
        )
        self.volume_slider.set(audio_manager.get_volume())
        self.volume_slider.pack(side="left", padx=5)
        
        # Обновляем информацию о треке каждые несколько секунд
        self.update_audio_info()
    
    def toggle_music(self):
        """Переключение воспроизведения музыки"""
        if audio_manager.is_playing:
            audio_manager.stop_music()
            self.play_button.configure(text="🎵")
        else:
            audio_manager.start_music()
            self.play_button.configure(text="⏸️")
  
    
    def change_volume(self, value):
        """Изменение громкости"""
        audio_manager.set_volume(value)
    
    def get_track_info(self):
        """Получение информации о текущем треке"""
        if not audio_manager.is_enabled:
            return "🎵 Аудио отключено (pygame не установлен)"
        
        info = audio_manager.get_playlist_info()
        if info["total_tracks"] == 0:
            return "🎵 Музыкальные файлы не найдены в папке data/music"
        
        current_track = info["current_track"] or "Нет трека"
        status = "Играет" if info["is_playing"] else "Остановлено"
        return f"🎵 {status}: {current_track} ({info['current_index']}/{info['total_tracks']})"
    def update_audio_info(self):
        """Обновление информации о треке"""
        try:
            if hasattr(self, 'track_label') and self.track_label.winfo_exists():
                self.track_label.configure(text=self.get_track_info())
            
            # Планируем следующее обновление через 3 секунды только если окно еще существует
            if self.root and self.root.winfo_exists():
                self.root.after(3000, self.update_audio_info)
        except Exception as e:
            # Игнорируем ошибки обновления UI если виджеты уже уничтожены
            pass
  
