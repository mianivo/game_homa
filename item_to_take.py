import pygame
from script_dir import script_dir


class Items:
    '''Предметы для подбора.'''
    def __init__(self, x, y, where_image):
        self.image = pygame.image.load(script_dir + where_image)
        self.rect = self.image.get_rect()
        width, height = self.rect.bottomright
        self.rect = pygame.Rect((x - width, y), (width, height))
        self.was_put = False
        self.type = 'item'

    def draw(self, window):
        if not self.was_put:
            window.blit(self.image, self.rect.topright)


    def unique_properties(self, hero):
        if not self.was_put:
            self.was_put = True

    def __bool__(self):
        return not self.was_put


class Cookies(Items):
    def __init__(self, x, y, mega_cook=False):
        '''Печенька. При подборе увеличивает кол-во печенек'''
        Items.__init__(self, x, y, where_image='images\items_to_take\Cook.png')
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
    def __init__(self, x, y):
        '''Сердце. При подборе увеличивает кол-во хп'''
        Items.__init__(self, x, y, where_image='images\items_to_take\Heart.png')

    def unique_properties(self, hero):
        if not self.was_put:
            Items.unique_properties(self, hero)
            hero.change_hp(150)
            return True

class Watermelon(Items):
    def __init__(self, x, y):
        '''Иникальный предмет для 20-го уровня уровня.'''
        Items.__init__(self, x, y, where_image='images\items_to_take\watermelon.png')

    def unique_properties(self, hero):
        if not self.was_put:
            Items.unique_properties(self, hero)
            hero.change_hp(100)
            hero.change_xp(2000)
            hero.change_cook_count(2000)
            return True

    def draw(self, window):
        if not self.was_put:
            window.blit(self.image, (self.rect.topright[0] - 60, self.rect.topright[1]))