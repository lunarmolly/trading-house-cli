import pygame
import os


class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None

    def play_loop(self, filename: str, volume: float = 0.3):
        """Проигрывает трек в цикле"""
        try:
            full_path = os.path.join(os.getcwd(), filename)
            if not os.path.exists(full_path):
                print(f"Файл не найден: {full_path}")
                return

            pygame.mixer.music.load(full_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)  # -1 = бесконечное воспроизведение
            self.current_track = filename
        except Exception as e:
            print(f"Ошибка воспроизведения: {e}")

    def stop_music(self):
        """Останавливает текущую музыку"""
        pygame.mixer.music.stop()

    def pause_music(self):
        """Ставит музыку на паузу"""
        pygame.mixer.music.pause()

    def resume_music(self):
        """Продолжает воспроизведение после паузы"""
        pygame.mixer.music.unpause()

    def play_background_music(self, context: str):
        """Воспроизводит соответствующую музыку в зависимости от контекста"""
        music_map = {
            "main_menu": "data/music/Древнеримская_музыка.mp3",
            "second_music": "data/music/roman_music.mp3"
        }
        if context in music_map:
            self.play_loop(music_map[context])