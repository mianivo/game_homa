from enemy import Enemy
from squirrel import Squirrel
import pygame
import time
from magic import Magic

from script_dir import script_dir


class Boss(Enemy):
    image_list_left = [pygame.image.load(script_dir + im) for im in
                       ['images\esh_king\left0.png', 'images\esh_king\left1.png',
                        'images\esh_king\left2.png']]
    image_list_right = [pygame.image.load(script_dir + im) for im in
                        ['images\esh_king\\right0.png', 'images\esh_king\\right1.png',
                         'images\esh_king\\right2.png']]

    def __init__(self, x, y, main=True, group=None):
        Enemy.__init__(self, x, y, speed=5, hp=10000, name='Ежице!',
                       how_much_go_right=65, how_much_go_left=65, damage=100, group=group)
        self.main_boss = main
        self.fase_time = 0
        self.was_hp = False
        self.xp_for_main_hero = 400
        self.hp_color = (50, 255, 50)

    def draw_additional(self, window):
        if self.main_boss:
            pygame.draw.rect(window, self.hp_color,
                             (60, 765, self.hp // 11, 20))

    def update(self, *args, **kwargs) -> None:
        if self.is_dead:
            self.remove(self.groups())

    def do_enemys(self):
        return 'do_e'

    def set_fase_time(self):
        self.fase_time = time.time()

    def enemy_move(self):
        '''Логика босса'''
        Enemy.enemy_move(self)
        if not self.was_hp and self.hp < 1500:  # При низком здорьвье восполняет его. 1 раз.
            self.change_hp(3501)
            self.was_hp = True
        if time.time() - self.fase_time > 15 + 0.41554:  # раз в 15 секунд делает действия
            if self.hp < 5000:  # Увеличивает урон и скорость
                self.speed = 6
                self.damage = 200
            if self.hp < 10000:  # регенерация
                self.change_hp(500)
            self.set_fase_time()
            if self.hp < 7500:  # возвращает сигнал к созданию врагов
                return self.do_enemys()
            self.hp_color = (255, 50, 50)
        if time.time() - self.fase_time > 3:
            self.hp_color = (50, 255, 50)


class Boss2(Squirrel, Boss):
    '''Финальный босс.'''
    image_list_left = [pygame.image.load(script_dir + im) for im in ['images\\final_boss\\final_boss_left_1.png',
                                                                     'images\\final_boss\\final_boss_left_2.png',
                                                                     'images\\final_boss\\final_boss_left_3.png']]
    image_list_right = [pygame.image.load(script_dir + im) for im in ['images\\final_boss\\final_boss_right_1.png',
                                                                      'images\\final_boss\\final_boss_right_2.png',
                                                                      'images\\final_boss\\final_boss_right_3.png']]

    def __init__(self, x, y, group):
        Boss.__init__(self, x, y, group=group)
        Squirrel.__init__(self, x, y, group=group)
        self.hp = 30500
        self.damage = 90
        self.xp_for_main_hero = 950
        self.for_fase_time = self.hp // 2000 + 4
        self.type = 'f'
        self.rect.height += 1
        self.magic_time = 0

    def enemy_move(self):
        '''Фазы теже что и у первого босса, но с другими цифрами. Но поведение перемещения унаследовано от белки.'''
        Squirrel.enemy_move(self)
        self.for_fase_time = self.hp // 1000 + 6
        self.for_magic_time = self.for_fase_time // 2
        self.speed = 3 - (self.hp // 7000) + 4
        if not self.was_hp and self.hp < 7501:
            self.change_hp(10000)
            self.was_hp = True
        if time.time() - self.fase_time > self.for_fase_time:
            if self.hp < 30000:
                self.change_hp(1000)
            self.set_fase_time()
            self.hp_color = (255, 0, 10)
            return self.do_enemys()
        if time.time() - self.fase_time > 3:
            self.hp_color = (100, 255, 100)

    def draw_additional(self, window):
        if self.main_boss:
            pygame.draw.rect(window, self.hp_color,
                             (60, 765, self.hp // 33, 20))

    def set_magic_time(self):
        self.magic_time = time.time()

    def do_magic(self):
        '''Раз в определнное время стреляет магией, как главный герой.'''
        if time.time() - self.magic_time > self.for_magic_time:
            self.set_magic_time()
            if self.is_go_right:
                return Magic(*self.rect.topright, True, self.damage * 2, self, is_boss_magic=True, group=self.groups())
            else:
                return Magic(*self.rect.topleft, False, self.damage * 2, self, is_boss_magic=True, group=self.groups())
