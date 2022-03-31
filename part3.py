import os
from functions import *

os.chdir(os.path.dirname(sys.argv[0]))

bd_name = input('Введите имя файла БД для дальнейшей работы (по умолчанию VUZ.sqlite) >>>  ') or 'VUZ.sqlite'  # Ввод имени файла БД
if not os.path.isfile(bd_name):
    print('\n\nНет такого файла!')
    input('\n Завершение работы с программой \n\n Нажмите на любую клавишу, чтобы выйти')
else:
    table_name_kart = input('Введите имя таблицы <Картотека вузов> (по умолчанию vuzkart) >>> ') or 'vuzkart'
    table_name_stat = input('Введите имя таблицы <Статистика вузов> (по умолчанию vuzstat) >>> ') or 'vuzstat'
    is_exit = False
    while not is_exit:
        os.system('cls||clear')
        print("\n Работа с {} \n".format(bd_name))
        choice_menu = menu()
        print('\n')
        if choice_menu == '1':
            os.system('cls||clear')
            table_name = tn_choice(table_name_kart, table_name_stat)
            table_bd(bd_name, table_name)
            input('\n Таблица выведена успешно \n\n Нажмите на любую клавишу для выхода в главное меню')
        elif choice_menu == '2':
            selected_region = select_region()
            name_vuzes = vuz_without_mail(bd_name, table_name_kart, selected_region)
            print('\n')
            if not name_vuzes:
                print('Вузов по заданным параметрам не найдено в таблице')
            else:
                print('Вузы по задданным параметрам : \n')
                for name_vuz in name_vuzes:
                    print(name_vuz)
            input('\n Нажмите на любую клавишу для выхода в главное меню')

        elif choice_menu == '3':
            raspred_stud(bd_name, table_name_kart, table_name_stat)
            input('\n Таблица выведена успешно \n\n Нажмите на любую клавишу для выхода в главное меню')
        elif choice_menu == '4':
            os.system('cls||clear')
            input('\n Завершение работы с программой \n\n Нажмите на любую клавишу, чтобы выйти')
            is_exit = True
        else:
            print('\n\n Ошибка ввода')
            input('\n Завершение работы с программой \n\n Нажмите на любую клавишу, чтобы выйти')
            is_exit = True