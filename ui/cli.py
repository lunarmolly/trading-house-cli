def select_difficulty() -> str:
    """CLI выбор уровня сложности"""
    print("\n=== Выбор уровня сложности ===")
    print("1. Легкий (меньше рисков, больше ресурсов)")
    print("2. Средний (стандартный баланс)")
    print("3. Сложный (высокие риски, меньше ресурсов)")

    while True:
        choice = input("Выберите уровень (1-3): ").strip()
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "normal"
        elif choice == "3":
            return "hard"
        else:
            print("Неверный выбор. Попробуйте снова.")


def show_main_menu(game) -> None:
    """
    Главное меню игрока. Работает в цикле до завершения игры.
    """
    while not game.is_game_over():
        print("\n=== Торговый Дом ===")
        print(f"Цикл: {game.current_cycle} / {game.max_cycles}")
        print(f"Баланс: {game.player.balance} денариев")
        print("1. Посмотреть города")
        print("2. Посмотреть активные караваны")
        print("3. Отправить новый караван")
        print("4. Купить товары")
        print("5. Посмотреть склад")
        print("6. Перейти к следующему циклу")
        print("7. Выйти")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_cities(game)
            input("\nНажмите Enter для возврата в меню...")
        elif choice == "2":
            show_caravans(game)
            input("\nНажмите Enter для возврата в меню...")
        elif choice == "3":
            send_caravan(game)
        elif choice == "4":
            buy_goods(game)
        elif choice == "5":
            show_inventory(game)
        elif choice == "6":
            game.next_cycle()
            game.update_caravans()
            show_active_caravans_status(game)
            input("\nНажмите Enter для возврата в меню...")
        elif choice == "7":
            print("Выход из игры.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

    # === Завершение игры ===
    if game.has_won():
        print("\n🏆 ПОБЕДА! 🏆")
        print(f"Вы накопили {game.player.balance} денариев за {game.current_cycle} циклов!")
        print("Вы стали владельцем роскошной виллы у моря.")
    else:
        print("\n💀 ИГРА ОКОНЧЕНА 💀")
        print(f"Ваш итоговый баланс: {game.player.balance} денариев.")
        print("К сожалению, цель не достигнута.")


def show_cities(game) -> None:
    print("\n--- Города ---")
    for city in game.cities:
        if city.duration == 0:
            print(f"{city.name}: мгновенная доставка (Рим)")
        else:
            # Показываем общее время экспедиции
            print(f"{city.name}: длительность экспедиции {city.duration} дней (туда-обратно)")


def show_caravans(game) -> None:
    print("\n--- Активные караваны ---")
    if not game.active_caravans:
        print("Нет активных караванов.")
        return
    for i, caravan in enumerate(game.active_caravans, 1):
        status = f"{caravan.destination.name}"
        if caravan.destination.duration == 0:
            status += " (Рим) - возврат в этом цикле"
        else:
            status += f" | Прибытие: цикл {caravan.arrival_cycle}, Возврат: {caravan.return_cycle}"
        print(f"{i}. {status}")


def show_inventory(game) -> None:
    print("\n--- Склад ---")
    if not game.player.inventory:
        print("Склад пуст.")
        input("\nНажмите Enter для возврата в меню...")
        return
    for name, qty in game.player.inventory.items():
        print(f"{name}: {qty} ед.")
    input("\nНажмите Enter для возврата в меню...")


def buy_goods(game) -> None:
    print("\n--- Покупка товаров ---")
    print(f"Ваш баланс: {game.player.balance} денариев")

    goods_list = game.goods
    goods_dict = {i + 1: g for i, g in enumerate(goods_list)}

    for idx, good in goods_dict.items():
        print(f"{idx}. {good.name} ({good.category}) — {good.base_price} денариев за ед.")

    choice = input("Выберите товар (номер) или 0 для выхода: ").strip()
    if not choice.isdigit() or int(choice) not in goods_dict and int(choice) != 0:
        print("Неверный ввод.")
        input("\nНажмите Enter для возврата...")
        return buy_goods(game)
    if int(choice) == 0:
        print("Отмена покупки.")
        input("\nНажмите Enter для возврата в меню...")
        return

    selected_good = goods_dict[int(choice)]

    qty_input = input(f"Введите количество для покупки '{selected_good.name}': ").strip()
    if not qty_input.isdigit() or int(qty_input) <= 0:
        print("Неверное количество.")
        input("\nНажмите Enter для возврата...")
        return buy_goods(game)

    quantity = int(qty_input)
    total_price = selected_good.base_price * quantity

    if total_price > game.player.balance:
        print(f"Недостаточно средств. Требуется {total_price}, доступно {game.player.balance}.")
        input("\nНажмите Enter для возврата...")
        return buy_goods(game)

    confirm = input(
        f"Подтвердить покупку {quantity} ед. '{selected_good.name}' за {total_price} денариев? (ДА/нет): ").strip().lower()
    if confirm not in ["", "да"]:
        print("Покупка отменена.")
        input("\nНажмите Enter для возврата в меню...")
        return

    game.player.add_goods(selected_good, quantity)
    game.player.adjust_balance(-total_price)
    print(f"Вы купили {quantity} ед. '{selected_good.name}' за {total_price} денариев.")
    input("\nНажмите Enter для возврата в меню...")


def send_caravan(game) -> None:
    print("\n--- Отправка каравана ---")
    if not game.player.inventory:
        print("На складе нет товаров для отправки.")
        input("\nНажмите Enter для возврата в меню...")
        return

    # Вывод списка городов
    for i, city in enumerate(game.cities, 1):
        if city.duration == 0:
            print(f"{i}. {city.name} (мгновенная доставка)")
        else:
            print(f"{i}. {city.name} (экспедиция: {city.duration} дней)")

    city_index = input("Выберите город (номер): ").strip()
    if not city_index.isdigit() or not (1 <= int(city_index) <= len(game.cities)):
        print("Неверный выбор.")
        input("\nНажмите Enter для возврата...")
        return send_caravan(game)
    city = game.cities[int(city_index) - 1]

    # Проверка доступности курьеров и повозок
    couriers = game.player.couriers
    if not couriers:
        print("Нет доступных курьеров.")
        input("\nНажмите Enter для возврата в меню...")
        return
    courier = couriers[0]

    wagons = game.player.wagons
    if not wagons:
        print("Нет доступных повозок.")
        input("\nНажмите Enter для возврата в меню...")
        return
    wagon = wagons[0]

    # Подготовка данных о товарах
    goods_dict = {g.name: g for g in game.goods}
    available_goods = [(name, qty) for name, qty in game.player.inventory.items() if qty > 0]

    if not available_goods:
        print("Нет доступных товаров.")
        input("\nНажмите Enter для возврата в меню...")
        return

    # Вывод товаров с расчетом цен
    print("\n--- Товары на складе ---")
    for idx, (name, qty) in enumerate(available_goods, 1):
        good_obj = goods_dict[name]

        # Расчет цены с учетом особенностей Рима
        if city.duration == 0:  # Рим
            expected_price = int(good_obj.base_price * 0.9)
            print(f"{idx}. {name} — {qty} ед. — фиксированная цена: {expected_price} (90% от базовой)")
        else:
            city_mod = city.demand_modifiers.get(name, 1.0) - 1.0
            event = city.current_event or "Нет события"
            event_mod = game.config["event_modifiers"].get(event, {}).get(name, 1.0) - 1.0
            total_percent = city_mod + event_mod
            final_modifier = 1.0 + total_percent
            expected_price = int(good_obj.base_price * final_modifier)
            print(f"{idx}. {name} — {qty} ед. — ожидаемая цена: {expected_price}")

    # Выбор товаров
    selection = {}
    used_capacity = 0
    goods_index = {i + 1: name for i, (name, _) in enumerate(available_goods)}

    print("Введите номер товара и количество через пробел (пустая строка — завершить):")
    while True:
        entry = input("> ").strip()
        if not entry:
            break
        try:
            num, qty = entry.split()
            num = int(num)
            qty = int(qty)

            if num not in goods_index:
                print("Неверный номер товара.")
                continue

            name = goods_index[num]
            if qty <= 0:
                print("Количество должно быть положительным.")
                continue
            if qty > game.player.inventory[name]:
                print("Недостаточно на складе.")
                continue
            if used_capacity + qty > wagon.capacity:
                print("Недостаточно места в повозке.")
                continue

            selection[name] = selection.get(name, 0) + qty
            used_capacity += qty
        except ValueError:
            print("Ошибка ввода. Пример: 1 50")

    if not selection:
        print("Вы не выбрали товары.")
        input("\nНажмите Enter для возврата в меню...")
        return

    # Подтверждение и отправка
    for name, qty in selection.items():
        good_obj = goods_dict[name]
        game.player.remove_goods(good_obj, qty)

    caravan = game.form_caravan(
        courier=courier,
        wagon=wagon,
        goods_selection=selection,
        city=city
    )

    if city.duration == 0:
        print(f"Караван отправлен в Рим (вернется в этом цикле)")
    else:
        print(f"Караван отправлен в {city.name} (вернется через {city.duration} циклов)")
    input("\nНажмите Enter для возврата в меню...")


def show_active_caravans_status(game) -> None:
    """
    Показывает статус всех активных караванов после перехода цикла.
    """
    print("\n--- Статус караванов ---")
    if not game.active_caravans:
        print("Нет активных караванов.")
        input("\nНажмите Enter для возврата в меню...")
        return

    for i, caravan in enumerate(game.active_caravans, 1):
        if caravan.destination.duration == 0:  # Рим - мгновенная доставка
            status = f"{caravan.destination.name} (Рим) - возвращен"
        else:
            if game.current_cycle < caravan.arrival_cycle:
                days_left = caravan.arrival_cycle - game.current_cycle
                status = f"{caravan.destination.name} | Прибытие через {days_left} циклов"
            elif game.current_cycle == caravan.arrival_cycle:
                status = f"{caravan.destination.name} | Продажа товаров"
            else:
                days_left = caravan.return_cycle - game.current_cycle
                status = f"{caravan.destination.name} | Возврат через {days_left} циклов"
                # Убрана проверка задержки как избыточная
                if days_left < 0:
                    status += " (Задержка!)"

        if caravan.event_occurred == "Смерть курьера":
            status += " — КУРЬЕР ПОГИБ"
        print(f"{i}. {status}")