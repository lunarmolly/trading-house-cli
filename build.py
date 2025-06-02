#!/usr/bin/env python3
"""
Скрипт для создания исполняемого файла игры "Торговый Дом"
через PyInstaller

Использование:
    python build.py          # Создание обычного билда
    python build.py --onefile # Создание одного exe файла
    python build.py --debug   # Создание билда с debug информацией
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path


def check_pyinstaller():
    """Проверка наличия PyInstaller"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller найден (версия {PyInstaller.__version__})")
        return True
    except ImportError:
        print("❌ PyInstaller не найден!")
        print("Установите его командой: pip install pyinstaller")
        return False


def clean_build_dirs():
    """Очистка предыдущих билдов"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Очищаем {dir_name}/")
            shutil.rmtree(dir_name)
    
    # Удаляем .spec файлы
    for spec_file in Path('.').glob('*.spec'):
        print(f"🧹 Удаляем {spec_file}")
        spec_file.unlink()


def get_pyinstaller_args(onefile=False, debug=False):
    """Подготовка аргументов для PyInstaller"""
    # Определяем разделитель для --add-data в зависимости от ОС
    separator = ';' if os.name == 'nt' else ':'
    
    args = [
        'pyinstaller',
        '--name=TradingHouse',
        f'--add-data=data{separator}data',  # Включаем папку data с музыкой
        f'--add-data=ui{separator}ui',      # Включаем папку ui (для GUI)
        '--hidden-import=customtkinter',
        '--hidden-import=tkinter',
        '--hidden-import=pygame',           # Добавляем pygame для музыки
        '--clean',
        '--noconfirm'
    ]
    
    # Проверяем иконку и добавляем её только если она валидна
    icon_path = 'data/icon.ico'
    if os.path.exists(icon_path):
        # Проверяем размер файла - минимальный размер ICO файла ~1KB
        if os.path.getsize(icon_path) > 1000:
            args.insert(2, f'--icon={icon_path}')
            print("🎨 Используем пользовательскую иконку")
        else:
            print("⚠️ Иконка слишком мала, пропускаем")
    else:
        print("⚠️ Иконка не найдена, создаем билд без иконки")
    
    if onefile:
        args.append('--onefile')
        print("📦 Создание одного исполняемого файла")
    else:
        args.append('--onedir')
        print("📁 Создание директории с исполняемым файлом")
    
    if debug:
        args.extend(['--debug=all', '--console'])
        print("🐛 Включен debug режим")
    else:
        args.append('--windowed')  # Без консоли для GUI
        print("🖼️ Создание GUI приложения без консоли")
    
    # Главный файл
    args.append('main.py')
    
    return args


def create_build_info():
    """Создание файла с информацией о билде"""
    try:
        # Получаем версию из git (если доступен)
        try:
            version = subprocess.check_output(
                ['git', 'describe', '--tags', '--always'], 
                stderr=subprocess.DEVNULL,
                text=True
            ).strip()
        except:
            version = "unknown"
        
        build_info = f"""# Торговый Дом - Build Info
Версия: {version}
Дата билда: {os.popen('date /t').read().strip() if os.name == 'nt' else os.popen('date').read().strip()}
Python: {sys.version}
Платформа: {sys.platform}

## Запуск
- Для GUI версии: TradingHouse.exe
- Для CLI версии: TradingHouse.exe cli

## Файлы данных
Убедитесь, что рядом с исполняемым файлом находится папка 'data' с конфигурационными файлами.
"""
        
        with open('dist/BUILD_INFO.txt', 'w', encoding='utf-8') as f:
            f.write(build_info)
        
        print("📝 Создан файл BUILD_INFO.txt")
    except Exception as e:
        print(f"⚠️ Не удалось создать BUILD_INFO.txt: {e}")


def copy_additional_files():
    """Копирование дополнительных файлов в билд"""
    files_to_copy = [
        ('README.md', 'dist/README.md'),
        ('requirements.txt', 'dist/requirements.txt')
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            try:
                shutil.copy2(src, dst)
                print(f"📋 Скопирован {src} -> {dst}")
            except Exception as e:
                print(f"⚠️ Не удалось скопировать {src}: {e}")


def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description='Создание билда игры "Торговый Дом"')
    parser.add_argument('--onefile', action='store_true', help='Создать один exe файл')
    parser.add_argument('--debug', action='store_true', help='Включить debug режим')
    parser.add_argument('--clean', action='store_true', help='Только очистить билды')
    
    args = parser.parse_args()
    
    print("🏛️ Торговый Дом - Сборка билда 🏛️")
    print("=" * 50)
    
    # Только очистка
    if args.clean:
        clean_build_dirs()
        print("✅ Очистка завершена!")
        return
    
    # Проверка PyInstaller
    if not check_pyinstaller():
        print("\n💡 Для установки PyInstaller выполните:")
        print("pip install pyinstaller")
        return
    
    # Очистка предыдущих билдов
    clean_build_dirs()
    
    # Проверка основных файлов
    if not os.path.exists('main.py'):
        print("❌ Файл main.py не найден!")
        return
    
    if not os.path.exists('data/balance_config.json'):
        print("❌ Файл data/balance_config.json не найден!")
        return
    
    print("✅ Основные файлы найдены")
    
    # Подготовка аргументов для PyInstaller
    pyinstaller_args = get_pyinstaller_args(args.onefile, args.debug)
    
    print(f"\n🔧 Команда PyInstaller:")
    print(' '.join(pyinstaller_args))
    
    # Создание билда
    print("\n🚀 Запуск PyInstaller...")
    try:
        result = subprocess.run(pyinstaller_args, check=True)
        print("✅ Билд успешно создан!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при создании билда: {e}")
        return
    except FileNotFoundError:
        print("❌ PyInstaller не найден в PATH!")
        return
    
    # Создание дополнительных файлов
    create_build_info()
    copy_additional_files()
    
    # Проверка результата
    exe_path = 'dist/TradingHouse.exe'
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n🎉 Билд готов!")
        print(f"📍 Путь: {os.path.abspath(exe_path)}")
        print(f"📏 Размер: {size_mb:.1f} MB")
        
        print(f"\n🚀 Для запуска:")
        print(f"   GUI версия: {exe_path}")
        print(f"   CLI версия: {exe_path} cli")
    else:
        print("\n❌ Исполняемый файл не найден!")
    
    print(f"\n📁 Содержимое папки dist:")
    if os.path.exists('dist'):
        for item in os.listdir('dist'):
            item_path = os.path.join('dist', item)
            if os.path.isdir(item_path):
                print(f"   📁 {item}/")
            else:
                size = os.path.getsize(item_path)
                print(f"   📄 {item} ({size} bytes)")


if __name__ == "__main__":
    main()
