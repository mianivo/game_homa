from pygame import image, Rect, sprite
import time
from script_dir import script_dir


class Person(sprite.Sprite):
    def __init__(self, x, y, image_list_left, image_list_right, speed=5, hp=None, name='', group=None):
        self.image_list_right = [image.load(script_dir + im) for im in
                                 image_list_right]  # Загружаем изображения по указаным путям
        self.image_list_left = [image.load(script_dir + im) for im in image_list_left]
        self.anim_count = 0
        self.how_much_animations = len(self.image_list_right)
        self.image = self.image_list_right[0]

        self.rect = self.image_list_right[0].get_rect()
        width, height = self.rect.bottomright
        self.rect = Rect((x - width, y), (width, height))

        self.is_dead = False
        self.is_go_right = True
        self.is_go_left = False
        self.is_fall = True
        self.is_jump = False
        self.can_jump = False

        self.name = name

        self.speed = speed

        self.hp = hp
        self.damage = 0
        self.person_rect_list = []
        self.time = 0
        self.object_list = []

        self.cook_count = 0
        self.get_damage = False

        super().__init__(group)


    def __str__(self):
        return f'Персонаж - {self.name}. Координаты: {self.rect.x, self.rect.y}.' \
               f' Здоровье {self.hp}. Урон {self.damage}.'

    def set_time(self):
        '''Запоминает время получения урона'''
        self.time = time.time()

    def check_time(self):
        '''Проверяет, прошло ли время неуязвимости после получения урона или нет.'''
        return time.time() - self.time > 0.4

    def move(self, x=0, y=0):
        '''Общая функция перемещения персонажей.
         Возвращает True, если персонаж при перемещении вошел в какой-либо блок.'''
        self.change_animation()
        self.rect = self.rect.move(x, y)
        return self.in_other_rect(x, y)

    def give_object_list(self, object_list):
        '''Получает список объектов. ОБъекты всё, с чем на уровне взоимодействует персонаж.'''
        self.object_list = object_list

    def go_left(self):
        self.is_go_left = True
        self.is_go_right = False
        self.move(x=-self.speed)

    def go_right(self):
        self.is_go_left = False
        self.is_go_right = True
        self.move(x=self.speed)

    def enemy_move(self):
        '''Правила перемещения врагов, у всех разный метод.'''

    def change_hp(self, how_much):
        '''Меняет здоровье на значение. Значение не приводится к отрицательному или положительному числу.'''

        self.get_damage = True
        if how_much < 0:  # Временная неуязвимость при уроне
            if self.check_time():
                self.hp += how_much
                self.dead()
                self.set_time()
        else:
            self.hp += how_much

    def dead(self):
        if self.hp <= 0:
            self.is_dead = True

    def fall(self):
        '''Падение персонажа. ПЕрсонаж падает всегда когда не прыгает
        (если на блоке, то его возвращает на местin_other_rect'''
        if not self.is_jump or not self.can_jump:
            if not self.move(y=self.speed * 3):
                self.can_jump = False
            else:
                self.can_jump = True
                self.is_fall = False
        else:
            self.is_fall = False

    def change_animation(self):
        '''Меняет анимации при перемещении.'''
        self.anim_count += 1
        if self.anim_count >= self.how_much_animations:
            self.anim_count = 0
        if self.is_go_right:
            self.image = self.image_list_right[self.anim_count]
        elif self.is_go_left:
            self.image = self.image_list_left[self.anim_count]

    def draw(self, window):
        window.blit(self.image, (self.rect.topright))

    def in_other_rect(self, x=0, y=0):
        '''Если прерсонаж пападет в блок, выталкивает его, причем не всегда в первоначальное положение.
         Сторона выталкивания зависит от стороны движения персонажа. НЕ ВЫТАЛКИВАЕТ ПЕРСОНАЖА,
         ЕСЛИ в методе взоимодействия объекта с персонажам указано не выталкивать персоенажа.'''
        answer = []
        for object in self.object_list:
            if object:  # если не мертв(для персонажей), или активен (для блоков) возвращает True.
                if self.rect.colliderect(object.rect) and self.rect != object.rect:
                    if not object.unique_properties(
                            self):  # мы должны получит True если блок сам уникально меняет координаты персонажа
                        if y < 0:
                            _, rect_y = object.rect.bottomright
                            self.rect = Rect((self.rect.x, rect_y), (self.rect.width, self.rect.height))
                            answer.append('u')
                        elif y > 0:
                            self.can_jump = True
                            _, rect_y = object.rect.topright
                            self.rect = Rect((self.rect.x, rect_y - self.rect.height),
                                             (self.rect.width, self.rect.height))
                            answer.append('d')
                        elif x < 0 and object.type != 'enemy':
                            rect_x, _ = object.rect.bottomright
                            self.rect = Rect((object.rect.x + self.rect.width, self.rect.y),
                                             (self.rect.width, self.rect.height))
                            answer.append('l')
                        elif x > 0 and object.type != 'enemy':
                            rect_x, _ = object.rect.topleft
                            self.rect = Rect((object.rect.x - self.rect.width, self.rect.y),
                                             (self.rect.width, self.rect.height))
                            answer.append('r')
        return answer

    def change_cook_count(self, how_much=1):
        self.cook_count += how_much

    def unique_properties(self, hero):
        '''Уникальное взоимодействие с персонажами. Некий абстрактный метод,
         который может быть реализован или не реализован в дочерних классах'''
        return True
