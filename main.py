import csv
import re

def reading_from_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        # pprint(contacts_list)
        return contacts_list


def editing_contacts(contacts_text):
    contact_list = list(contacts_text)
    # Проверка на правильность заполнения ФИО по столбцам
    for contact in contact_list:
        if len(contact[0].split()) > 1:
            full_name = contact[0].split()
            contact[0] = full_name[0]
            contact[1] = full_name[1]
            if len(full_name) == 3:
                contact[2] = full_name[2]
            elif len(full_name) == 2:
                contact[2] = ''
        if len(contact[1].split()) > 1:
            name = contact[1].split()
            contact[1] = name[0]
            contact[2] = name[1]
    # Проверка на дублирование контактов
    for i in range(1, len(contact_list)):
        j = 1
        while i + j < len(contact_list):
            if contact_list[i][0] == contact_list[i + j][0] and contact_list[i][1] == contact_list[i + j][1]:
                k = 0
                while k < len(contact_list[i]):
                    if contact_list[i][k] < contact_list[i + j][k]:
                        contact_list[i][k] = contact_list[i + j][k]
                    k += 1
                contact_list.pop(i + j)
            j += 1
    return contact_list


def writing_to_file(file, contacts_list):
    with open(file, "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


def editing_phones(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        pattern = r"(\+7|8)\s*[\(]*(\d{3,5})[\)]*[\s-]*(\d{3})[\s-]?(\d{2})[\s-]?(\d{2}\s?)\s?[\(]?(\w*\.?)\s?(\d*)[\)]?"
        subst = r"+7(\2)\3-\4-\5\6\7"
        result = re.sub(pattern, subst, text)
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(result)


def main():
    contacts = reading_from_file("phonebook_raw.csv")
    contacts_edit = editing_contacts(contacts)
    writing_to_file("phonebook.csv", contacts_edit)
    editing_phones("phonebook.csv")

if __name__ == "__main__":
    main()