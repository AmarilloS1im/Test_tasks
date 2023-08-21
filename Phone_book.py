import os
import json
import re
import openpyxl


# Функция очистки консоли, для удобства чтения
def console_out_indent():
    '''print Что бы разграничить визуально меню , при запуски из IDE, как очистить вывод через код не смог найти:(
       os.system для очистки консоли, если запускать через терминал'''
    print('=============\n' * 10)
    os.system('cls||clear')


# Функция которая выводить в коносль меню, с вариантами выбора для пользователя
def phone_book_options():
    user_choice = str(input('Выберете, что хотите сделать:\n'
                            '1-Получить данные из телефонной книги\n'
                            '2-Добавить новые данные в телефонную книгу\n'
                            '3-Отредактировать уже имеющиеся данные\n'
                            '4-Завершить работу\n'
                            'Введите нужное значение: '))
    if user_choice == '1':
        console_out_indent()
        search_by_one_or_many()
    elif user_choice == '2':
        console_out_indent()
        manual_add_data_or_by_file()
    elif user_choice == '3':
        console_out_indent()
        change_phone_book_data()
    elif user_choice == '4':
        console_out_indent()
        print('Телефонная книга закрыта')
        return None
    else:
        console_out_indent()
        print('Вы ввели не корректный номер, выберите 1,2,3,4 или 5')
        phone_book_options()


# Функция которая предлагает выбрать варианты поиска, по одному параметру или множество параметров
# или вывести все данные постранично
def search_by_one_or_many():
    user_choice = str(input('Выберите параметры поиска:\n'
                            '1-Один параметр поиска\n'
                            '2-Поиск по множественным параметрам\n'
                            '3-Вывести данные постранично\n'
                            '4-Вернуться в главное меню\n'
                            'Введите нужное значение: '))
    if user_choice == '1':
        get_data_from_book_by_one_param()
    elif user_choice == '2':
        get_data_from_book_by_many_param()
    elif user_choice == '3':
        show_info_by_page()
    elif user_choice == '4':
        console_out_indent()
        phone_book_options()
    else:
        console_out_indent()
        print('Вы ввели не корректный номер, выберите 1,2,3 или 4')
        search_by_one_or_many()


# Функция которая выводит в консоль данные по одному параметру от пользователя
def get_data_from_book_by_one_param():
    user_choice = str(input(
        'Введите параметр поиска например Фамилию или номер телефона: '))
    with open('phone_book_data.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    out_list = []
    for i in range(len(json_data)):
        for j in range(len(json_data[i])):
            if user_choice.upper() in json_data[i][j]:
                out_list.append(json_data[i][j][user_choice.upper()])
    if len(out_list) == 1:
        [print(x) for x in out_list]
        user_choice = str(input('Найти новую запись?\n'
                                '1-Да\n'
                                '2-Возврат в главное меню\n'
                                'Введите нужное значение: '))
        if user_choice == '1':
            console_out_indent()
            get_data_from_book_by_one_param()
        else:
            console_out_indent()
            phone_book_options()
    else:
        print('\n\n\nНе найдено ни одной записи удовлетворяющей условиям поиска')
        user_choice = str(input('Хотите попробовать еще?\n'
                                '1-Да\n'
                                '2-Вернуться в глвное меню\n'
                                'Введите нужное значение: '))
        if user_choice == '1':
            console_out_indent()
            get_data_from_book_by_one_param()
        else:
            console_out_indent()
            phone_book_options()


# Функция которая выводит в консоль данные по множественным параметрам от пользователя
def get_data_from_book_by_many_param(flag_print_param = True):


    def check_bad_param(params):
        '''Получает на вход список из параметров которые ввел пользователь
           удаляет пустые строки и пробелы,и возвращает список с параметрами в которых есть хотя бы одна буква
           или цифра или спецсимвол и не пустых строк и пробелов'''
        new_param_list = []
        for param in params:
            match = re.match(r'\s*$', param)
            if match is None:
                new_param_list.append(param.upper())
        return new_param_list

    user_choice = str(input('Введите Фамилию или Имя или Отчество или название компании или рабочий номер телефона,'
                            ' или мобильный или введите все сразу.\nНе более 6 параметров.\n'
                            'Вводить данные нужно через запятую:  '))
    user_choice = user_choice.split(',')
    if len(user_choice) > 6:
        console_out_indent()
        print(f'Ошибка вы ввели {len(user_choice)} параметров, а допустимо максимум 6 параметров\n'
              f'==============================')
        get_data_from_book_by_many_param()
    user_choice = check_bad_param(user_choice)
    with open('phone_book_data.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    out_list = []
    for i in range(len(json_data)):
        count = 0
        for j in range(len(json_data[i])):
            if list(json_data[i][j].keys())[0].upper() not in user_choice:
                pass
            else:
                count += 1
        if count == len(user_choice):
            last_key = list(json_data[i][j].keys())[0]
            out_list.append(json_data[i][j][last_key])
    if len(out_list) < 1:
        console_out_indent()
        print('Не найдено ни одной записи удовлетворяющей условиям поиска\n\n\n')
        user_choice = str(input('Хотите попробовать еще?\n'
                                '1-Да\n'
                                '2-Вернуться в глвное меню\n'
                                'Введите нужное значение: '))
        if user_choice == '1':
            console_out_indent()
            get_data_from_book_by_many_param()
        else:
            console_out_indent()
            phone_book_options()
    else:
        if flag_print_param:
            [print(x) for x in out_list]
            user_choice = str(input('Найти новую запись?\n'
                                    '1-Да\n'
                                    '2-Вернуться в глвное меню \n'
                                    'Введите нужное значение: '))
            if user_choice == '1':
                console_out_indent()
                get_data_from_book_by_many_param()
            else:
                console_out_indent()
                phone_book_options()
        else:
            return out_list


# Функция выводит данные из телефонного справочника постранично
def show_info_by_page():
    with open('phone_book_data.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    page_list = []
    tmp_list = []
    for i in range(len(json_data)):
        tmp_list.append(list(json_data[i][0].values())[0])
    sorted_tmp_list = sorted(tmp_list, key=lambda x: x[0])
    tmp_list = []
    for data in sorted_tmp_list:
        tmp_list.append(data)
        if len(tmp_list) > 5:
            page_list.append(tmp_list)
            tmp_list = []
        else:
            continue
    page_list.append(tmp_list)

    # функция для вызова следующей страницы
    def next_page(page_list):
        '''Плучает на вход список списков с данными из справочника
            собирает в строку, добавляет перенос строк в конце и возвращает генератор.
            Это сделано, что бы выводить постранично красво в столбик, каждую страницу'''
        for i in range(len(page_list)):
            new_str = ''
            for j in range(len(page_list[i])):
                new_str = new_str + str(page_list[i][j]) + '\n'
            yield new_str

    page = next_page(page_list)
    print(next(page))
    print('стр 1')
    count = 1
    while count < len(page_list):
        user_choice = str(input('Нажмите кнопку Пробел и Enter чтобы посмотреть следующую страницу '))
        if user_choice == ' ':
            count += 1
            print(next(page))
            print(f'стр {count}')
        else:
            pass
    print('Вы дошли до конца справочника\n\n')
    user_choice = str(input('1-Вернуться в главное меню\n'
                            '2-Завершить работу\n'
                            'Введите нужное значение: '))
    if user_choice == '1':
        console_out_indent()
        phone_book_options()
    else:
        print('\n\n\n\nРабота завершена')
        return None


# Функция которая предлагает выбрать, добавлять данные вручную или загрузить через файл эксель
def manual_add_data_or_by_file():
    user_choice = str(input('1-Ввести данные вручную\n'
                            '2-Загрузка через файл эксель\n'
                            '3-Вернуться в главное меню\n'
                            'Введите нужное значение: '))
    if user_choice == '1':
        console_out_indent()
        add_data_to_book_manual()
    elif user_choice == '2':
        add_data_to_book_by_file()
    elif user_choice == '3':
        console_out_indent()
        phone_book_options()
    else:
        console_out_indent()
        print('Вы ввели некорректный номер, выберите 1,2 или 3')
        manual_add_data_or_by_file()


# Функция которая добавляет данные вручну
def add_data_to_book_manual():
    last_name = str(input('Введите фамилию: '))
    first_name = str(input('Введите имя: '))
    middle_name = str(input('Введите отчество: '))
    company_name = str(input('Введите название компании: '))
    work_phone_number = str(input('Введите рабочий номер телефона: '))
    cell_phone_number = str(input('Введите личный (сотовый) номер телефона: '))
    new_data = [{f'{last_name.upper()}': [last_name, first_name, middle_name, company_name, work_phone_number,
                                          cell_phone_number]},
                {f'{first_name.upper()}': [last_name, first_name, middle_name, company_name, work_phone_number,
                                           cell_phone_number]},
                {f'{middle_name.upper()}': [last_name, first_name, middle_name, company_name, work_phone_number,
                                            cell_phone_number]},
                {f'{company_name.upper()}': [last_name, first_name, middle_name, company_name, work_phone_number,
                                             cell_phone_number]},
                {f'{work_phone_number.upper()}': [last_name, first_name, middle_name, company_name, work_phone_number,
                                                  cell_phone_number]},
                {f'{cell_phone_number.upper()}': [last_name, first_name, middle_name, company_name, work_phone_number,
                                                  cell_phone_number]}
                ]
    with open('phone_book_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        data.append(new_data)
    with open('phone_book_data.json', 'w', encoding='utf-8') as new_file:
        json.dump(data, new_file, indent=3, ensure_ascii=False)
    find_duplicates()
    print('Данные успешно добавлены')
    user_choice = int(input('Добавить еще данные?\n'
                            '1-Да\n'
                            '2-Вернуться в главное меню\n'
                            'Введите нужное значение: '))
    if user_choice == 1:
        add_data_to_book_manual()
    else:
        console_out_indent()
        phone_book_options()


# Функция которая добавляет данные из файла эксель
def add_data_to_book_by_file():
    user_choice = str(input('\n\n\n'
                            'ВНИМАНИЕ файл должен быть в формате .xls или .xlsx\n\n'
                            'Данные в файле заполняются с самой первой ячейки и далее вниз, всего 6 столбцов:\n'
                            'Фамилия,Имя,Отчество,Название компании,Рабочий номер телефона,Личный номер телефона\n'
                            'Введите путь к файлу\n\n'))
    file_extention = user_choice.split('.')[-1]
    if file_extention != 'xlsx' and file_extention != 'xls':
        print('\n\n\n\n\n\n\nОшибка, файл может быть только в формате xlsx или xls')
        add_data_to_book_by_file()
    else:
        try:
            book = openpyxl.open(user_choice, read_only=True, data_only=True)
            sheet = book.active
            row = 1
            temp_data_list = []
            with open('phone_book_data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            for x in range(1, sheet.max_row + 1):
                for column in range(0, 6):
                    temp_data_list.append(sheet[row][column].value)
                new_data = [{f'{str(temp_data_list[0]).upper()}': temp_data_list},
                            {f'{str(temp_data_list[1]).upper()}': temp_data_list},
                            {f'{str(temp_data_list[2]).upper()}': temp_data_list},
                            {f'{str(temp_data_list[3]).upper()}': temp_data_list},
                            {f'{str(temp_data_list[4]).upper()}': temp_data_list},
                            {f'{str(temp_data_list[5]).upper()}': temp_data_list}]
                data.append(new_data)
                temp_data_list = []
                row += 1
            with open('phone_book_data.json', 'w', encoding='utf-8') as new_file:
                json.dump(data, new_file, indent=3, ensure_ascii=False)
            find_duplicates()
            print('Данные успешно добавлены')
            user_choice = str(input('Загрузить еще файл?\n'
                                    '1-Да\n'
                                    '2-Вернуться в главное меню\n'
                                    'Введите нужное значение: '))
            if user_choice == '1':
                console_out_indent()
                add_data_to_book_by_file()
            else:
                console_out_indent()
                phone_book_options()
        except IOError as ex:
            console_out_indent()
            user_choice = str(input(f'{ex}\n\n'
                  f'Ошибка при открытии файла, проверьте правильность пути\n'
                  f'1-Попробовать еще раз\n'
                  f'2-Вернуться в главное меню\n'
                  f'Введите нужное значение: '))


            if user_choice == '1':
                add_data_to_book_by_file()
            else:
                console_out_indent()
                phone_book_options()




# Функция редактирует одну выбранную запись, по одному выбранному параметру
def change_phone_book_data():
    #Функция возвращает шаблон заполнения json файла
    def new_data_template_to_append(last_name, first_name, middle_name, company_name, work_phone_number,
                                    cell_phone_number):
        new_data = [{f'{last_name.upper()}': [last_name, first_name, middle_name, company_name, work_phone_number,
                                              cell_phone_number]},
                    {f'{first_name.upper()}': [last_name, first_name, middle_name, company_name, work_phone_number,
                                               cell_phone_number]},
                    {f'{middle_name.upper()}': [last_name, first_name, middle_name, company_name, work_phone_number,
                                                cell_phone_number]},
                    {f'{company_name.upper()}': [last_name, first_name, middle_name, company_name,
                                                 work_phone_number, cell_phone_number]},
                    {f'{work_phone_number.upper()}': [last_name, first_name, middle_name, company_name,
                                                      work_phone_number, cell_phone_number]},
                    {f'{cell_phone_number.upper()}': [last_name, first_name, middle_name, company_name,
                                                      work_phone_number, cell_phone_number]}
                    ]
        return new_data

    print('Для изменения данных введите в поиске нужные параметры\n')
    data_to_change = get_data_from_book_by_many_param(flag_print_param=False)
    print(data_to_change)
    print(len(data_to_change))
    if len(data_to_change) > 0 and len(data_to_change) < 2:
        user_choice = str(input('Выберите, какой параметр вы хотите поменять\n'
                                '1-Фамилию\n'
                                '2-Имя\n'
                                '3-Отчество\n'
                                '4-Название компании\n'
                                '5-Рабочий телефон\n'
                                '6-Личный телефон\n'))
        if user_choice == '1':
            new_key = str(input('Введите новую фамилию: '))
            last_name = new_key
            first_name = str(data_to_change[0][1])
            middle_name = str(data_to_change[0][2])
            company_name = str(data_to_change[0][3])
            work_phone_number = str(data_to_change[0][4])
            cell_phone_number = str(data_to_change[0][5])
            new_data = new_data_template_to_append(last_name, first_name,
                                                   middle_name, company_name, work_phone_number, cell_phone_number)
        elif user_choice == '2':
            new_key = str(input('Введите новое Имя: '))
            last_name = str(data_to_change[0][0])
            first_name = new_key
            middle_name = str(data_to_change[0][2])
            company_name = str(data_to_change[0][3])
            work_phone_number = str(data_to_change[0][4])
            cell_phone_number = str(data_to_change[0][5])
            new_data = new_data = new_data_template_to_append(last_name, first_name,
                                                              middle_name, company_name, work_phone_number,
                                                              cell_phone_number)
        elif user_choice == '3':
            new_key = str(input('Введите новое Отчество: '))
            last_name = str(data_to_change[0][0])
            first_name = str(data_to_change[0][1])
            middle_name = new_key
            company_name = str(data_to_change[0][3])
            work_phone_number = str(data_to_change[0][4])
            cell_phone_number = str(data_to_change[0][5])
            new_data = new_data = new_data_template_to_append(last_name, first_name,
                                                              middle_name, company_name, work_phone_number,
                                                              cell_phone_number)
        elif user_choice == '4':
            new_key = str(input('Введите новое название компании: '))
            last_name = str(data_to_change[0][0])
            first_name = str(data_to_change[0][1])
            middle_name = str(data_to_change[0][2])
            company_name = new_key
            work_phone_number = str(data_to_change[0][4])
            cell_phone_number = str(data_to_change[0][5])
            new_data = new_data = new_data_template_to_append(last_name, first_name,
                                                              middle_name, company_name, work_phone_number,
                                                              cell_phone_number)
        elif user_choice == '5':
            new_key = str(input('Введите новый рабочий номер телефона: '))
            last_name = str(data_to_change[0][0])
            first_name = str(data_to_change[0][1])
            middle_name = str(data_to_change[0][2])
            company_name = str(data_to_change[0][3])
            work_phone_number = new_key
            cell_phone_number = str(data_to_change[0][5])
            new_data = new_data = new_data_template_to_append(last_name, first_name,
                                                              middle_name, company_name, work_phone_number,
                                                              cell_phone_number)
        elif user_choice == '6':
            new_key = str(input('Введите новый номер личного телефона: '))
            last_name = str(data_to_change[0][0])
            first_name = str(data_to_change[0][1])
            middle_name = str(data_to_change[0][2])
            company_name = str(data_to_change[0][3])
            work_phone_number = str(data_to_change[0][4])
            cell_phone_number = new_key
            new_data = new_data = new_data_template_to_append(last_name, first_name,
                                                              middle_name, company_name, work_phone_number,
                                                              cell_phone_number)
        with open('phone_book_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        data.append(new_data)
        data_to_change[0] = [str(x).upper() for x in data_to_change[0]]
        for i in range(len(data)):
            count = 0
            for j in range(len(data[i])):
                if list(data[i][j].keys())[0] not in data_to_change[0]:
                    pass
                else:
                    count += 1
            if count == len(data_to_change[0]):
                del data[i]
                break

        with open('phone_book_data.json', 'w', encoding='utf-8') as new_file:
            json.dump(data, new_file, indent=3, ensure_ascii=False)
        print('Данные успешно изменены')
        user_choice = str(input('Хотите изменить еще одну запись?\n'
                                '1-Да\n'
                                '2-Вернуться в главное меню\n'
                                'Введите нужное значение: '))
        if user_choice == '1':
            console_out_indent()
            change_phone_book_data()
        else:
            console_out_indent()
            phone_book_options()
    else:
        console_out_indent()
        print(data_to_change)
        print('Слишком большое количество записей для редактирования\n'
              'Должна быть одна запись. Увеличте колличество параметров в поиске,\n'
              'чтобы точно определить какую запись нужно изменить')

        change_phone_book_data()
#Функция которая проверяет на абсолютные дубликаты и удаляет их если находит
def find_duplicates():
    with open('phone_book_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    check_list = []
    for i in range(len(data)):
        check_list.append(list(data[i][0].values())[0])
    check_list= sorted(check_list, key=lambda x: str(x[-1]))
    duplicate_list = []

    for i in range(len(check_list)-1):
        tmp_list = []
        for j in range(len(check_list[i])):
            if check_list[i][j] == check_list[i+1][j]:
                tmp_list.append(str(check_list[i][j]).upper())
            else:
                tmp_list = []
                break
        if len(tmp_list)> 0:
            duplicate_list.append(tmp_list)
        else:
            pass

    for x in range(len(duplicate_list)):
        for i in range(len(data)):
            count = 0
            for j in range(len(data[i])):
                if list(data[i][j].keys())[0] not in duplicate_list[x]:
                    pass
                else:
                    count += 1
            if count == len(duplicate_list[x]):
                del data[i]
                break
    with open('phone_book_data.json', 'w', encoding='utf-8') as new_file:
        json.dump(data, new_file, indent=3, ensure_ascii=False)


if __name__ == '__main__':
    phone_book_options()



