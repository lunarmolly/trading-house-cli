trading_house_cli/
├── main.py                      # Точка входа
│
├── ui/
│   ├── __init__.py               # Делает ui пакетом
│   └── cli.py                    # CLI-интерфейс
│
├── core/
│   ├── __init__.py               # Делает core пакетом
│   ├── game.py                   # Игровой процесс
│   ├── world.py                  # Генерация мира
│   ├── goods.py                  # Работа с товарами
│   ├── caravan.py                # Механика караванов
│   ├── events.py                 # События в пути
│   ├── economy.py                # Рынок и цены
│   └── finance.py                # Финансовый учет
│
├── models/
│   ├── __init__.py               # Делает models пакетом
│   ├── city.py                   # Модель города
│   ├── goods_item.py             # Модель товара
│   ├── courier.py                # Модель курьера
│   ├── wagon.py                  # Модель повозки
│   ├── player.py                 # Модель игрока
│   └── caravan.py                # Модель торговой миссии
│
├── data/
│   └── goods_config.json         # Конфигурация товаров
│
├── requirements.txt              # Зависимости
└── README.md                     # Документация
