import os
import tkinter as tk

window = tk.Tk('400x250')
window.title('Ошибка! Не найден файл!')


def check_files():
    '''Проверяет файлы изображений, уровней и т.д.'''
    answer = []

    def check_dir(dirr, must_be=[]):
        must_be_in_dir = must_be
        try:
            if dirr:
                in_dir_list = os.listdir(dirr)
            else:
                in_dir_list = os.listdir()
        except:
            answer.append(f'Не найдена папка {dirr}')
            return
        for i in must_be_in_dir:
            if i not in in_dir_list:
                answer.append(f' Не найден файл {i}, в папке, {dirr}. ')

    check_dir('', ['images', 'music', 'levels'])
    check_dir('images',
              ['bg', 'Blocks', 'Buttons', 'dekor', 'enemys', 'esh_king', 'gun', 'items_to_take', 'magic', 'main_hero',
               'shell', 'final_boss'])
    check_dir('levels', ['level0.txt', 'level1.txt', 'level10.txt', 'level11.txt', 'level12.txt', 'level13.txt',
                         'level14.txt', 'level15.txt', 'level16.txt', 'level17.txt', 'level18.txt', 'level19.txt',
                         'level2.txt', 'level20.txt', 'level21.txt', 'level22.txt', 'level3.txt', 'level4.txt',
                         'level5.txt', 'level6.txt', 'level7.txt', 'level8.txt', 'level9.txt', 'level201.txt',
                         'level202.txt', 'level203.txt', 'level204.txt', 'level205.txt'])
    check_dir('music', ['in_level_music.mp3', 'in_menu_music.mp3', 'Terraria_Music.mp3', 'Terraria_Music_2.mp3'])
    check_dir('images\\bg', ['Bg.png'])
    check_dir('images\\Blocks', ['board.png', 'dirt.png', 'gold.png', 'rainbow_block', 'spike.png', 'stone_wall.png',
                                 'final_boss_wall.png'])
    check_dir('images\\Buttons',
              ['easy_button.png', 'easy_button_on.png', 'For_text.png', 'hard_button.png', 'hard_button_on.png',
               'in_level.png', 'in_level_on.png', 'level_button.png', 'level_button_on.png', 'long_button.png',
               'long_button_on.png', 'medium_button.png', 'medium_button_on.png', 'music_button.png',
               'music_button_on.png'])
    check_dir('images\\dekor', ['Bush.png'])
    check_dir('images\\enemys', ['esh', 'squirrel'])
    check_dir('images\\final_boss\\',
              ['final_boss_left_1.png', 'final_boss_left_2.png', 'final_boss_left_3.png', 'final_boss_right_1.png',
               'final_boss_right_2.png', 'final_boss_right_3.png'])
    check_dir('images\\enemys\esh', ['left1.png', 'left2.png', 'left3.png', 'Right1.png', 'Right2.png', 'Right3.png'])
    check_dir('images\\enemys\squirrel',
              ['left0.png', 'left1.png', 'left2.png', 'right0.png', 'right1.png', 'right2.png'])
    check_dir('images\\esh_king', ['left0.png', 'left1.png', 'left2.png', 'right0.png', 'right1.png', 'right2.png'])
    check_dir('images\\items_to_take', ['Cook.png', 'Heart.png', 'watermelon.png'])
    check_dir('images\\gun', ['gun0.png', 'gun1.png', 'gun2.png', 'gun3.png', 'wheel.png'])
    check_dir('images\\shell', ['shell.png', 'shell_dekor.png'])
    check_dir('images\\magic',
              ['magic_1.png', 'magic_2.png', 'magic_3.png', 'magic_4.png', 'magic_dekor_1.png', 'boss_magic_1.png',
               'boss_magic_2.png', 'boss_magic_3.png', 'boss_magic_4.png', 'boss_magic_dekor.png', ])
    check_dir('images\\main_hero', ['Left0.png', 'Left1.png', 'Left2.png', 'Right0.png', 'Right1.png', 'Right2.png'])
    lbl = tk.Label(window, text='\n'.join(answer))
    lbl.grid(column=0, row=0)


check_files()
window.mainloop()
