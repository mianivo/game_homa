import pygame.font
from levels import *
from script_dir import script_dir

pygame.init()


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
