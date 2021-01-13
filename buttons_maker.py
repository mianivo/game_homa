import pygame
from menu import Buttons, Label, Menu, MenuSection, ComplextyButton
from script_dir import script_dir
from buttons_commands import *

with open(script_dir + 'settings.txt') as file:
    dict_chars = {1073741906: 'Ве', 1073741905: 'Ни', 1073741903: 'Пр', 1073741904: 'Ле'}
    strings = file.read().split('\n')
    jump, left, right, down, magic, hill, tp, complexty = [dict_chars[int(i)] if int(i) in
                                                                                 dict_chars else chr(
        int(i)) if n < 7 else i for n, i in enumerate(strings)]
    complexty = int(strings[-1])


def create_menu_information(information_list, x_cor=260):
    labels_list = []
    for n, text in enumerate(information_list):
        labels_list.append(
            Label(x_cor=x_cor,
                  y_cor=30 + 25 * n,
                  text=text,
                  text_color=(255, 255, 0), text_size=28))
    return labels_list


def create_back_button(sprite_group):
    back_button = Buttons(x_cor=450, y_cor=520,  # переход главное меню
                          image='images\Buttons\long_button.png',
                          image_on='images\Buttons\long_button_on.png', text='В главное меню',
                          command=back_button_command, group=sprite_group)
    return back_button


def create_main_menu_buttons():
    main_menu = MenuSection('main_menu')
    button_sprite_group = main_menu.get_sprite_group()

    start_button = Buttons(x_cor=250, y_cor=60,  # переход к показу списка уровней
                           image='images\Buttons\long_button.png',
                           image_on='images\Buttons\long_button_on.png',
                           text='Начать игру',
                           command=start_button_command, group=button_sprite_group)
    settings_button = Buttons(x_cor=250, y_cor=180,  # переход к настройкам
                              image='images\Buttons\long_button.png',
                              image_on='images\Buttons\long_button_on.png', text='Настройки'
                              , command=settings_button_command, group=button_sprite_group)
    information_button = Buttons(x_cor=250, y_cor=300,  # переход к меню информации (сведения об игре)
                                 image='images\Buttons\long_button.png',
                                 image_on='images\Buttons\long_button_on.png', text='Информация',
                                 command=information_button_command, group=button_sprite_group)
    exit_button = Buttons(x_cor=250, y_cor=420,  # выход из игры
                          image='images\Buttons\long_button.png',
                          image_on='images\Buttons\long_button_on.png', text='Выход',
                          command=quit_button_command, group=button_sprite_group)

    version_label = Label(x_cor=60, y_cor=10, text='Версия 1.1')
    for i in [start_button, settings_button, information_button, exit_button]:
        main_menu.add_button(i)
    main_menu.add_label(version_label)
    return main_menu


def crete_levels_section():
    levels_menu = MenuSection('levels')
    button_sprite_group = levels_menu.get_sprite_group()
    levels_menu.add_button(create_back_button(button_sprite_group))

    levels_button_list = []
    for i in range(10):
        for j in range(3):
            if i + j * 10 <= 22:
                levels_button_list.append(
                    Buttons(x_cor=10 + 80 * i,
                            y_cor=90 + 80 * j,
                            image='images\Buttons\\' + ('close_' if int(
                                about_hero_info_list[-1]) < i + j * 10 - 1 else '') + 'level_button.png',
                            image_on='images\Buttons\\' + ('close_' if int(
                                about_hero_info_list[-1]) < i + j * 10 - 1 else '') + 'level_button_on.png',
                            text=str(i + j * 10),
                            command=None if int(about_hero_info_list[-1]) < i + j * 10 - 1 else levels_command,
                            group=button_sprite_group))
    levels_labels_list = create_menu_information(['Лучше проходить уровни попорядку, не пропуская их.',
                                                  'Прохождение одного уровня, откроет два следующих.'], x_cor=260)
    for i in levels_button_list:
        levels_menu.add_button(i)
    for i in levels_labels_list:
        levels_menu.add_label(i)
    return levels_menu


def create_level_button():
    into_level_menu = MenuSection('into_level')
    button_sprite_group = into_level_menu.get_sprite_group()
    bt = Buttons(x_cor=960, y_cor=0,
                 image='images\Buttons\in_level.png',
                 image_on='images\Buttons\in_level_on.png', text=' ',
                 command=into_level_command, group=button_sprite_group)
    into_level_menu.add_button(bt)
    return into_level_menu


def crete_settings_section():
    settings_menu = MenuSection('settings')
    button_sprite_group = settings_menu.get_sprite_group()
    label_list = []

    label_list.extend(
        create_menu_information(['                                                                    Музыка:',
                                 'Выбор сложности:                                                                                  ']))
    label_list.extend(create_menu_information(['', '', 'Кнопки:', '', 'Прыжок', '', 'Влево', '', 'Вправо', '', 'Вниз']))
    label_list.extend(
        create_menu_information(['', '', '', '', 'Маг. атака', '', 'Лечение', '', 'Телепортация'], x_cor=400))

    music_button = Buttons(x_cor=680, y_cor=10,  # включение/выключение музыки
                           image='images\Buttons\music_button.png',
                           image_on='images\Buttons\music_button_on.png',
                           text='', command=music_command, group=button_sprite_group)

    global complexty
    complexty = ComplextyButton(x_cor=50, y_cor=400,
                                image='images\Buttons\easy_button.png' if complexty == 0 else
                                'images\Buttons\medium_button.png' if complexty == 1 else 'images\Buttons\hard_button.png',
                                image_on='images\Buttons\easy_button.png' if complexty == 0 else
                                'images\Buttons\medium_button.png' if complexty == 1 else 'images\Buttons\hard_button.png',
                                text='Сейчас', group=button_sprite_group)

    set_easy = ChangeComplextyCommand(complexty, 7, 0)
    set_medium = ChangeComplextyCommand(complexty, 7, 1)
    set_hard = ChangeComplextyCommand(complexty, 7, 2)

    easy = Buttons(x_cor=50, y_cor=100,  # включение/выключение музыки
                   image='images\Buttons\easy_button.png',
                   image_on='images\Buttons\easy_button_on.png', text='Легкая', command=set_easy,
                   group=button_sprite_group)
    medium = Buttons(x_cor=50, y_cor=200,  # включение/выключение музыки
                     image='images\Buttons\medium_button.png',
                     image_on='images\Buttons\medium_button_on.png', text='Средняя', command=set_medium,
                     group=button_sprite_group)
    hard = Buttons(x_cor=50, y_cor=300,  # включение/выключение музыки
                   image='images\Buttons\hard_button.png',
                   image_on='images\Buttons\hard_button_on.png', text='Тяжелая', command=set_hard,
                   group=button_sprite_group)

    set_go_right_button = Buttons(x_cor=450, y_cor=310,  # включение/выключение музыки
                                  image='images\Buttons\level_button.png',
                                  image_on='images\Buttons\level_button_on.png', text=right, group=button_sprite_group,
                                  command=set_right_key)

    set_go_left_button = Buttons(x_cor=450, y_cor=230,  # включение/выключение музыки
                                 image='images\Buttons\level_button.png',
                                 image_on='images\Buttons\level_button_on.png', text=left, group=button_sprite_group,
                                 command=set_left_key)

    set_jump_button = Buttons(x_cor=450, y_cor=150,  # включение/выключение музыки
                              image='images\Buttons\level_button.png',
                              image_on='images\Buttons\level_button_on.png', text=jump, group=button_sprite_group,
                              command=set_jump_key)

    set_go_down_button = Buttons(x_cor=450, y_cor=390,  # включение/выключение музыки
                                 image='images\Buttons\level_button.png',
                                 image_on='images\Buttons\level_button_on.png', text=down, group=button_sprite_group,
                                 command=set_down_key)

    set_magic = Buttons(x_cor=700, y_cor=150,  # включение/выключение музыки
                        image='images\Buttons\level_button.png',
                        image_on='images\Buttons\level_button_on.png', text=magic, group=button_sprite_group,
                        command=set_magic_key)

    set_tp = Buttons(x_cor=700, y_cor=310,  # включение/выключение музыки
                     image='images\Buttons\level_button.png',
                     image_on='images\Buttons\level_button_on.png', text=tp, group=button_sprite_group,
                     command=set_tp_key)

    set_hill = Buttons(x_cor=700, y_cor=230,  # включение/выключение музыки
                       image='images\Buttons\level_button.png',
                       image_on='images\Buttons\level_button_on.png', text=hill, group=button_sprite_group,
                       command=set_hill_key)

    del_game_progress = Buttons(x_cor=50, y_cor=520,  # Стирает инфоррмацию об персонеаже
                                image='images\Buttons\long_button.png',
                                image_on='images\Buttons\long_button_on.png', text='Стереть прогресс',
                                command=ask_del_progress, group=button_sprite_group)
    for button in [music_button, easy, medium, hard, complexty, set_go_right_button,
                   set_go_left_button, set_jump_button, set_go_down_button,
                   set_magic, set_tp, set_hill, del_game_progress]:
        settings_menu.add_button(button)
    for label in label_list:
        settings_menu.add_label(label)
    settings_menu.add_button(create_back_button(button_sprite_group))
    return settings_menu


def create_ask_del_game_progress_buttons():
    settings_menu = MenuSection('ask_del_progress')
    button_sprite_group = settings_menu.get_sprite_group()
    label_list = []

    del_game_progress = Buttons(x_cor=250, y_cor=100,  # Стирает инфоррмацию об персонеаже
                                image='images\Buttons\long_button.png',
                                image_on='images\Buttons\long_button_on.png', text='Подтвердить',
                                command=del_progress, group=button_sprite_group)
    label_list.extend(create_menu_information(
        ['Нажав кнопку подтвердить, вы подтверждаете, что', 'хотите УДАЛИТЬ прогресс персонажа БЕЗВОЗВРАТНО.']))
    settings_menu.add_button(del_game_progress)
    settings_menu.add_button(create_back_button(button_sprite_group))
    for label in label_list:
        settings_menu.add_label(label)
    return settings_menu


def create_info_menu():
    information_menu = MenuSection('information')
    button_sprite_group = information_menu.get_sprite_group()
    about_autors_button = Buttons(x_cor=250, y_cor=20,  # переход к меню информации об авторах
                                  image='images\Buttons\long_button.png',
                                  image_on='images\Buttons\long_button_on.png', text='Об авторах',
                                  command=about_autors_button_command,
                                  group=button_sprite_group)
    about_game_button = Buttons(x_cor=250, y_cor=140,  # переход к меню информации об игре
                                image='images\Buttons\long_button.png',
                                command=about_game_button_command,
                                image_on='images\Buttons\long_button_on.png', text='Об игре', group=button_sprite_group)
    about_person_button = Buttons(x_cor=250, y_cor=260,  # переход к меню информации об персонаже
                                  image='images\Buttons\long_button.png',
                                  image_on='images\Buttons\long_button_on.png', text='О персонаже',
                                  command=about_person_button_command,
                                  group=button_sprite_group)
    for button in [about_autors_button, about_game_button, about_person_button]:
        information_menu.add_button(button)
    information_menu.add_button(create_back_button(button_sprite_group))
    return information_menu


def create_about_autors_menu():
    about_autors_menu = MenuSection('about_autors')
    button_sprite_group = about_autors_menu.get_sprite_group()
    label_list = create_menu_information(
        ['Разработчик: Михеев Андрей',
         'Художники: Михеева Александра, Михеев Андрей'])
    for label in label_list:
        about_autors_menu.add_label(label)
    about_autors_menu.add_button(create_back_button(button_sprite_group))
    return about_autors_menu


def create_about_game_menu():
    about_game_menu = MenuSection('about_game')
    button_sprite_group = about_game_menu.get_sprite_group()
    label_list = create_menu_information(
        ['Все знают, что хомячки любят семечки.',
         'Но где много вкусных и больших семечек?',
         'Семечек больше всего в арбузах!'])
    for label in label_list:
        about_game_menu.add_label(label)
    about_game_menu.add_button(create_back_button(button_sprite_group))
    return about_game_menu


def create_about_person_menu():
    about_game_menu = MenuSection('about_person')
    button_sprite_group = about_game_menu.get_sprite_group()
    person_skills = Buttons(x_cor=250, y_cor=260,  # переход к меню информации о способностях персонажа
                            image='images\Buttons\long_button.png',
                            image_on='images\Buttons\long_button_on.png', text='Способности описание',
                            command=about_skills_button_command,
                            text_size=34, group=button_sprite_group)
    # в меню о способностях персонажа
    person_skills_develop = Buttons(x_cor=250, y_cor=380,  # переход в меню открытия способнстей
                                    image='images\Buttons\long_button.png',
                                    image_on='images\Buttons\long_button_on.png',
                                    command=open_skills_button_command,
                                    text='Способности открыть', group=button_sprite_group)
    for button in [person_skills, person_skills_develop, create_back_button(button_sprite_group)]:
        about_game_menu.add_button(button)
    with open(script_dir + 'images\main_hero\main_hero_info.txt') as about_hero_info:
        about_hero_info_list = about_hero_info.read().split('\n')

        label_list = create_menu_information([str(i) + ' ' + str(j) for i, j in zip(['Опыт:',
                                                                                     'Количество печенек:',
                                                                                     'Способность телепорт:',
                                                                                     'Способность лечение:',
                                                                                     'Способность магическая атака:'],
                                                                                    about_hero_info_list[:2] + [
                                                                                        'Разблокировано' if i == '1' else 'Заблокировано'
                                                                                        for i in
                                                                                        about_hero_info_list[2:]])])
    for label in label_list:
        about_game_menu.add_label(label)
    return about_game_menu


def create_about_skills_menu():
    about_game_menu = MenuSection('about_game')
    button_sprite_group = about_game_menu.get_sprite_group()
    label_list = create_menu_information(
        ['Тут приведено описание спсобностей', 'Всего три способности.',
         'Все способности потребляют печеньки, имеют перезарядку.',
         'Телепорт телепортирует(неожидано).',
         ' Ограничение по телепортации, нельзя выйти за пределы уровня.',
         'телопорт потребляет 5 печенек, перезарядка 5 секунд',
         'Лечение мгновенно востанавливает большое количество',
         ' hp. Перезарядка 12. Потребление 34. Используй чаще!',
         'Последнее заклинание выпускает магический снаряд во врага,',
         ' сняряд не проходит сквозь блоки, имеет высокую скорость,',
         'эффективно против боссов. Потребление 2, перезярядка 0.8.',
         'Урон снаряда равен удвоенному урону Хомы!',
         'Некоторые уровни нельзя пройти, не применяя способности!'])
    for label in label_list:
        about_game_menu.add_label(label)
    about_game_menu.add_button(create_back_button(button_sprite_group))
    return about_game_menu


def create_open_skills():
    about_game_menu = MenuSection('open_skills')
    button_sprite_group = about_game_menu.get_sprite_group()
    person_skill_teleportation = Buttons(x_cor=250, y_cor=60,  # Открыть телепорт
                                         image='images\Buttons\long_button.png',
                                         image_on='images\Buttons\long_button_on.png', text='Телепортация',
                                         group=button_sprite_group,
                                         command=open_tp_command)

    person_skill_hill = Buttons(x_cor=250, y_cor=180,  # Открыть лечение
                                image='images\Buttons\long_button.png',
                                image_on='images\Buttons\long_button_on.png', text='Лечение',
                                group=button_sprite_group,
                                command=open_hill_command)
    for button in [person_skill_teleportation, person_skill_hill, create_back_button(button_sprite_group)]:
        about_game_menu.add_button(button)
    labels_list = create_menu_information(
        ['Открыть телепортацию за 300 печенек.', '', '', 'Открыть лечение за 100 печенек.',
         '', '', '', 'Способность магическая атака открывается сама после 6-го уровня'])
    for label in labels_list:
        about_game_menu.add_label(label)
    return about_game_menu
