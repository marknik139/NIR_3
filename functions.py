import sqlite3
import sys

def menu():
    print('Что требуется сделать? \n')
    print('1. Отображение выбранной таблицы БД')
    print('2. Составить и отобразить на экране перечень полных наименований вузов, с выбранным федеральным округом и у которых в БД отсутствует адрес эл. почты')
    print('3. Рассчитать и представить в виде таблицы распределение количества студентов по статусам вузов')
    print('4. Закончить работу программы')
    return input('Выберите действие >>> ')


def tn_choice(table_name_kart, table_name_stat):
    choice = input('Какую таблицу вывести? \n\n 1. <Картотека вузов> \n\n 2. <Статистика вузов> \n\n Выбор >>> ')
    if choice == '1':
        return table_name_kart
    elif choice == '2':
        return table_name_stat


def table_bd(db_name, table_name):
    """
    Отображение текущего содержимого БД на экране в виде таблицы
    """
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    sql = 'SELECT * FROM {}'.format(table_name)
    with con:
        data = cur.execute(sql).fetchall()

    print('\n \nТаблица: ', table_name, ' из БД', db_name, '\n')

    col_width = [0] * len(data[0])

    for x in data:
        for k, y in enumerate(x):
            if len(str(y).strip()) > col_width[k]:
                col_width[k] = len(str(y).strip())

    for x in col_width:
        if x < max(col_width):
            x = max(col_width)

    for line in data:
        for i, x in enumerate(line):
            sys.stdout.write('{0}{1}'.format(str(x).strip(), ((col_width[i] - len(str(x).strip())) * ' ' + '  ')))
        print('')

    cur.close()
    con.close()

def select_region():
    """
    Выбор региона
    """    
    print('Выберите федеральный округ вуза')
    print(' 1. Южный')
    print(' 2. Центральный')
    print(' 3. Уральский')
    print(' 4. Сибирский')
    print(' 5. Северо-Кавказский')
    print(' 6. Северо-Западный')
    print(' 7. Приволжский')
    print(' 8. Дальневосточный')
    choice = input('Выбор >>> ')

    if choice == '1':
        return 'Южный'
    elif choice == '2':
        return 'Центральный'
    elif choice == '3':
        return 'Уральский'
    elif choice == '4':
        return 'Сибирский'
    elif choice == '5':
        return 'Северо-Кавказский'
    elif choice == '6':
        return 'Северо-Западный'
    elif choice == '7':
        return 'Приволжский'
    elif choice == '8':
        return 'Дальневосточный'
    else:
        print('\n\n Ошибка ввода')
        input('\n Завершение работы с программой \n\n Нажмите на любую клавишу, чтобы выйти')
        sys.exit()


def vuz_without_mail(bd_name, table_name_kart, selected_region):
    """
    Вывод вузов без указанной эдектронной почты для выбранного региона.
    """
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    sql = 'SELECT TRIM(z1) FROM {0} WHERE TRIM(region) = "{1}" AND TRIM(e_mail) = ""  '.format(
        table_name_kart, selected_region)
    cur.execute(sql)
    data = []

    while True:
        next_row = cur.fetchone()
        if next_row:
            data.append(next_row[0])
        else:
            break

    return data


def raspred_stud(bd_name, table_name_kart, table_name_stat):
    """
    Для выбранного профиля вуза расчёт и представление в виде
    таблицы распределения кол-во студентов по статусам вуза
    """
    con = sqlite3.connect(bd_name)
    cur = con.cursor()
    sql="SELECT a.prof FROM vuzkart as a, vuzstat as b ON a.codvuz=b.codvuz"
    data = list(set(cur.execute(sql).fetchall())) # Профили подготовки

    K=1
    while(K):
        print("Выберите интересующий профиль подготовки: ")
        for i in range(len(data)):
            print("{} - для выбора {}".format(i+1,data[i][0]))
        profil=input(">>>")
        if profil=="1":
            z_profil=data[0][0]
            K=0
        elif profil=="2":
            z_profil=data[1][0]
            K=0
        elif profil=="3":
            z_profil=data[2][0]
            K=0
        elif profil=="4":
            z_profil=data[3][0]
            K=0
        else:
            print("Ошибка! Вы ввели неправильное значение. Введите значение снова\n")

    sql="SELECT a.status FROM vuzkart as a, vuzstat as b ON a.codvuz=b.codvuz"
    data_1 = list(set(cur.execute(sql).fetchall())) # Статусы вузов
    print("Порядковый номер".center(25),"|","Статус".center(25),"|","Кол-во студентов".center(25),"|","Процент от общего числа студентов".center(40))
    print('------------------------------------------------------------------------------------------------------------------------------')

    sql = 'SELECT b.stud FROM vuzkart as a,vuzstat as b ON a.codvuz=b.codvuz WHERE a.prof=="{}"' .format(z_profil)
    data_4=cur.execute(sql).fetchall()
    Sum1=0
    for i in data_4:
        Sum1+=i[0]
        
    for i in range(len(data_1)) :
        sql = 'SELECT b.stud FROM vuzkart as a,vuzstat as b ON a.codvuz=b.codvuz WHERE a.status=="{}" and prof=="{}"' .format(data_1[i][0],z_profil)
        data_3=cur.execute(sql).fetchall()
        kol=0
        Sum=0
        for j in range(len(data_3)):
            kol+=1
            Sum+=data_3[j][0]
        print(str(i+1).center(25),"|",str(data_1[i][0]).center(25),"|",str(Sum).center(25),"|",(str(Sum/Sum1*100)+'%').center(40))
    print("Сумма количества студентов для вузов с профилем {} = {} ".format(z_profil,Sum1))
