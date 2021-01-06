from script_dir import script_dir


def check_settings():
    def do_settings_file():
        normal_string = ['273', '276', '275', '274', '49', '50', '51', '2']
        with open(script_dir + 'settings.txt', 'w') as file:
            file.write('\n'.join(normal_string))

    try:
        with open(script_dir + 'settings.txt') as file:
            strings = file.read().split('\n')
            print(strings)
        if len(strings) != 8:
            print(1)
            do_settings_file()
        else:
            try:
                for i in strings:
                    int(i)
            except:
                print(2)
                do_settings_file()
    except:
        print(3)
        do_settings_file()


def check_main_hero():
    def do_main_hero_file():
        normal_string = ['0', '80', '0', '0', '0', '-1']
        with open(script_dir + 'images\main_hero\main_hero_info.txt', 'w') as file:
            file.write('\n'.join(normal_string))

    try:
        with open(script_dir + 'images\main_hero\main_hero_info.txt') as file:
            strings = file.read().split('\n')
        if len(strings) != 6:
            do_main_hero_file()
        else:
            try:
                for i in strings:
                    if 0 < int(i) >= 10000000000:
                        do_main_hero_file()
            except:
                do_main_hero_file()
    except:
        do_main_hero_file()


check_settings()
check_main_hero()