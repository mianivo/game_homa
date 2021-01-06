import pygame
from script_dir import script_dir


# Класс не наследуется, т.к. имеет слишком много особенностей
class Magic:
    '''Магия для атаки.'''
    def __init__(self, x, y, is_right, damage, main_hero, image_magic_list=['images\magic\magic_1.png',
                                                                            'images\magic\magic_2.png',
                                                                            'images\magic\magic_3.png',
                                                                            'images\magic\magic_4.png'],
                 dekor_image='images\magic\magic_dekor_1.png'):
        self.image_magic_list = [pygame.image.load(script_dir + im) for im in image_magic_list]
        self.x_cor = x
        self.y_cor = y
        self.rect = self.image_magic_list[0].get_rect()
        self.is_right = is_right
        self.move_count = 0
        self.anim_count = 0
        self.anim_count_max = 3
        width, height = self.rect.bottomright
        self.rect = pygame.Rect((x - width, y), (width, height))
        self.image_dekor = pygame.image.load(script_dir + dekor_image)
        self.main_hero = main_hero
        self.where_dekor_list = []
        self.end = False
        self.damage = damage
        self.type = 'magic'

    def move(self):
        if self.move_count < 32:
            self.move_count += 2
        x = self.move_count
        if self.move_count % 4 == 0:
            self.where_dekor_list.append([*self.rect.topright, 4])
        x = x if self.is_right else -x
        self.change_animation()
        self.rect = self.rect.move(x, 0)

    def draw(self, window):
        window.blit(self.image_magic_list[self.anim_count], self.rect.topright)
        for n, dekor in enumerate(self.where_dekor_list):
            window.blit(self.image_dekor, (dekor[0] - 5, dekor[1] - 5))
            dekor[2] -= 1
            if dekor[2] < 0:
                self.where_dekor_list.pop(n)

    def change_animation(self):
        self.anim_count += 1
        if self.anim_count > self.anim_count_max:
            self.anim_count = 0

    def unique_properties(self, hero):
        '''Когда врезается во врага или врезается в блок, пропадает'''
        hero.change_hp(-self.damage)
        if hero.type == 'enemy':
            if hero.is_dead:
                self.main_hero.change_xp(hero.xp_for_main_hero // 2)
        self.end = True
        return True