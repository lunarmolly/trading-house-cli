import tkinter as tk
from tkinter import ttk
from ui.frames.main_menu_frame import MainMenuFrame
from ui.frames.cities_frame import CitiesFrame


class TradeHouseGUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Торговый Дом")
        self.geometry("800x600")
        self.resizable(False, False)

        self.game = game

        # Создаём переменные после инициализации Tk()
        self.status_text = tk.StringVar()
        self.update_status_bar()

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Регистрация фреймов
        self.add_frame("MainMenuFrame", MainMenuFrame(container, self))
        self.add_frame("CitiesFrame", CitiesFrame(container, self))

        self.show_frame("MainMenuFrame")

    def add_frame(self, name, frame):
        self.frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Показывает нужный фрейм"""
        frame = self.frames[page_name]
        frame.tkraise()

    def update_status_bar(self):
        """Обновляет информацию в нижней панели"""
        self.status_text.set(f"Цикл: {self.game.current_cycle} / {self.game.max_cycles}, Баланс: {self.game.player.balance}")

    def exit_game(self):
        self.destroy()