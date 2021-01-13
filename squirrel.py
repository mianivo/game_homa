from enemy import Enemy
import time
import pygame

from script_dir import script_dir


class Squirrel(Enemy):
    '''Враг - белка. Я попытался ей дать хоть немного логики.'''

    image_list_left = [pygame.image.load(script_dir + im) for im in
                       ['images\enemys\squirrel\left0.png', 'images\enemys\squirrel\left1.png',
                        'images\enemys\squirrel\left2.png']]
    image_list_right = [pygame.image.load(script_dir + im) for im in
                        ['images\enemys\squirrel\\right0.png', 'images\enemys\squirrel\\right1.png',
                         'images\enemys\squirrel\\right2.png']]

    def __init__(self, x, y,
                 speed=5, hp=1400, name='Белка', how_much_go_right=40, how_much_go_left=40, damage=40, main_hero=None,
                 is_go_right=True, group=None):
        Enemy.__init__(self, x=x, y=y, how_much_go_right=how_much_go_right,
                       how_much_go_left=how_much_go_left, speed=speed, hp=hp, name=name, damage=damage, group=group)
        self.is_go_right = is_go_right
        self.near_person = False
        self.rast = 0
        self.is_jump = False
        self.can_jump = False
        self.want_jump = False
        self.jump_count = 10
        self.hero_time = 0
        self.jump_time = 0
        self.turn_time = 0
        self.main_hero = main_hero

    def set_hero(self, hero):
        self.main_hero = hero

    def set_hero_time(self):
        self.hero_time = time.time()

    def set_jump_time(self):
        self.jump_time = time.time()

    def set_turn_time(self):
        self.turn_time = time.time()

    def turn_person(self):
        if time.time() - self.turn_time > 0.6:
            if self.rast > 0:
                self.is_go_left = True
                self.is_go_right = False
            else:
                self.is_go_left = False
                self.is_go_right = True
            self.set_turn_time()

    def where_hero(self):
        '''Смотрит положение относително героя.'''
        rast = self.rect.topleft[0] - self.main_hero.rect.topleft[0]  # Растояние по иксу до героя
        self.rast = rast
        if -self.main_hero.rect.height <= self.rect.topleft[1] - self.main_hero.rect.topleft[
            1] <= self.main_hero.rect.height:  # Если корднаты по игрику примерно равны
            rect_for_check = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] + 20, -self.rast,
                                         1)  # Создаем прямоугольник от белки к главному герою
            if (rast >= 0 and self.is_go_left) or (rast <= 0 and self.is_go_right):
                for block in self.object_list:  # Проверяем прямоугольник на соприкоснавения с блоками
                    if rect_for_check.colliderect(block.rect):
                        return
                self.hero_kor = self.main_hero.rect.topleft
                self.rast = rast
                self.near_person = True
                self.set_hero_time()
                return

    def enemy_move(self):
        self.where_hero()
        self.jump()
        if self.near_person:
            self.turn_person()
            if self.is_go_right:
                self.go_right()
            else:
                self.go_left()
            if -100 <= self.rast <= 120:
                self.jump_start()
        else:
            Enemy.enemy_move(self)
        if time.time() - self.hero_time > 4:
            self.near_person = False
            self.set_hero_time()

    def jump_start(self):
        if time.time() - self.jump_time > 6:
            self.want_jump = True
            self.set_jump_time()

    def jump(self):
        if self.want_jump and self.can_jump:
            self.speed = 4
            self.is_jump = True
            self.is_fall = False
            self.jump_count -= 1
            self.move(y=-self.speed * 3)
            if self.jump_count < 0:
                self.jump_count = 10
                self.is_jump = False
                self.is_fall = True
                self.can_jump = False
        else:
            self.speed = 5
            self.is_jump = False
            self.want_jump = False
            self.is_fall = True

    def unique_properties(self, main_hero):
        if not self.is_jump and not self.is_fall:
            return Enemy.unique_properties(self, main_hero)
        else:
            main_hero.change_hp(-self.damage)
            return True
