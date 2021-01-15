from pygame import image, Rect, sprite
import time
from script_dir import script_dir

# Я решил, что удобнее будет передавить при инициализации блока путь к файлу, а по пути уже
# Определять какое изображение нужно загрузить
blocks_image_list = {'images\Blocks\stone_wall.png': image.load(script_dir + 'images\Blocks\stone_wall.png'),
                     'images\Blocks\dirt.png': image.load(script_dir + 'images\Blocks\dirt.png'),
                     'images\Blocks\\board.png': image.load(script_dir + 'images\Blocks\\board.png'),
                     'images\dekor\Bush.png': image.load(script_dir + 'images\dekor\Bush.png'),
                     'images\Blocks\gold.png': image.load(script_dir + 'images\Blocks\gold.png'),
                     'images\Blocks\\final_boss_wall.png': image.load(
                         script_dir + 'images\Blocks\\final_boss_wall.png'),
                     'images\Blocks\spike.png': image.load(script_dir + 'images\Blocks\spike.png'),
                     'images\Blocks\\rainbow_block\sprite_00.png':
                         image.load(script_dir + 'images\Blocks\\rainbow_block\sprite_00.png')}


class Blocks(sprite.Sprite):
    '''Класс реализует поведение обычного блока.
    Под обычным поведением подрузамевается отрисовка, столкновения,
     появление исчезнавение при убийстве всех врагов или при проходении промежутка времени'''
    empty_image = image.load(script_dir + 'images//empty_image.png')  # нужно, когда блок исчезает

    def __init__(self, x, y, where_image='images\Blocks\dirt.png', sleep_block=False, sleep_now=False, without=False,
                 without_now=False, is_dekor=False, group=None):
        '''Инициализирует блок и его характеристики'''
        if where_image in blocks_image_list:
            self.image = blocks_image_list[where_image]
        else:
            raise ValueError('Не корректно задан путь к файлу с изображением')
        self.start_image = self.image.copy()
        self.x_cor = x
        self.y_cor = y
        self.is_dekor = is_dekor
        self.rect = self.image.get_rect()
        width, height = self.rect.bottomright
        self.rect = Rect((x - width, y), (width, height))
        self.type = 'block'
        self.sleep_block = sleep_block
        self.sleep_now = sleep_now
        self.sleep_time = 0
        self.without = without
        if without_now:
            self.sleep_now = True
        super().__init__(group)

    def __str__(self):
        return f'Простой блок с координатами {self.x_cor, self.y_cor}. Без особых свойств.'

    def update(self, *args, **kwargs) -> None:
        '''Обработка пропажи появления блока'''
        if self.sleep_block:
            self.time_disappear()
        if self.sleep_block or self.without:
            if not self.sleep_now:
                self.image = self.start_image
            else:
                self.image = self.empty_image

    def unique_properties(self, hero):
        '''Необычное поведение при столкновении с другим объектом.'''
        pass

    def set_sleep_time(self):
        '''Устанавливает времяисчезновения (для таймера), если блок исчезающий'''
        self.sleep_time = time.time()

    def time_disappear(self):
        '''Проверка, должен ли блок появится/исчезнуть по времени'''
        if time.time() - self.sleep_time > 3:
            if self.sleep_block:
                self.sleep_now = not self.sleep_now
                self.set_sleep_time()

    def enemy_disappear(self):
        '''Проверка, должен ли блок появится/исчезнуть когда все враги убиты'''
        if self.without:
            self.sleep_now = not self.sleep_now

    def __bool__(self):
        '''Возвращает, исчез ли блок сейчас'''
        return False if (self.sleep_now or self.is_dekor) else True


class Dekor(Blocks):
    '''Реализует блок сквозь который проходят персонажи, но не проходят снаряды'''
    def __init__(self, x, y, where_image, sleep_block, sleep_now, without, without_now, is_dekor, group):
        Blocks.__init__(self, x, y, where_image, sleep_block, sleep_now, without, without_now, group=group)
        self.is_dekor = True
        self.type = 'bush'

    def __bool__(self):
        return False  # всегда


class Rainbow_blocks(Blocks):
    '''Блок с анимацией'''
    where_image_list = [f'{script_dir}images\Blocks\\rainbow_block\sprite_{i if i >= 10 else "0" + str(i)}.png'
                        for i in
                        range(18)]

    def __init__(self, x, y, sleep_block=False, sleep_now=False, without=False, without_now=False, is_dekor=False,
                 group=None):
        Blocks.__init__(self, x, y, where_image='images\Blocks\\rainbow_block\sprite_00.png', sleep_block=sleep_block,
                        sleep_now=sleep_now, without=without, without_now=without_now, is_dekor=is_dekor, group=group)
        self.image_list = [image.load(im) for im in self.where_image_list]
        self.image_count = 0
        self.max_count = 17

    def update(self):
        if not self.sleep_now:
            self.image = self.image_list[self.image_count]
            self.image_count += 1
            if self.image_count > self.max_count:
                self.image_count = 0
        else:
            self.image = self.empty_image
