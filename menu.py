import pygame.font
from levels import *
import time
from script_dir import script_dir

pygame.init()


# Здесь просто ужасный код. Все кнопки и их методы смешаны в кучу. Я не смог придумать как его структуризировать.

class OLdMenu:
    def __init__(self, window):
        self.levels_button_list = []
        self.what_on_menu = 'start'
        # Создание списка уровней
        self.window = window
        with open(script_dir + 'settings.txt') as file:
            dict_chars = {1073741906: 'Ве', 1073741905: 'Ни', 1073741903: 'Пр', 1073741904: 'Ле'}
            strings = file.read().split('\n')
            jump, left, right, down, magic, hill, tp, complexty = [dict_chars[int(i)] if int(i) in
                                                                                         dict_chars else chr(
                int(i)) if n < 7 else i for n, i in enumerate(strings)]
            complexty = int(strings[-1])

        # главное меню
        self.start_button = Buttons(x_cor=250, y_cor=60,  # переход к показу списка уровней
                                    image='images\Buttons\long_button.png',
                                    image_on='images\Buttons\long_button_on.png',
                                    text='Начать игру',
                                    command=self.start)
        # Во всех разделах меню кроме главного меню
        self.back_button = Buttons(x_cor=450, y_cor=520,  # переход главное меню
                                   image='images\Buttons\long_button.png',
                                   image_on='images\Buttons\long_button_on.png', text='В главное меню',
                                   command=self.go_main_menu)
        self.settings_button = Buttons(x_cor=250, y_cor=180,  # переход к настройкам
                                       image='images\Buttons\long_button.png',
                                       image_on='images\Buttons\long_button_on.png', text='Настройки'
                                       , command=self.show_settings)
        self.set_go_right_button = Buttons(x_cor=250, y_cor=180,  # переход к настройкам
                                           image='images\Buttons\long_button.png',
                                           image_on='images\Buttons\long_button_on.png', text='Настройки'
                                           , command=self.show_settings)
        self.information_button = Buttons(x_cor=250, y_cor=300,  # переход к меню информации (сведения об игре)
                                          image='images\Buttons\long_button.png',
                                          image_on='images\Buttons\long_button_on.png', text='Информация',
                                          command=self.show_information)
        self.exit_button = Buttons(x_cor=250, y_cor=420,  # выход из игры
                                   image='images\Buttons\long_button.png',
                                   image_on='images\Buttons\long_button_on.png', text='Выход',
                                   command=self.exit)
        # в меню настроек
        self.music_on = True
        self.music_button = Buttons(x_cor=680, y_cor=10,  # включение/выключение музыки
                                    image='images\Buttons\music_button.png',
                                    image_on='images\Buttons\music_button_on.png', text='',
                                    command=self.work_music)

        self.easy = Buttons(x_cor=50, y_cor=100,  # включение/выключение музыки
                            image='images\Buttons\easy_button.png',
                            image_on='images\Buttons\easy_button_on.png', text='Легкая',
                            command=self.set_easy)
        self.medium = Buttons(x_cor=50, y_cor=200,  # включение/выключение музыки
                              image='images\Buttons\medium_button.png',
                              image_on='images\Buttons\medium_button_on.png', text='Средняя',
                              command=self.set_medium)
        self.hard = Buttons(x_cor=50, y_cor=300,  # включение/выключение музыки
                            image='images\Buttons\hard_button.png',
                            image_on='images\Buttons\hard_button_on.png', text='Тяжелая',
                            command=self.set_hard)
        self.del_game_progress = Buttons(x_cor=50, y_cor=520,  # Стирает инфоррмацию об персонеаже
                                         image='images\Buttons\long_button.png',
                                         image_on='images\Buttons\long_button_on.png', text='Стереть прогресс',
                                         command=self.show_question)
        self.ask_del_game_progress = Buttons(x_cor=250, y_cor=100,  # Стирает инфоррмацию об персонеаже
                                             image='images\Buttons\long_button.png',
                                             image_on='images\Buttons\long_button_on.png', text='Подтвердить',
                                             command=self.del_progress)
        self.question_list = [self.ask_del_game_progress, self.back_button]
        self.create_information(
            ['Нажав кнопку подтвердить, вы подтверждаете, что', 'хотите УДАЛИТЬ прогресс персонажа БЕЗВОЗВРАТНО.'],
            self.question_list)

        self.complexty = Buttons(x_cor=50, y_cor=400,
                                 image='images\Buttons\easy_button.png' if complexty == 0 else
                                 'images\Buttons\medium_button.png' if complexty == 1 else 'images\Buttons\hard_button.png',
                                 image_on='images\Buttons\easy_button.png' if complexty == 0 else
                                 'images\Buttons\medium_button.png' if complexty == 1 else 'images\Buttons\hard_button.png',
                                 text='Сейчас')

        self.set_go_right_button = Buttons(x_cor=450, y_cor=310,  # включение/выключение музыки
                                           image='images\Buttons\level_button.png',
                                           image_on='images\Buttons\level_button_on.png', text=right,
                                           command=self.set_right_key)

        self.set_go_left_button = Buttons(x_cor=450, y_cor=230,  # включение/выключение музыки
                                          image='images\Buttons\level_button.png',
                                          image_on='images\Buttons\level_button_on.png', text=left,
                                          command=self.set_left_key)

        self.set_jump_button = Buttons(x_cor=450, y_cor=150,  # включение/выключение музыки
                                       image='images\Buttons\level_button.png',
                                       image_on='images\Buttons\level_button_on.png', text=jump,
                                       command=self.set_jump_key)

        self.set_go_down_button = Buttons(x_cor=450, y_cor=390,  # включение/выключение музыки
                                          image='images\Buttons\level_button.png',
                                          image_on='images\Buttons\level_button_on.png', text=down,
                                          command=self.set_down_key)

        self.set_magic = Buttons(x_cor=700, y_cor=150,  # включение/выключение музыки
                                 image='images\Buttons\level_button.png',
                                 image_on='images\Buttons\level_button_on.png', text=magic,
                                 command=self.set_magic_key)

        self.set_tp = Buttons(x_cor=700, y_cor=310,  # включение/выключение музыки
                              image='images\Buttons\level_button.png',
                              image_on='images\Buttons\level_button_on.png', text=tp,
                              command=self.set_tp_key)

        self.set_hill = Buttons(x_cor=700, y_cor=230,  # включение/выключение музыки
                                image='images\Buttons\level_button.png',
                                image_on='images\Buttons\level_button_on.png', text=hill,
                                command=self.set_hill_key)

        # в меню информации
        self.about_autors_button = Buttons(x_cor=250, y_cor=20,  # переход к меню информации об авторах
                                           image='images\Buttons\long_button.png',
                                           image_on='images\Buttons\long_button_on.png', text='Об авторах',
                                           command=self.show_information_about_autors)
        self.about_game_button = Buttons(x_cor=250, y_cor=140,  # переход к меню информации об игре
                                         image='images\Buttons\long_button.png',
                                         image_on='images\Buttons\long_button_on.png', text='Об игре',
                                         command=self.show_information_about_game)
        self.about_person_button = Buttons(x_cor=250, y_cor=260,  # переход к меню информации об персонаже
                                           image='images\Buttons\long_button.png',
                                           image_on='images\Buttons\long_button_on.png', text='О персонаже',
                                           command=self.show_information_about_person)
        # в меню о персонаже
        self.person_skills = Buttons(x_cor=250, y_cor=260,  # переход к меню информации о способностях персонажа
                                     image='images\Buttons\long_button.png',
                                     image_on='images\Buttons\long_button_on.png', text='Способности описание',
                                     text_size=34,
                                     command=self.show_skills)
        # в меню о способностях персонажа
        self.person_skills_develop = Buttons(x_cor=250, y_cor=380,  # переход в меню открытия способнстей
                                             image='images\Buttons\long_button.png',
                                             image_on='images\Buttons\long_button_on.png', text='Способности открыть',
                                             command=self.show_skills_for_open)
        # в меню открытия способностей персонажа
        self.person_skill_teleportation = Buttons(x_cor=250, y_cor=40,  # Открыть телепорт
                                                  image='images\Buttons\long_button.png',
                                                  image_on='images\Buttons\long_button_on.png', text='Телепортация',
                                                  command=self.open_tp)

        self.person_skill_hill = Buttons(x_cor=250, y_cor=160,  # Открыть лечение
                                         image='images\Buttons\long_button.png',
                                         image_on='images\Buttons\long_button_on.png', text='Лечение',
                                         command=self.open_hill)

        # __Конец кнопок меню__
        self.start_button_list = [self.start_button, self.information_button,  # список кнопок главного меню
                                  self.settings_button, self.exit_button]
        self.levels_button_list.append(self.back_button)
        self.what_show = self.start_button_list

        self.information_autors = ['Разработчик: Михеев Андрей',
                                   'Художники: Михеева Александра, Михеев Андрей', 'Музыка: взята из интернета.']
        self.information_game = ['Это игра о хомячке, отправившемуся в путь', 'во имя великой цели.',
                                 'Он отправился в путь ради АРБУЗИКОВ!!!']

        self.information_button_list = [self.about_autors_button, self.about_game_button, self.about_person_button,
                                        self.back_button]
        self.about_autors = []
        self.about_game = []
        self.about_person = []
        self.skills_list = []
        self.skills_for_open = [self.person_skill_teleportation, self.person_skill_hill]
        with open(script_dir + 'images\main_hero\main_hero_info.txt') as about_hero_info:
            about_hero_info_list = about_hero_info.read().split('\n')

            self.create_information([str(i) + ' ' + str(j) for i, j in zip(['Опыт:',
                                                                            'Количество печенек:',
                                                                            'Способность телепорт:',
                                                                            'Способность лечение:',
                                                                            'Способность магическая атака:'],
                                                                           about_hero_info_list[:2] + [
                                                                               'Разблокировано' if i == '1' else 'Заблокировано'
                                                                               for i in about_hero_info_list[2:]])
                                     ],
                                    self.about_person)
        for i in range(10):
            for j in range(3):
                if i + j * 10 <= 22:
                    self.levels_button_list.append(
                        Buttons(x_cor=10 + 80 * i,
                                y_cor=70 + 80 * j,
                                image='images\Buttons\\' + ('close_' if int(
                                    about_hero_info_list[-1]) < i + j * 10 - 1 else '') + 'level_button.png',
                                image_on='images\Buttons\\' + ('close_' if int(
                                    about_hero_info_list[-1]) < i + j * 10 - 1 else '') + 'level_button_on.png',
                                text=str(i + j * 10),
                                command=None if int(about_hero_info_list[-1]) < i + j * 10 - 1 else self.start_level))
        self.create_information(
            ['Лучше проходить уровни попорядку, не пропуская их.', 'Прохождение одного уровня, откроет два следующих.'],
            self.levels_button_list)
        self.create_information(self.information_autors, self.about_autors)
        self.create_information(self.information_game, self.about_game)
        self.create_information(['Тут приведено описание спсобностей', 'Всего три способности.',
                                 'Все способности потребляют печеньки, имеют перезарядку.',
                                 'Телепорт телепортирует(неожидано).',
                                 ' Ограничение по телепортации, нельзя выйти за пределы уровня.',
                                 'телопорт потребляет 5 печенек, перезарядка 5 секунд',
                                 'Лечение мгновенно востанавливает большое количество',
                                 ' hp. Перезарядка 12. Потребление 34. Используй чаще!',
                                 'Последнее заклинание выпускает магический снаряд во врага,',
                                 ' сняряд не проходит сквозь блоки, имеет высокую скорость,',
                                 'эффективно против боссов. Потребление 2, перезярядка 0.8.',
                                 'Урон снаряда равен удвоенному урону Хомы!',
                                 'Некоторые уровни нельзя пройти, не применяя способности!'], self.skills_list)
        self.create_information(['Открыть телепортацию за 300 печенек.', '', '', 'Открыть лечение за 100 печенек.',
                                 '', '', '', 'Способность магическая атака открывается сама после 6-го уровня'],
                                self.skills_for_open)
        self.create_information(['Версия 1.0'], self.start_button_list, x_cor=60, append_back=0)
        self.settings_button_list = [self.music_button, self.easy, self.medium, self.hard, self.set_go_right_button,
                                     self.set_go_left_button, self.set_go_down_button, self.set_jump_button,
                                     self.set_tp, self.set_hill, self.set_magic, self.complexty, self.del_game_progress]
        self.create_information(['                                                                    Музыка:',
                                 'Выбор сложности:                                                                                  '],
                                self.settings_button_list)
        self.create_information(['', '', 'Кнопки:', '', 'Прыжок', '', 'Влево', '', 'Вправо', '', 'Вниз'],
                                self.settings_button_list)
        self.create_information(['', '', '', '', 'Маг. атака', '', 'Лечение', '', 'Телепортация'],
                                self.settings_button_list, x_cor=610)

        self.about_person.append(self.person_skills)
        self.about_person.append(self.person_skills_develop)

        self.click_time = 0

        self.buttons_sprite_group = pygame.sprite.Group()

    def what_buttons(self, what_on_menu):
        if what_on_menu == 'start':
            self.what_show = self.start_button_list
        elif what_on_menu == 'levels':
            self.what_show = self.levels_button_list
            pygame.mouse.set_pos(400, 89)
        elif what_on_menu == 'settings':
            self.what_show = self.settings_button_list
        elif what_on_menu == 'information':
            self.what_show = self.information_button_list
        elif what_on_menu == 'information_about_autors':
            self.what_show = self.about_autors
        elif what_on_menu == 'information_about_person':
            self.what_show = self.about_person
        elif what_on_menu == 'information_about_game':
            self.what_show = self.about_game
        elif what_on_menu == 'skills':
            self.what_show = self.skills_list
        elif what_on_menu == 'skills_for_open':
            self.what_show = self.skills_for_open
        elif what_on_menu == 'level':
            self.what_show = [Buttons(x_cor=960, y_cor=0,
                                      image='images\Buttons\in_level.png',
                                      image_on='images\Buttons\in_level_on.png', text='',
                                      command=self.go_main_menu)]
        elif what_on_menu == 'question':
            self.what_show = self.question_list

        else:
            print('++++++++++\n', 'ОШИБКА МЕНЮ')

    def show_skills(self):
        self.what_buttons('skills')

    def del_progress(self):
        with open(script_dir + 'images\main_hero\main_hero_info.txt', 'w') as file:
            file.write('\n'.join(['0', '80', '0', '0', '0', '-1']))

        self.reload_menu()

    def show_question(self):
        self.what_buttons('question')

    def show_skills_for_open(self):
        self.what_buttons('skills_for_open')

    def reload_menu(self):
        self.__init__(self.window)

    def open_hill(self):
        result = False
        with open(script_dir + 'images\main_hero\main_hero_info.txt') as about_hero_info:
            about_hero_info_list = about_hero_info.read().split('\n')
            if int(about_hero_info_list[1]) >= 100 and about_hero_info_list[3] != '1':
                about_hero_info_list[1] = str(int(about_hero_info_list[1]) - 100)
                about_hero_info_list[3] = '1'
                result = True
        with open(script_dir + 'images\main_hero\main_hero_info.txt', 'w') as info_file:
            info_file.write('\n'.join(about_hero_info_list))
        if result:
            self.reload_menu()

    def open_tp(self):
        result = False
        with open(script_dir + 'images\main_hero\main_hero_info.txt') as about_hero_info:
            about_hero_info_list = about_hero_info.read().split('\n')
            if int(about_hero_info_list[1]) >= 300 and about_hero_info_list[2] != '1':
                about_hero_info_list[1] = str(int(about_hero_info_list[1]) - 300)
                about_hero_info_list[2] = '1'
                result = True
        with open(script_dir + 'images\main_hero\main_hero_info.txt', 'w') as info_file:
            info_file.write('\n'.join(about_hero_info_list))
        if result:
            self.reload_menu()

    def start(self):
        self.what_buttons('levels')
        return 'start'

    def go_main_menu(self):
        self.what_buttons('start')
        return 'main_menu'

    def set_easy(self):
        self.change_settings_file(7, 0)
        self.set_complexty_image(0)

    def set_medium(self):
        self.change_settings_file(7, 1)
        self.set_complexty_image(1)

    def set_hard(self):
        self.change_settings_file(7, 2)
        self.set_complexty_image(2)

    def set_complexty_image(self, complexty):
        self.complexty.__init__(x_cor=50, y_cor=400,  # включение/выключение музыки
                                image='images\Buttons\easy_button.png' if complexty == 0 else
                                (
                                    'images\Buttons\medium_button.png' if complexty == 1 else 'images\Buttons\hard_button.png'),
                                image_on='images\Buttons\easy_button.png' if complexty == 0 else
                                (
                                    'images\Buttons\medium_button.png' if complexty == 1 else 'images\Buttons\hard_button.png'),
                                text='Сейчас',
                                command=self.set_hard)

    def show_information_about_person(self):
        self.what_buttons('information_about_person')
        pygame.mouse.set_pos(400, 250)

    def show_information_about_game(self):
        self.what_buttons('information_about_game')

    def show_information_about_autors(self):
        self.what_buttons('information_about_autors')

    def set_click_time(self):  # Чтобы кнопки не нажимались многократно
        '''устанавливает время нажатия'''
        self.click_time = time.time()

    def click(self, m_x_cor, m_y_cor, is_click):
        for bt in self.what_show:
            result = bt.click(m_x_cor, m_y_cor, is_click)
            if result:
                return result, bt.text

    def draw(self):
        for bt in self.what_show:
            bt.draw(self.window)

    def start_level(self):
        self.what_buttons('level')
        return 'loadl'

    def create_information(self, information_list, where_append, x_cor=400, append_back=1):
        for n, text in enumerate(information_list):
            where_append.append(
                Buttons(x_cor=x_cor,
                        y_cor=20 + 40 * n,
                        text=text,
                        image='images\Buttons\For_text.png',
                        image_on='images\Buttons\For_text.png',
                        text_color=(255, 255, 0), text_size=28))
        if append_back:
            where_append.append(self.back_button)

    def show_settings(self):
        self.what_buttons('settings')
        self.set_click_time()

    def exit(self):
        quit('Выход через кнопку в меню')

    def show_information(self):
        pygame.mouse.set_pos(400, 250)
        self.what_buttons('information')

    def work_music(self):
        if time.time() - self.click_time > 0.1:
            self.set_click_time()
            return 'music'

    def set_right_key(self):
        if time.time() - self.click_time > 0.1:
            self.set_go_right_button.change_text(self.read_key(2))

    def set_left_key(self):
        if time.time() - self.click_time > 0.1:
            self.set_go_left_button.change_text(self.read_key(1))

    def set_jump_key(self):
        if time.time() - self.click_time > 0.1:
            self.set_jump_button.change_text(self.read_key(0))

    def set_down_key(self):
        if time.time() - self.click_time > 0.1:
            self.set_go_down_button.change_text(self.read_key(3))

    def set_magic_key(self):
        if time.time() - self.click_time > 0.1:
            self.set_magic.change_text(self.read_key(4))

    def set_hill_key(self):
        if time.time() - self.click_time > 0.1:
            self.set_hill.change_text(self.read_key(5))

    def set_tp_key(self):
        if time.time() - self.click_time > 0.1:
            self.set_tp.change_text(self.read_key(6))

    def read_key(self, string_number):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == 1073741906:
                        answer = 'Ве'
                    elif event.key == 1073741905:
                        answer = 'Ни'
                    elif event.key == 1073741903:
                        answer = 'Пр'
                    elif event.key == 1073741904:
                        answer = 'Ле'
                    else:
                        answer = chr(event.key)
                    self.change_settings_file(string_number, event.key)
                    return answer
                if event.type == pygame.QUIT:
                    quit('крестиком')

    def change_settings_file(self, string_number, text):
        with open(script_dir + 'settings.txt') as file:
            info_list = file.read().split('\n')
            info_list[string_number] = str(text)
        with open(script_dir + 'settings.txt', 'w') as file:
            file.write('\n'.join(info_list))


class Label:
    def __init__(self, x_cor=0, y_cor=0, text='12345', text_color=(255, 255, 0), text_size=36):
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.text_size = text_size
        self.text_color = text_color

        self.text = text
        rect = pygame.Rect(x_cor, y_cor, 1, 1)
        bottom_right = rect.bottomright
        self.x_cor2, self.y_cor2 = self.x_cor + bottom_right[0], self.y_cor + bottom_right[1]
        self.image_text = pygame.font.SysFont('arial', text_size).render(self.text, 1, text_color)
        text_mid = (self.image_text.get_rect().topleft[0] + self.image_text.get_rect().bottomright[0]) // 2
        self.text_cor = (self.x_cor + self.x_cor2) // 2 - text_mid, \
                        (self.y_cor + self.y_cor2) // 2 - 18

    def change_text(self, new_text):
        self.image_text = pygame.font.SysFont('arial', self.text_size).render(new_text, 1, self.text_color)
        text_mid = (self.image_text.get_rect().topleft[0] + self.image_text.get_rect().bottomright[0]) // 2
        self.text_cor = (self.x_cor + self.rect.bottomright[0]) // 2 - text_mid, \
                        (self.y_cor + self.rect.bottomright[1]) // 2 - 18

    def draw_text(self, window):
        window.blit(self.image_text, self.text_cor)


class Buttons(Label, pygame.sprite.Sprite):
    image_dict = {}
    for image_name in ['images\Buttons\close_level_button.png', 'images\Buttons\close_level_button_on.png',
                       'images\Buttons\easy_button.png',
                       'images\Buttons\easy_button_on.png', 'images\Buttons\For_text.png',
                       'images\Buttons\hard_button.png', 'images\Buttons\hard_button_on.png',
                       'images\Buttons\in_level.png', 'images\Buttons\in_level_on.png',
                       'images\Buttons\level_button.png', 'images\Buttons\level_button_on.png',
                       'images\Buttons\long_button.png', 'images\Buttons\long_button_on.png',
                       'images\Buttons\medium_button.png',
                       'images\Buttons\medium_button_on.png', 'images\Buttons\music_button.png',
                       'images\Buttons\music_button_on.png']:
        image_dict[image_name] = pygame.image.load(script_dir + image_name)

    def __init__(self, x_cor=0, y_cor=0, image='images\Buttons\long_button.png', text=' ', command=None,
                 image_on=None, text_color=(0, 0, 0),
                 text_size=36, group=None):
        Label.__init__(self, x_cor, y_cor, text, text_color, text_size)
        pygame.sprite.Sprite.__init__(self, group)

        self.start_image = self.image_dict[image]
        image_rect = self.start_image.get_rect()
        self.rect = image_rect.move(x_cor, y_cor)

        self.image_on = self.image_dict[image_on]

        self.image = self.start_image

        text_mid = (self.image_text.get_rect().topleft[0] + self.image_text.get_rect().bottomright[0]) // 2
        self.text_cor = (self.x_cor + self.rect.bottomright[0]) // 2 - text_mid, \
                        (self.y_cor + self.rect.bottomright[1]) // 2 - 18

        self.command = command

    def click(self, m_x_cor, m_y_cor, is_click, menu):
        if self.rect.collidepoint(m_x_cor, m_y_cor):
            self.image = self.image_on
            if is_click:
                if self.command:
                    result = self.command.execute(menu)
                    if type(result) == tuple:
                        if result[0] == 'change@#button@#text':
                            self.change_text(result[1])
                            return result[1]
                    return self.command.execute(menu)
        else:
            self.image = self.start_image


class ComplextyButton(Buttons):
    def __init__(self, x_cor=0, y_cor=0, image='images\Buttons\long_button.png', text=' ', command=None,
                 image_on=None, text_color=(0, 0, 0),
                 text_size=36, group=None):
        super(ComplextyButton, self).__init__(x_cor, y_cor, image, text, command,
                                              image_on, text_color, text_size, group)

    def change_image(self, complexty):
        start_image = 'images\Buttons\easy_button.png' if complexty == 0 else \
            'images\Buttons\medium_button.png' if complexty == 1 else 'images\Buttons\hard_button.png'
        image_on = 'images\Buttons\easy_button.png' if complexty == 0 else \
            'images\Buttons\medium_button.png' if complexty == 1 else 'images\Buttons\hard_button.png'
        self.start_image = self.image_dict[start_image]
        self.image_on = self.image_dict[image_on]
        self.image = self.start_image


class OldButtons():  # В пайгейм нет готовых кнопок
    def __init__(self, x_cor=0, y_cor=0, image=None, text='12345', command=None, image_on=None, text_color=(0, 0, 0),
                 text_size=36):
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.text_size = text_size
        self.text_color = text_color
        self.image = pygame.image.load(script_dir + image)

        self.image_on = pygame.image.load(script_dir + image_on)

        self.image_now = self.image

        self.text = text
        rect = self.image.get_rect()
        bottomright = rect.bottomright
        self.x_cor2, self.y_cor2 = self.x_cor + bottomright[0], self.y_cor + bottomright[1]
        self.image_text = pygame.font.SysFont('arial', text_size).render(self.text, 1, text_color)
        text_mid = (self.image_text.get_rect().topleft[0] + self.image_text.get_rect().bottomright[0]) // 2
        self.text_cor = (self.x_cor + self.x_cor2) // 2 - text_mid, \
                        (self.y_cor + self.y_cor2) // 2 - 18

        self.command = command

    def change_text(self, new_text):
        self.image_text = pygame.font.SysFont('arial', self.text_size).render(new_text, 1, self.text_color)
        text_mid = (self.image_text.get_rect().topleft[0] + self.image_text.get_rect().bottomright[0]) // 2
        self.text_cor = (self.x_cor + self.x_cor2) // 2 - text_mid, \
                        (self.y_cor + self.y_cor2) // 2 - 18

    def draw(self, window):
        if self.image_now:
            window.blit(self.image_now, (self.x_cor, self.y_cor))
        window.blit(self.image_text, self.text_cor)

    def click(self, m_x_cor, m_y_cor, is_click):
        if self.x_cor <= m_x_cor <= self.x_cor2 \
                and self.y_cor <= m_y_cor <= self.y_cor2:
            self.image_now = self.image_on
            if is_click:
                if self.command:
                    return self.command()
        else:
            self.image_now = self.image


class MenuSection:
    def __init__(self, menu, name=''):
        self.main_menu = menu
        self.button_list = []
        self.label_list = []
        self.name = name

        self.buttons_sprite_group = pygame.sprite.Group()

        self.button_count = 0

    def get_sprite_group(self):
        return self.buttons_sprite_group

    def add_button(self, button):
        self.button_list.append(button)

    def add_label(self, label):
        self.label_list.append(label)

    def draw(self, window):
        self.buttons_sprite_group.draw(window)
        for button in self.button_list:
            button.draw_text(window)
        for label in self.label_list:
            label.draw_text(window)

    def __next__(self):
        try:
            answer = self.button_list[self.button_count]
            self.button_count += 1
            return answer
        except IndexError:
            self.button_count = 0
            raise StopIteration

    def __iter__(self):
        return self


class Menu:
    def __init__(self):
        self.menu_section_dict = {}
        self.menu_now = 'main_menu'

        self.init_menu_sections()

    def init_menu_sections(self):
        self.menu_section_dict['main_menu'] = buttons_maker.create_main_menu_buttons()
        self.menu_section_dict['levels'] = buttons_maker.crete_levels_section()
        self.menu_section_dict['into_level'] = buttons_maker.create_level_button()
        self.menu_section_dict['settings'] = buttons_maker.crete_settings_section()
        self.menu_section_dict['ask_del_progress'] = buttons_maker.create_ask_del_game_progress_buttons()
        self.menu_section_dict['information'] = buttons_maker.create_info_menu()
        self.menu_section_dict['about_autors'] = buttons_maker.create_about_autors_menu()
        self.menu_section_dict['about_game'] = buttons_maker.create_about_game_menu()
        self.menu_section_dict['about_person'] = buttons_maker.create_about_person_menu()
        self.menu_section_dict['about_skills'] = buttons_maker.create_about_skills_menu()
        self.menu_section_dict['open_skills'] = buttons_maker.create_open_skills()

    def change_section_now(self, menu_now):
        self.menu_now = menu_now

    def run(self, m_x_cor, m_y_cor, is_click):
        for bt in self.menu_section_dict[self.menu_now]:
            result = bt.click(m_x_cor, m_y_cor, is_click, self)
            if result:
                return result, bt.text

    def draw(self, window):
        self.menu_section_dict[self.menu_now].draw(window)

    def reload_menu(self):
        self.__init__()


import buttons_maker
