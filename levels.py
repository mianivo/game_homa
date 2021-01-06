from blocks import *
import random
import pygame
from HOMA import Homa
from enemy import Enemy
from item_to_take import Cookies, Hearts, Watermelon
from spike import Spikes
from magic import Magic
from squirrel import Squirrel
from boss import Boss, Boss2
from Shell import Shell
from gun import Gun
from script_dir import script_dir


class Level:
    def __init__(self, level_number, complexity):
        self.complexiry = complexity  # Сложность
        self.level_number = level_number
        file_name = 'levels\level' + str(level_number) + '.txt'
        self.image_text = None  # текст для отображения на уровне
        if self.level_number == '19':
            self.image_text = pygame.font.SysFont('arial', 36).render('Головоломка.', 1, (0, 255, 0))
        elif self.level_number == '6':
            self.image_text = pygame.font.SysFont('arial', 36).render('Используй лечение.', 1, (0, 255, 0))
        elif self.level_number == '21':
            self.image_text = pygame.font.SysFont('arial', 36).render('На 22 хуже', 1, (255, 0, 0))
        elif self.level_number == '22':
            self.image_text = pygame.font.SysFont('arial', 36).render('Это реально пройти', 1, (255, 0, 0))
        self.level_size = (1000, 800)
        self.main_hero = None
        with open(script_dir + file_name) as file_object:
            self.level_file = file_object.read()

        self.boss = None  # босс
        self.blocks_on_level_list = []  # список всех блоков
        self.person_list = []  # Список врагов
        self.item_list = []  # Предметы для подбора
        self.magic_list = []  # магия главного героя
        self.shell_list = []  # Снаряды и магия финального босса

        for string in self.level_file.split('\n'):
            object, x_cor, y_cor, *dop = string.split()
            sleep = False
            without = False
            sleep_now = False
            without_now = False
            is_dekor = False
            is_go_right = True
            how_much_go = False
            is_right = 0
            is_up = 0
            speed_atack = 1
            position = 1
            if dop:
                if dop[0] == 'sleep':
                    sleep = True
                    sleep_now = int(dop[1])
                elif dop[0] == 'without':
                    without = True
                    without_now = int(dop[1])
                elif dop[0] == 'dekor':
                    is_dekor = True
                elif dop[0] == 'go':
                    how_much_go = int(dop[1])
                    is_go_right = int(dop[2]) if len(dop) > 2 else False
                elif dop[0] == 'is_right':
                    is_right = 1
                elif dop[0] == 'is_up':
                    is_up = 1
                elif object == 'gun':
                    if dop:
                        speed_atack = float(dop[0])
                        if len(dop) > 1:
                            position = int(dop[1])
                if len(dop) > 1 and dop[1] == 'is_up':
                    is_up = 1

            if 'dirt' == object:
                self.blocks_on_level_list.append(
                    Blocks(int(x_cor), int(y_cor), sleep_block=sleep, sleep_now=sleep_now, without=without,
                           without_now=without_now, is_dekor=is_dekor))
            elif 'stone_wall' == object:
                self.blocks_on_level_list.append(
                    Blocks(int(x_cor), int(y_cor), where_image='images\Blocks\stone_wall.png', sleep_block=sleep,
                           sleep_now=sleep_now, without=without, without_now=without_now, is_dekor=is_dekor))
            elif 'board' == object:
                self.blocks_on_level_list.append(
                    Blocks(int(x_cor), int(y_cor), where_image='images\Blocks\\board.png', sleep_block=sleep,
                           sleep_now=sleep_now, without=without, without_now=without_now, is_dekor=is_dekor))
            elif 'bush' == object:
                self.blocks_on_level_list.append(
                    Dekor(x=int(x_cor), y=int(y_cor), where_image='images\dekor\Bush.png', sleep_block=sleep,
                          sleep_now=sleep_now, without=without, without_now=without_now, is_dekor=is_dekor))
            elif 'gold' == object:
                self.blocks_on_level_list.append(
                    Blocks(int(x_cor), int(y_cor), where_image='images\Blocks\gold.png', sleep_block=sleep,
                           sleep_now=sleep_now, without=without, without_now=without_now, is_dekor=is_dekor))
            elif 'rainbow_block' == object:
                self.blocks_on_level_list.append(
                    Rainbow_blocks(int(x_cor), int(y_cor), sleep_block=sleep, sleep_now=sleep_now, without=without,
                                   without_now=without_now, is_dekor=is_dekor))
            elif 'cook' == object:
                self.item_list.append(Cookies(int(x_cor), int(y_cor)))
            elif 'mega_cook' == object:
                self.item_list.append(Cookies(int(x_cor), int(y_cor), mega_cook=True))
            elif 'final_boss_wall' == object:
                self.blocks_on_level_list.append(
                    Blocks(int(x_cor), int(y_cor), sleep_block=sleep, sleep_now=sleep_now, without=without,
                           without_now=without_now, is_dekor=is_dekor,
                           where_image='images\Blocks\\final_boss_wall.png'))
            elif 'shell' == object:
                self.shell_list.append(Shell(int(x_cor), int(y_cor), is_right=is_right, is_up=is_up))
            elif 'gun' == object:
                self.person_list.append(Gun(int(x_cor), int(y_cor), speed_atack=speed_atack, position=position))
            elif 'esh' == object:
                self.person_list.append(Enemy(x=int(x_cor), y=int(y_cor), how_much_go_right=int(dop[0]) if dop else 30,
                                              how_much_go_left=int(dop[0]) if dop else 30,
                                              hp=800 if self.level_number != '19' else 1))
            elif 'spike' == object:
                self.blocks_on_level_list.append(Spikes(x=int(x_cor), y=int(y_cor)))
            elif 'squirrel' == object:
                self.person_list.append(Squirrel(x=int(x_cor), y=int(y_cor), main_hero=self.main_hero,
                                                 how_much_go_right=how_much_go if how_much_go else 40,
                                                 how_much_go_left=how_much_go if how_much_go else 40,
                                                 is_go_right=is_go_right))
            elif 'Homa' == object:
                self.main_hero = Homa(int(x_cor), int(y_cor), complexity=self.complexiry)
            elif 'boss_1' == object:
                self.boss = Boss(x=int(x_cor), y=int(y_cor))
            elif 'person_boss_1' == object:
                self.person_list.append(Boss(x=int(x_cor), y=int(y_cor)))
        if self.main_hero == None:
            self.main_hero = Homa(300, 300, complexity=self.complexiry)
            for person in self.person_list:
                try:
                    person.set_hero(self.main_hero)
                except:
                    pass
        self.okr = 40  # удалить

    def draw(self, window):
        '''Рисование объектов уровня(всё кроме кнопки выхода с уровня и фона)'''
        if self.level_number != '17':
            for item in self.item_list:
                item.draw(window)
        self.main_hero.draw(window)
        for block in self.blocks_on_level_list:
            block.draw(window)
        for person in self.person_list:
            if person.is_dead == False:
                person.draw(window)
        for magic in self.magic_list + self.shell_list:
            magic.draw(window)
            magic.move()
        self.main_hero.draw_info(window)
        if self.boss:
            self.boss.draw(window)
        if self.image_text:
            window.blit(self.image_text, (600, 10))

    def control_main_hero(self, keys):
        for key in keys:
            if key == "l":
                self.main_hero.go_left()
            elif key == 'r':
                self.main_hero.go_right()
            elif key == 'j':
                self.main_hero.jump_start()
            elif key == 't':
                self.main_hero.teleportation()
            elif key == 'h':
                self.main_hero.hill()
            elif key == 'm':
                magic = self.main_hero.do_magic()
                if magic:
                    self.magic_list.append(magic)
        self.main_hero.give_object_list(self.blocks_on_level_list + self.person_list + self.item_list + [
            self.boss if self.boss else None] + self.shell_list)
        self.main_hero.fall()
        self.main_hero.jump()

        # уникальное поведение при замерщении определенных уровней
        if not self.boss and (self.main_hero.rect.topright[0] > self.level_size[0] or \
                              self.main_hero.rect.topright[1] > self.level_size[1] or \
                              self.main_hero.rect.topright[0] < -20 or self.main_hero.rect.topright[1] < - 20):
            if self.level_number == '17':
                pygame.mixer.music.load(script_dir + 'music\Terraria_Music.mp3')
                pygame.mixer.music.play(-1)
                self.close_level()
                self.__init__(level_number='161', complexity=self.complexiry)
                self.image_text = pygame.font.SysFont('arial', 36).render('Легкая битва', 1, (0, 255, 0))
            elif self.level_number == '205':
                self.close_level()
                self.__init__(level_number='0', complexity=self.complexiry)
                for i in range(5):
                    self.person_list.append(Homa(200, 200 + 100 * i))
                    self.person_list[i].enemy_move = lambda: 0
                    self.person_list[i].change_hp = lambda x: 0
                self.main_hero.move(550, 200)
                self.image_text = pygame.font.SysFont('arial', 36).render('Конец.', 1, (0, 255, 0))
            elif self.level_number == '204':
                self.close_level()
                self.__init__(level_number='205', complexity=self.complexiry)
            elif self.level_number == '203':
                self.close_level()
                self.__init__(level_number='204', complexity=self.complexiry)
                pygame.mixer.music.load(script_dir + 'music\in_level_music.mp3')
                pygame.mixer.music.play(-1)
                self.item_list.append(Watermelon(420, 160))
            elif self.level_number == '202':
                self.close_level()
                self.__init__(level_number='203', complexity=self.complexiry)
            elif self.level_number == '201':
                self.close_level()
                self.__init__(level_number='202', complexity=self.complexiry)
                self.image_text = pygame.font.SysFont('arial', 36).render('Финальный босс!', 1, (0, 255, 0))
                pygame.mixer.music.load(script_dir + 'music\Terraria_Music_2.mp3')
                self.boss = Boss2(500, 500)
                self.boss.main_hero = self.main_hero
                pygame.mixer.music.play(-1)
            elif self.level_number == '20':
                self.close_level()
                self.__init__(level_number='201', complexity=self.complexiry)
                self.image_text = pygame.font.SysFont('arial', 36).render('Мирные ёжики', 1, (0, 255, 0))
            else:
                self.main_hero.change_cook_count(int(self.level_number) * 2)
                self.close_level()
                if int(self.level_number) + 1 > int(self.main_hero.skills[-1]):
                    self.main_hero.skills[-1] = str(int(self.level_number) + 1)
                return True
        if self.main_hero.is_dead:
            self.close_level()
            return True

    def others_persons(self):
        self.magic_in_blocks()
        if not self.boss:
            all_dead = True
        else:
            all_dead = False
        for person in self.person_list:
            if not person.is_dead:
                person.give_object_list([i for i in self.blocks_on_level_list if not i.sleep_now] + self.item_list + [
                    self.main_hero] + self.magic_list)
                object = person.enemy_move()
                if self and object:
                    self.shell_list.append(object)
                person.fall()
                all_dead = False
            else:
                if person.do_heart:
                    if random.randrange(0, 2):
                        self.item_list.append(Hearts(*person.rect.topright))
                    else:
                        self.item_list.append(Cookies(*person.rect.topright))
                    person.do_heart = False
        if all_dead and self.person_list:
            for block in self.blocks_on_level_list:
                block.enemy_disappear()
            self.person_list.clear()
            if self.level_number == '203':
                self.person_list.append(Homa(x=800, y=-100, speed=5))
        if self.boss:
            self.boss.give_object_list([i for i in self.blocks_on_level_list if not i.sleep_now] + self.item_list + [
                self.main_hero] + self.magic_list)
            if self.boss.enemy_move():
                for i in range(random.randrange(2, 5)):
                    self.person_list.append(Enemy(x=random.randrange(200, 700), y=random.randrange(50, 800) - 900,
                                                  speed=random.randrange(3, 6), hp=random.randrange(400, 800)))
                for _ in range(random.randrange(0, 4)):
                    sq = Squirrel(x=random.randrange(200, 700), y=random.randrange(50, 800) - 900,
                                  speed=random.randrange(4, 6), hp=random.randrange(600, 1000))
                    sq.set_hero(self.main_hero)
                    self.person_list.append(sq)
                if self.boss.type == 'f':
                    gun = Gun(x=random.randrange(100, 700), y=random.randrange(50, 800) - 1200, speed_atack=5,
                              position=random.randrange(0, 4))
                    self.person_list.append(gun)
            if self.boss.type == 'f':
                boss_magic = self.boss.do_magic()
                if boss_magic:
                    self.shell_list.append(boss_magic)

            self.boss.fall()

    def magic_in_blocks(self):
        for block in self.blocks_on_level_list:
            for n, magic in enumerate(self.magic_list):
                if magic.rect.colliderect(block.rect) and block.sleep_now == False and (
                        block.type == 'bush' or (block.type != 'spike' and block)):
                    magic.end = True
                if magic.end == True:
                    self.magic_list.pop(n)
            for n, magic in enumerate(self.shell_list):
                if magic.rect.colliderect(block.rect) and block.sleep_now == False and (
                        block.type == 'bush' or (block.type != 'spike' and block)):
                    magic.end = True
                if magic.end == True:
                    self.shell_list.pop(n)

    def check_items(self, hero):
        for item in self.item_list:
            item.in_hero(hero)

    def close_level(self):
        if self.level_number != '161':
            self.main_hero.end_level()
        else:
            self.level_number = '17'
            self.main_hero.end_level()
