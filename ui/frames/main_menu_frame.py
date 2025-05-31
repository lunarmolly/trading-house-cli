from tkinter import ttk

# Фрейм главного меню
class MainMenuFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        top_frame = ttk.Frame(self)
        top_frame.pack(pady=10, fill="x")

        status_label = ttk.Label(top_frame, textvariable=controller.status_text, font=("Arial", 14))
        status_label.pack(side="left", padx=10)

        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20)

        buttons = [
            ("Посмотреть города", lambda: controller.show_frame("CitiesFrame")),
            ("Посмотреть активные караваны", lambda: controller.show_frame("CaravansFrame")),
            ("Отправить новый караван", lambda: controller.show_frame("SendCaravanFrame")),
            ("Купить товары", lambda: controller.show_frame("BuyGoodsFrame")),
            ("Посмотреть склад", lambda: controller.show_frame("InventoryFrame")),
            ("Перейти к следующему циклу", lambda: controller.next_cycle()),
            ("Выход", controller.exit_game),
        ]

        for text, command in buttons:
            ttk.Button(main_frame, text=text, command=command).pack(pady=5, fill="x")
