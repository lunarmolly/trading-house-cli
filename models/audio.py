"""
Система управления фоновой музыкой в игре
"""

import os
import random
import threading
import time
from typing import List, Optional

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    pygame = None
    PYGAME_AVAILABLE = False
    print("Предупреждение: pygame не установлен. Музыка будет отключена.")
    print("Для включения музыки установите: pip install pygame")


class AudioManager:
    """Менеджер для управления фоновой музыкой"""
    
    def __init__(self, music_folder: str = "data/music", volume: float = 0.5):
        self.music_folder = music_folder
        self.volume = volume
        self.playlist: List[str] = []
        self.current_track_index = 0
        self.is_playing = False
        self.is_enabled = PYGAME_AVAILABLE
        self.shuffle_mode = True  # Всегда включено
        self._music_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        if self.is_enabled:
            try:
                # Инициализация с более безопасными параметрами
                pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
                pygame.mixer.init()
                pygame.mixer.music.set_volume(self.volume)
                self._load_playlist()
                print("🎵 Аудио система инициализирована успешно")
            except Exception as e:
                print(f"Предупреждение: Не удалось инициализировать аудио: {e}")
                print("🎵 Музыка будет отключена")
                self.is_enabled = False
    
    def _load_playlist(self) -> None:
        """Загрузка списка музыкальных файлов"""
        if not os.path.exists(self.music_folder):
            print(f"Папка с музыкой не найдена: {self.music_folder}")
            return
        
        # Поддерживаемые форматы
        supported_formats = ('.mp3', '.ogg', '.wav', '.m4a')
        
        self.playlist = []
        for file in os.listdir(self.music_folder):
            if file.lower().endswith(supported_formats):
                self.playlist.append(os.path.join(self.music_folder, file))
        
        if self.playlist:
            print(f"Найдено {len(self.playlist)} музыкальных файлов")
            if self.shuffle_mode:
                self._shuffle_playlist()
        else:
            print("Музыкальные файлы не найдены в папке music")
    
    def _shuffle_playlist(self) -> None:
        """Перемешивание плейлиста"""
        if self.playlist:
            random.shuffle(self.playlist)
            self.current_track_index = 0
    
    def start_music(self) -> None:
        """Запуск фоновой музыки"""
        if not self.is_enabled or not self.playlist:
            return
        
        if self.is_playing:
            return
        
        self.is_playing = True
        self._stop_event.clear()
        self._music_thread = threading.Thread(target=self._music_loop, daemon=True)
        self._music_thread.start()
        print("🎵 Фоновая музыка запущена")
    def stop_music(self) -> None:
        """Остановка фоновой музыки"""
        if not self.is_enabled:
            return
        
        self.is_playing = False
        self._stop_event.set()
        
        try:
            if pygame and PYGAME_AVAILABLE:
                pygame.mixer.music.stop()
        except Exception as e:
            print(f"Ошибка при остановке музыки: {e}")
        
        if self._music_thread and self._music_thread.is_alive():
            self._music_thread.join(timeout=1.0)
        
        print("🎵 Фоновая музыка остановлена")
    def _music_loop(self) -> None:
        """Основной цикл воспроизведения музыки"""
        while self.is_playing and not self._stop_event.is_set():
            try:
                if self.playlist and self.is_enabled:
                    current_track = self.playlist[self.current_track_index]
                    print(f"🎵 Играет: {os.path.basename(current_track)}")
                    
                    if PYGAME_AVAILABLE:
                        pygame.mixer.music.load(current_track)
                        pygame.mixer.music.play()
                        
                        # Ждем окончания трека
                        while (pygame.mixer.music.get_busy() and 
                               self.is_playing and 
                               not self._stop_event.is_set()):
                            time.sleep(0.5)
                    
                    # Переход к следующему треку
                    self._next_track()
                else:
                    time.sleep(1)
                    
            except Exception as e:
                print(f"Ошибка воспроизведения музыки: {e}")
                # При ошибке ждем перед попыткой следующего трека
                time.sleep(2)
                self._next_track()
    
    def _next_track(self) -> None:
        """Переход к следующему треку"""
        if not self.playlist:
            return
        
        self.current_track_index += 1
        
        # Если достигли конца плейлиста, начинаем сначала
        if self.current_track_index >= len(self.playlist):
            self.current_track_index = 0
            if self.shuffle_mode:
                self._shuffle_playlist()
                print("🔀 Плейлист перемешан")
    def set_volume(self, volume: float) -> None:
        """Установка громкости (0.0 - 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        if self.is_enabled and pygame and PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.set_volume(self.volume)
            except Exception as e:
                print(f"Ошибка установки громкости: {e}")
    
    def get_volume(self) -> float:
        """Получение текущей громкости"""
        return self.volume
  
    
    def get_current_track(self) -> Optional[str]:
        """Получение имени текущего трека"""
        if self.playlist and 0 <= self.current_track_index < len(self.playlist):
            return os.path.basename(self.playlist[self.current_track_index])
        return None
    
    def get_playlist_info(self) -> dict:
        """Информация о плейлисте"""
        return {
            "total_tracks": len(self.playlist),
            "current_index": self.current_track_index + 1 if self.playlist else 0,
            "current_track": self.get_current_track(),
            "shuffle_mode": self.shuffle_mode,
            "is_playing": self.is_playing,
            "volume": self.volume,
            "enabled": self.is_enabled
        }


# Глобальный экземпляр менеджера аудио
audio_manager = AudioManager()
