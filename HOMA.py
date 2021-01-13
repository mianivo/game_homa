import pygame
from person import Person
from item_to_take import Cookies, Hearts
from magic import Magic
import time
from script_dir import script_dir


class Homa(Person):  # Главного героя - хомяка зовут Хома!.
    image_list_left = [pygame.image.load(script_dir + im) for im in
                       ['images\main_hero\Left0.png', 'images\main_hero\Left1.png',
                        'images\main_hero\Left2.png']]
    image_list_right = [pygame.image.load(script_dir + im) for im in
                        ['images\main_hero\Right0.png', 'images\main_hero\Right1.png',
                         'images\main_hero\Right2.png']]

    def __init__(self, x, y, speed=4, hp=400, complexity=0, group=None):
        Person.__init__(self, x, y, speed, hp, 'Хома!', group)
        self.complexity = complexity  # сложность от неё зависит получаемый урон.
        self.is_jump = False
        self.can_jump = False
        self.want_jump = False
        self.jump_count = 10
        with open(script_dir + 'images\main_hero\main_hero_info.txt', encoding='utf-8') as info_file:
            all_info = info_file.read()  # читаем информацию о прогрессе игры
            self.xp, self.cook_count, *self.skills = [i for i in all_info.split('\n')]

        self.xp = int(self.xp)
        self.cook_count = int(self.cook_count)
        self.level = self.xp // 200 + 1
        self.image_text_xp = pygame.font.SysFont('arial', 36).render(str(self.level), 1, (255, 255, 0))
        self.is_dead = False
        self.rect_list = []
        self.damage = self.level * 11 + 130
        self.type = 'main_hero'

        self.hp = self.level * 50 + 250
        self.cook_image = pygame.image.load(script_dir + 'images\items_to_take\Cook.png')
        self.cook_image_text = pygame.font.SysFont('arial', 24).render(str(self.cook_count), 1, (255, 200, 0))
        self.heart_image = pygame.image.load(script_dir + 'images\items_to_take\Heart.png')
        self.tp_time = 0
        self.hill_time = 0
        self.magic_time = 0
        if self.level >= 5:
            self.skills[2] = '1'

        self.move_count_for_not_main_hero = 40

    def change_hp(self, how_much):
        Person.change_hp(self, how_much * ((self.complexity * 2 + 1) if how_much < 0 else 1))

    def enemy_move(self):
        '''Если используется не как главный герой, а как декоративный персонаж.(используется только на 20 уровне)'''
        if self.move_count_for_not_main_hero:
            self.move_count_for_not_main_hero -= 1
            self.go_left()
        else:
            self.move_count_for_not_main_hero = 35
            self.jump_start()
        self.jump()
        if self.rect.topleft[0] < -100:
            self.is_dead = True

    def do_heart(self):
        pass

    def jump(self):
        '''Прыжок.'''
        if self.want_jump and self.can_jump:  # Если была нажата кнопка прыжка и мы не падаем.
            self.is_jump = True
            self.is_fall = False
            self.jump_count -= 1
            self.move(y=-self.speed * 3)
            if self.jump_count < 0:
                self.jump_count = 12
                self.is_jump = False
                self.is_fall = True
                self.can_jump = False
        else:
            self.is_jump = False
            self.want_jump = False
            self.is_fall = True

    def draw_info(self, window):
        self.hp_line = self.hp % 800  # линия здоровья
        if self.hp > 700:
            self.image_text_hp = pygame.font.SysFont('arial', 28).render('X' + str(self.hp // 801 + 1), 1, (255, 0, 0))
            window.blit(self.image_text_hp, (self.hp_line + 80, 8))
        pygame.draw.rect(window, (255, 0, 0), (35, 20, self.hp_line, 10))
        pygame.draw.rect(window, (255, 255, 0), (35, 50, self.xp - (self.level - 1) * 200, 10))  # линия опыта
        window.blit(self.image_text_xp, (4, 35))

        window.blit(self.heart_image, (1, 5))

        window.blit(self.cook_image, (250, 35))
        window.blit(self.cook_image_text, (290, 35))

    def change_xp(self, how_much):
        self.xp += how_much
        if self.xp % 200 > 0:
            self.level = self.xp // 200 + 1
            self.image_text_xp = pygame.font.SysFont('arial', 36).render(str(self.level), 1, (255, 255, 0))

    def change_cook_count(self, how_much=1):
        Person.change_cook_count(self, how_much * 3 if how_much > 0 else how_much)
        self.cook_image_text = pygame.font.SysFont('arial', 24).render(str(self.cook_count), 1, (255, 200, 0))

    def jump_start(self):
        '''Сообщаем, что хотим прыгнуть. Вызывается, когда нажата кнопка прыжка'''
        self.want_jump = True

    def teleportation(self):
        '''Телепортация.'''
        if self.cook_count > 4:
            if time.time() - self.tp_time > 5 and self.skills[0] == '1':
                kord = self.rect.topleft
                if self.is_go_right and self.rect.topright[0] + 120 < 1000:
                    self.move(x=120)
                    self.in_other_rect(1, 0)
                elif self.is_go_left and self.rect.topleft[0] - 120 > -10:
                    self.move(x=-120)
                    self.in_other_rect(-1, 0)
                else:
                    return
                if self.rect.topleft == kord:
                    return
                self.change_cook_count(-5)
                self.was_tp = True
                self.set_tp_time()

    def set_tp_time(self):
        self.tp_time = time.time()

    def set_hill_time(self):
        self.hill_time = time.time()

    def set_magic_time(self):
        self.magic_time = time.time()

    def hill(self):
        if self.cook_count > 33:
            if time.time() - self.hill_time > 12:
                if self.skills[1] == '1':
                    self.change_hp(600)
                    self.set_hill_time()
                    self.change_cook_count(-34)

    def end_level(self):
        '''Сохраняем прогресс при завершении уровня (по любой причине).'''
        with open(script_dir + 'images\main_hero\main_hero_info.txt', 'w') as info_file:
            info_file.write('\n'.join([str(self.xp), str(self.cook_count), *self.skills]))

    def do_magic(self):
        '''Магическая атака. Возвращает экземпляр класса магия.'''
        if self.cook_count > 1:
            if self.skills[2] == '1':
                if time.time() - self.magic_time > 0.7:
                    self.change_cook_count(-2)
                    self.set_magic_time()
                    if self.is_go_right:
                        return Magic(*self.rect.topright, True, self.damage * 2, self, group=self.groups())
                    else:
                        return Magic(*self.rect.topleft, False, self.damage * 2, self, group=self.groups())
