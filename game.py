# Игра завершена 26.06.2020.
from script_dir import script_dir  # Ошибка, если не указывать абсолютный путь
# В коде давольно мало комметариев(как минимуи меньше чем в прошлом проекте)
# Что делает модуль/класс/метод понятно из названия. Сложные моменты объяснены.
print(script_dir)
try:
    import pygame

    pygame.init()

    import menu
    import HOMA
    import levels
    import settings
    from time import sleep, time


    class Game:
        '''Связующий класс. Вызывает основные методы меню, уровня. Отрисоавывает экран.'''

        def __init__(self):
            st = settings.Settings()  # Самые основные настройки
            self.window = pygame.display.set_mode((st.window_width, st.window_height))
            pygame.display.set_caption('Хома!')
            self.menu = menu.Menu()  # Меню, все кнопки(включая кнопку выхода в уровне)
            self.bg = st.bg
            self.level_now = None
            self.level_go = False
            self.music_on = True

        def load_menu_music(self):
            if self.music_on:
                pygame.mixer.music.load(script_dir + 'music\in_menu_music.mp3')
                pygame.mixer.music.play(-1)

        def load_level_music(self):
            if self.music_on:
                pygame.mixer.music.load(script_dir + 'music\in_level_music.mp3')
                pygame.mixer.music.play(-1)

        def load_boss_music(self):
            if self.music_on:
                pygame.mixer.music.load(script_dir + 'music\Terraria_Music.mp3')
                pygame.mixer.music.play(-1)

        def in_menu(self):
            '''Вся работа класса с меню. Отрисовывает меню,
             получает нажатые кнопки, некоторые кнопки обратавыет.'''
            self.menu.draw(self.window)
            # Проверка результата нажатий на кнопки меню
            result = self.menu.run(*self.mouse_pos, pygame.mouse.get_pressed()[0])
            if result:
                if result[0] == 'loadl':  # Загружает уровень
                    self.level_go = True
                    with open(script_dir + 'settings.txt') as file:
                        self.key_list = [int(i) for i in file.read().split('\n')]  # список горячих клавишь
                        self.complexity = self.key_list.pop(7)  # Сложность
                    if int(result[1]) == 10:
                        self.load_boss_music()
                    else:
                        self.load_level_music()
                    self.level_now = levels.Level(result[-1], self.complexity)
                    self.window = pygame.display.set_mode(self.level_now.level_size)
                elif result[0] == 'main_menu':
                    # закрытие уровня, длл кнопки на уровне (если переход не с уровня, ничего не произайдет)
                    self.close_level()
                    self.load_menu_music()
                elif result[0] == 'music':
                    self.music_on = not self.music_on  # Для кнопки выключения музыки в настройках
                    if self.music_on:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()

        def check_keys(self, event):
            '''Проверяет, совпадение кода нажатых клавиш, с кодом из списка горячих клавиш'''
            if event.key == self.key_list[0]:
                return 'j'
            if event.key == self.key_list[2]:
                return 'r'
            if event.key == self.key_list[1]:
                return 'l'
            if event.key == self.key_list[6]:
                return 't'
            if event.key == self.key_list[5]:
                return 'h'
            if event.key == self.key_list[4]:
                return 'm'

        def in_level(self, keys):
            '''Вся работа с уровнем.'''
            self.level_now.draw(self.window)
            self.level_now.others_persons()  # Обработка персонажей
            if self.level_now.control_main_hero(keys):  # Управление гланым героем
                self.close_level()

        def run_game(self):
            '''Метод реализует основной цикл игры.'''
            self.load_menu_music()

            self.keys = []  # Список нажатых клавиш
            clock = pygame.time.Clock()
            while True:
                self.window.blit(self.bg, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        try:
                            self.level_now.close_level()
                        except AttributeError:
                            pass
                        finally:
                            quit('выход крестиком')
                    # Идея такая. Если кнопка нажата, она добовляестя в список нажатых кнопок,
                    # если отпущена удаляется из него. Были проблемы с обработкой длительного зажатия клавиш
                    if self.level_go:
                        if event.type == pygame.KEYDOWN:
                            self.keys.append(self.check_keys(event))
                        if event.type == pygame.KEYUP:
                            self.keys.remove(self.check_keys(event))

                self.mouse_pos = pygame.mouse.get_pos()  # Позиция мыши
                if self.level_go:
                    self.in_level(self.keys)
                self.in_menu()

                pygame.display.update()
                clock.tick(23)
                # С каждым кадром все процессы игры(проверка соприкоснавений, перемещения) прогоняются.
                # По моим замерам более 80% времени идет на прорисовку

        def close_level(self):
            try:  # чтобы работала в меню кнопка выхода в главное меню
                self.level_now.close_level()
                self.level_go = False
                del self.level_now
                pygame.display.set_mode((800, 600))
                self.menu.__init__()  # Обновление меню
                self.menu.change_section_now('levels')  # переход в список уровней
                self.load_menu_music()
                self.keys.clear()  # Очитска списка нажатых клавиш
            except:
                pass


    import Check_txt_files  # Проверяет файл настроек и информации о главном герое.

    # Если что-то не так, перезаписывает файл, приводя к начальным параметрам
    game = Game()  # сама игра
    game.run_game()
except pygame.error as e:  # При ошибке выводит сообщение
    print(e)
    import Check_other_files
except Exception as e:
    import logging
    import tkinter as tk  # использую ткинтер, т.к. нужно показать только окошко с надписью

    window = tk.Tk('400x250')
    window.title('Непредвиденная ошибка.')
    lbl = tk.Label(window,
                   text='Произошла непредвиденная ошибка.'
                        ' Обратитесь к разработчику игры.\n Сообщение об ошибке записано в файл log.txt')
    lbl.grid(column=0, row=0)
    lbl2 = tk.Label(window, text=e)
    lbl2.grid(column=0, row=1)
    window.mainloop()
    logging.basicConfig(filename="log.txt", level=logging.INFO)
    logging.error(str(e))
    input()
