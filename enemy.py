import pygame
from person import Person
import random

from script_dir import script_dir


class Enemy(Person):  # Главного героя - хомяка зовут Хома!.
    image_list_left = [pygame.image.load(script_dir + im) for im in
                       ['images\enemys\esh\left1.png', 'images\enemys\esh\left2.png',
                        'images\enemys\esh\left3.png']]
    image_list_right = [pygame.image.load(script_dir + im) for im in ['images\enemys\esh\Right1.png', 'images\enemys\esh\Right2.png',
                        'images\enemys\esh\Right3.png']]

    def __init__(self, x, y,
                 speed=4, hp=800, name='Ежице!', how_much_go_right=30, how_much_go_left=30, damage=50, group=None):
        Person.__init__(self, x, y, speed, hp, name, group)
        self.how_much_go_right_start = how_much_go_right
        self.how_much_go_left_start = how_much_go_left
        self.damage = damage
        self.xp_for_main_hero = 25

        self.how_much_go_right = how_much_go_right
        self.how_much_go_left = how_much_go_left
        self.type = 'enemy'

        self.do_heart = False

    def enemy_move(self):
        if self.how_much_go_right < 0 and self.is_go_right:
            self.is_go_right = False
            self.how_much_go_right = self.how_much_go_right_start
        if self.how_much_go_left < 0 and self.is_go_left:
            self.how_much_go_left = self.how_much_go_left_start
            self.is_go_right = True

        if self.is_go_right:
            self.how_much_go_right -= 1
            self.go_right()
        else:
            self.how_much_go_left -= 1
            self.go_left()

    def unique_properties(self, main_hero):
        if self.rect.colliderect(main_hero.rect):  # часть взоимодействия с главным героем
            if main_hero.can_jump == False and main_hero.is_jump == False:
                self.change_hp(-main_hero.damage)
                if self.is_dead:
                    main_hero.change_xp(self.xp_for_main_hero)
            else:
                main_hero.change_hp(-self.damage)
            # Подпрыгивает
            if main_hero.is_jump == False:
                to_time_save = self.unique_properties
                self.unique_properties = lambda x: None
                main_hero.in_other_rect(y=1)
                main_hero.want_jump = main_hero.can_jump = True
                main_hero.jump_count = 5
                self.unique_properties = to_time_save
            else:
                return True

    def dead(self):
        Person.dead(self)
        if self.is_dead:
            if random.randrange(0, 12) > 8 or self.cook_count:
                self.do_heart = True

    def draw_additional(self, window):
        if self.get_damage:
            pygame.draw.rect(window, (255, 0, 0),
                             (self.rect.topleft[0] + 10, self.rect.topleft[1] - 20, self.hp // 20, 2))

    def __bool__(self):
        return not self.is_dead
