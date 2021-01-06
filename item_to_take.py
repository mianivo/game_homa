import pygame
from script_dir import script_dir


class Items(pygame.sprite.Sprite):
    '''Предметы для подбора.'''

    def __init__(self, x, y, where_image, group=None):
        self.image = pygame.image.load(script_dir + where_image)
        self.rect = self.image.get_rect()
        width, height = self.rect.bottomright
        self.rect = pygame.Rect((x - width, y), (width, height))
        self.was_put = False
        self.type = 'item'
        super(Items, self).__init__(group)

    def draw(self, window):
        if not self.was_put:
            window.blit(self.image, self.rect.topright)

    def unique_properties(self, hero):
        if not self.was_put:
            self.was_put = True
            self.groups()[0].remove(self)

    def __bool__(self):
        return not self.was_put


class Cookies(Items):
    def __init__(self, x, y, mega_cook=False, group=None):
        '''Печенька. При подборе увеличивает кол-во печенек'''
        Items.__init__(self, x, y, where_image='images\items_to_take\Cook.png', group=group)
        self.mega_cook = mega_cook

    def unique_properties(self, hero):
        if not self.was_put:
            Items.unique_properties(self, hero)
            if not self.mega_cook:
                hero.change_cook_count()
            else:
                hero.change_cook_count(150)
            return True


class Hearts(Items):
    def __init__(self, x, y, group=None):
        '''Сердце. При подборе увеличивает кол-во хп'''
        Items.__init__(self, x, y, where_image='images\items_to_take\Heart.png', group=group)

    def unique_properties(self, hero):
        if not self.was_put:
            Items.unique_properties(self, hero)
            hero.change_hp(150)
            return True


class Watermelon(Items):
    def __init__(self, x, y, group=None):
        '''Иникальный предмет для 20-го уровня уровня.'''
        Items.__init__(self, x, y, where_image='images\items_to_take\watermelon.png', group=group)

    def unique_properties(self, hero):
        if not self.was_put:
            Items.unique_properties(self, hero)
            hero.change_hp(100)
            hero.change_xp(2000)
            hero.change_cook_count(2000)
            return True
