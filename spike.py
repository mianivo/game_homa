from blocks import Blocks


class Spikes(Blocks):
    def __init__(self, x, y):
        Blocks.__init__(self, x, y, where_image='images\Blocks\spike.png')
        self.type = 'spike'

    def unique_properties(self, hero):
        if hero.can_jump == False and hero.is_jump == False and self.rect.bottomleft[1] > hero.rect.bottomleft[1]:
            hero.is_dead = True
        return True

    def __str__(self):
        return f'Блок шипов с координатами {self.x_cor, self.y_cor}. Любой кто падает на него сверху мгновенно умирает.'
