import magic
import pygame
from enemy import Enemy
from Shell import Shell
from time import time
from script_dir import script_dir


class Gun(Enemy):
    '''Пушка. Отличия от ежа не перемещается в лево/право. Стреляет снарядами.'''
    gun_image_list = [pygame.image.load(f'{script_dir}\\images\gun\gun{position}.png') for position in range(4)]
    image_list_left = [pygame.image.load(f'{script_dir}\\images\gun\wheel.png')]
    image_list_right = image_list_left

    def __init__(self, x, y,
                 speed=4, hp=800, damage=50, is_active=True, speed_atack=1, position=1, group=None):
        self.gun_image = self.gun_image_list[position]
        Enemy.__init__(self, x, y, speed=speed, hp=hp, damage=damage, group=group)
        self.is_active = is_active
        self.speed_atack = speed_atack
        self.position = position
        self.time_attack = 0

    def enemy_move(self):
        if time() - self.time_attack >= self.speed_atack:
            self.set_time()
            return Shell(x=self.rect.topright[0] + 10 if self.position < 2 else self.rect.topleft[0] - 10,
                         y=(self.rect.topright[1] if self.position % 2 == 1 else self.rect.topright[1] + 5) - 10,
                         is_right=self.position // 2 - 1, is_up=self.position % 2, group=self.groups())

    def set_time(self):
        self.time_attack = time()

    def draw_additional(self, window):
        super(Gun, self).draw_additional(window)
        if not self.is_dead:
            window.blit(self.gun_image, (self.rect.topleft[0] - 10, self.rect.topleft[1] - 10))
