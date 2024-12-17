import csv
import re


def get_list_from_csv(file):
    """Функция, которая получает список из файла csv."""
    try:
        with open(file, encoding="utf-8") as f:
            rows = csv.reader(f, delimiter=",")
            return list(rows)
    except Exception as ex_get_csv:
        print(f"Ошибка при получении данных из csv. {ex_get_csv}")


def get_digit(string: str):
    """Функция, которая получает кортеж из чисел номера и цифры:
     если 0 - нет добавочного номера, если 1 - есть."""
    number = ""
    flag = 0
    if "доб" in string:
        flag = 1
    for item in string:
        if item.isdigit():
            number += item
    return number, flag


def get_format_number(number_phone):
    """Функция, которая преобразует номер телефона."""
    if number_phone == "":
        return ""
    numbers = get_digit(number_phone)
    if numbers[1]:
        return re.sub(r"(\d)(\d{3})(\d{3})(\d{2})(\d{2})(\d)", r"+7(\2)\3-\4-\5 доб.\6", numbers[0])
    return re.sub(r"(\d)(\d{3})(\d{3})(\d{2})(\d{2})", r"+7(\2)\3-\4-\5", numbers[0])


def group_two_list(lst1, lst2):
    """Функция, которая объединяет два списка."""
    try:
        group_lst = []
        for i in range(len(lst1)):
            if lst1[i] == lst2[i]:
                group_lst.append(lst1[i])
            elif lst1[i] == "":
                group_lst.append(lst2[i])
            else:
                group_lst.append(lst1[i])
        return group_lst
    except Exception as ex_group:
        print(f"Ошибка при объединение двух список! {ex_group}")


def convert_data(contacts_lst):
    """Функция, которая преобразует список контактов."""
    try:
        convert_lst = []
        for contact in contacts_lst[1:]:
            lst = " ".join(contact[:3]).split()
            if len(lst) == 2:
                lst.append("")
            lst.extend(contact[3:5])
            lst.append(get_format_number(contact[5]))
            lst.append(contact[6])
            convert_lst.append(lst)
        return convert_lst
    except Exception as ex:
        print(f"Ошибка при преобразовании списка контактов. {ex}")


def get_group_data(convert_lst):
    """Функция, которая объединяет дублирующие данные."""
    lst = convert_data(convert_lst)
    group_list = []
    for ind1, item1 in enumerate(lst):
        for _, item2 in enumerate(lst[ind1 + 1:]):
            if item1[:2] == item2[:2]:
                item1 = item1[:2] + group_two_list(item1[2:], item2[2:])
                lst.remove(item2)
            ind1 += 1
        group_list.append(item1)
    return group_list


def prepare_data_for_csv(group_data, header):
    """Функция, которая формирует окончательный список для файла csv."""
    data = [header] + get_group_data(group_data)
    return data


def add_list_in_csv(file, contact):
    """Функция, которая записывает данные в формате CSV."""
    try:
        with open(file, "w", encoding="utf-8", newline="") as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(contact)
    except Exception as ex_add:
        print(f"Ошибка при добавлении списка в файл csv. {ex_add}")


if __name__ == '__main__':
    contacts_list = get_list_from_csv("phonebook_raw.csv")
    contacts = prepare_data_for_csv(contacts_list, contacts_list[0])
    new_file = "phonebook.csv"
    add_list_in_csv(new_file, contacts)
