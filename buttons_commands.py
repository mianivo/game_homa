from script_dir import script_dir

import pygame
from abc import ABC, abstractmethod

with open(script_dir + 'settings.txt') as file:
    dict_chars = {1073741906: 'Ве', 1073741905: 'Ни', 1073741903: 'Пр', 1073741904: 'Ле'}
    strings = file.read().split('\n')
    jump, left, right, down, magic, hill, tp, complexty = [dict_chars[int(i)] if int(i) in
                                                                                 dict_chars else chr(
        int(i)) if n < 7 else i for n, i in enumerate(strings)]
    complexty = int(strings[-1])

with open(script_dir + 'images\main_hero\main_hero_info.txt') as about_hero_info:
    about_hero_info_list = about_hero_info.read().split('\n')


class Command(ABC):
    @abstractmethod
    def execute(self, menu):
        pass


class ChangeSettingsFileCommand(Command):
    def __init__(self, string_number, text='1'):
        self.string_number = string_number
        self.text = text

    def change_settings_file(self, string_number, text):
        with open(script_dir + 'settings.txt') as file:
            info_list = file.read().split('\n')
            info_list[string_number] = str(text)
        with open(script_dir + 'settings.txt', 'w') as file:
            file.write('\n'.join(info_list))

    def execute(self, menu=None):
        self.change_settings_file(self.string_number, self.text)


class ChangeMenuSectionCommand(Command):
    def __init__(self, section_name, mouse_move=()):
        self.new_section_name = section_name
        self.mouse_move = mouse_move

    def execute(self, menu):
        menu.change_section_now(self.new_section_name)
        if self.mouse_move:
            pygame.mouse.set_pos(*self.mouse_move)


class QuitCommand(Command):
    def execute(self, menu):
        quit('Выход через кнопку в меню')


class ReturnCommand(ChangeMenuSectionCommand):
    def __init__(self, what_return, section_name='', mouse_move=()):
        super().__init__(section_name, mouse_move)
        self.what_return = what_return

    def execute(self, menu):
        if self.new_section_name:
            super().execute(menu)
        return self.what_return


import time


class MusicCommand(Command):

    def __init__(self):
        self.click_time = 0

    def execute(self, menu):
        if self.click_time + 0.4 < time.time():
            self.click_time = time.time()
            pygame.mixer.music.pause() if pygame.mixer.music.get_busy() else pygame.mixer.music.unpause()


class SetKeyCommand(ChangeSettingsFileCommand):
    def read_key(self):
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
                    self.change_settings_file(self.string_number, event.key)
                    return answer
                if event.type == pygame.QUIT:
                    quit('крестиком')

    def execute(self, menu=None):
        return ('change@#button@#text', self.read_key())


class ChangeComplextyCommand(ChangeSettingsFileCommand):
    def __init__(self, button, string_number, text='1'):
        super().__init__(string_number, text)
        self.button_for_change = button

    def execute(self, menu=None):
        super().execute(menu)
        self.button_for_change.change_image(self.text)


class DelProgressCommand(Command):
    def execute(self, menu=None):
        with open(script_dir + 'images\main_hero\main_hero_info.txt', 'w') as file:
            file.write('\n'.join(['0', '80', '0', '0', '0', '-1']))
        menu.__init__()
        menu.change_section_now('main_menu')


back_button_command = ChangeMenuSectionCommand('main_menu')

start_button_command = ChangeMenuSectionCommand('levels', mouse_move=(400, 89))
settings_button_command = ChangeMenuSectionCommand('settings', mouse_move=(400, 89))
information_button_command = ChangeMenuSectionCommand('information')
quit_button_command = QuitCommand()

levels_command = ReturnCommand('loadl', 'into_level')
into_level_command = ReturnCommand('main_menu', 'levels')

music_command = MusicCommand()

set_jump_key = SetKeyCommand(0)
set_left_key = SetKeyCommand(1)
set_right_key = SetKeyCommand(2)
set_down_key = SetKeyCommand(3)
set_magic_key = SetKeyCommand(4)
set_hill_key = SetKeyCommand(5)
set_tp_key = SetKeyCommand(6)

ask_del_progress = ChangeMenuSectionCommand('ask_del_progress')
del_progress = DelProgressCommand()

about_autors_button_command = ChangeMenuSectionCommand('about_autors')
about_game_button_command = ChangeMenuSectionCommand('about_game')
about_person_button_command = ChangeMenuSectionCommand('about_person', mouse_move=(400, 189))

about_skills_button_command = ChangeMenuSectionCommand('about_skills')
open_skills_button_command = ChangeMenuSectionCommand('open_skills')


class OpenHillSkill(Command):
    def execute(self, menu=None):
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
            menu.reload_menu()


open_hill_command = OpenHillSkill()


class OpenTeleportSkill(Command):
    def execute(self, menu):
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
            menu.reload_menu()


open_tp_command = OpenTeleportSkill()
