import pygame
from script_dir import script_dir


class Shell(pygame.sprite.Sprite):
    def __init__(self, x, y, is_right, is_up, color=(0, 0, 0),
                 dekor_image=pygame.image.load(script_dir + 'images\shell\shell_dekor.png'), group=None):
        '''Снаряд для пушки. Наносит урон только главному герою.'''
        self.image = pygame.image.load(script_dir + 'images\shell\shell.png')
        self.x_cor = x
        self.y_cor = y
        self.color = color
        self.rect = pygame.Rect(x, y, 30, 30)
        self.is_right = is_right
        self.is_up = is_up
        self.end = False
        self.damage = 1000
        self.type = 'shell'
        self.where_dekor_list = [(x, y) for _ in range(3)]
        self.dekor_image = dekor_image
        self.y_cor_fall = -15 if is_up else 0
        self.fall_count = 0

        super().__init__(group)

    def draw_additional(self, window):
        for x, y in self.where_dekor_list:
            window.blit(self.dekor_image, (x, y))
        self.where_dekor_list.pop(0)
        self.where_dekor_list.append((self.rect.topleft[0] + (-25 if self.is_right else 20), self.rect.topleft[1] + (
            self.y_cor_fall if self.y_cor_fall <= 0 else -self.y_cor_fall)))

    def update(self, *args, **kwargs) -> None:
        if self.end:
            self.remove(self.groups())
        self.y_cor_fall += 0.4
        self.rect = self.rect.move(11 if self.is_right else -11, self.y_cor_fall // 1)

    def unique_properties(self, hero):
        hero.change_hp(-self.damage)
        self.end = True
        return True
