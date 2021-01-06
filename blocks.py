from pygame import image, Rect, sprite
import time
from script_dir import script_dir


class Blocks(sprite.Sprite):
    empty_image = image.load(script_dir + 'images//empty_image.png')

    def __init__(self, x, y, where_image='images\Blocks\dirt.png', sleep_block=False, sleep_now=False, without=False,
                 without_now=False, is_dekor=False, group=None):
        '''Инициализирует блок и его характеристики'''
        self.image = image.load(script_dir + where_image)
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
        if self.sleep_block:
            if not self.sleep_now:
                self.image = self.start_image
            else:
                self.image = self.empty_image
            self.time_disappear()

    def unique_properties(self, hero):
        pass

    def set_sleep_time(self):
        self.sleep_time = time.time()

    def time_disappear(self):
        if time.time() - self.sleep_time > 3:
            if self.sleep_block:
                self.sleep_now = not self.sleep_now
                self.set_sleep_time()

    def enemy_disappear(self):
        if self.without:
            self.sleep_now = not self.sleep_now

    def __bool__(self):
        return False if (self.sleep_now or self.is_dekor) else True


class Dekor(Blocks):
    def __init__(self, x, y, where_image, sleep_block, sleep_now, without, without_now, is_dekor, group):
        Blocks.__init__(self, x, y, where_image, sleep_block, sleep_now, without, without_now, group=group)
        self.is_dekor = True
        self.type = 'bush'

    def __bool__(self):
        return False  # всегда


class Rainbow_blocks(Blocks):
    def __init__(self, x, y, sleep_block=False, sleep_now=False, without=False, without_now=False, is_dekor=False,
                 group=None):
        Blocks.__init__(self, x, y, where_image='images\Blocks\\rainbow_block\sprite_00.png', sleep_block=sleep_block,
                        sleep_now=sleep_now, without=without, without_now=without_now, is_dekor=is_dekor, group=group)
        self.where_image_list = [f'{script_dir}images\Blocks\\rainbow_block\sprite_{i if i >= 10 else "0" + str(i)}.png'
                                 for i in
                                 range(18)]
        self.image_list = [image.load(im) for im in self.where_image_list]
        self.image_count = 0
        self.max_count = 17

    def change_image(self):
        self.image = self.image_list[self.image_count]
        self.image_count += 1
        if self.image_count > self.max_count:
            self.image_count = 0

    def draw(self, window):
        Blocks.draw(self, window)
        self.change_image()
