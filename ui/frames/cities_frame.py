from tkinter import ttk, END
import tkinter as tk

class CitiesFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Заголовок
        title_label = ttk.Label(self, text="Города", font=("Arial", 16))
        title_label.pack(pady=10)

        # Статусбар вверху
        top_frame = ttk.Frame(self)
        top_frame.pack(pady=5, fill="x")

        status_label = ttk.Label(top_frame, textvariable=controller.status_text, font=("Arial", 12))
        status_label.pack(side="left", padx=10)

        # Контейнер для списка городов
        listbox_frame = ttk.Frame(self)
        listbox_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Список городов
        self.city_listbox = tk.Listbox(listbox_frame, height=15, width=80)
        self.city_listbox.pack(side="left", fill="both", expand=True)

        # Скроллбар
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.city_listbox.yview)
        scrollbar.pack(side="right", fill="y")

        self.city_listbox.config(yscrollcommand=scrollbar.set)

        back_button = ttk.Button(self, text="Назад", command=lambda: controller.show_frame("MainMenuFrame"))
        back_button.pack(pady=10)

        self.refresh()
# Обновление списка городов
    def refresh(self):
        """Обновляет список городов"""
        self.city_listbox.delete(0, END)
        for city in self.controller.game.cities:
            event = city.current_event or "нет события"
            line = f"{city.name} | {city.distance} дней | Событие: {event}"
            self.city_listbox.insert(END, line)