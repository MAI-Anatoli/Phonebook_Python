import csv

# Функция для чтения контактов из файла CSV
def read_contacts_from_csv():
    try:
        with open('contacts.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            contacts = list(reader)
        return contacts
    except FileNotFoundError:
        return []

# Функция для записи контактов в файл CSV
def write_contacts_to_csv(contacts):
    with open('contacts.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(contacts)

# Функция для отображения всех контактов
def show_contacts():
    contacts = read_contacts_from_csv()  # Пытаемся сначала прочитать из CSV
    if not contacts:
        try:
            with open('contacts.txt', 'r', encoding='utf-8') as file:
                contacts = [line.strip().split(', ') for line in file]
        except FileNotFoundError:
            pass
    
    if contacts:
        print("Список контактов:")
        for index, contact in enumerate(contacts, start=1):
            print(f"{index}. {', '.join(contact)}")
    else:
        print("Телефонный справочник пуст.")

# Функция для добавления контакта
def add_contact(name, number, comment):
    contact = [name, number, comment]
    contacts = read_contacts_from_csv()  # Пытаемся сначала прочитать из CSV
    if not contacts:
        try:
            with open('contacts.txt', 'r', encoding='utf-8') as file:
                contacts = [line.strip().split(', ') for line in file]
        except FileNotFoundError:
            pass
    contacts.append(contact)
    write_contacts_to_csv(contacts)
    print("Контакт успешно добавлен.")

# Функция для поиска контакта
def find_contact(search_term):
    try:
        # Пытаемся сначала прочитать из CSV
        contacts = read_contacts_from_csv()
        found = False
        for contact in contacts:
            if search_term.lower() in contact[0].lower():
                print("Контакт найден:")
                print(f"{contact[0]}, {contact[1]}, {contact[2]}\n")

                found = True
        if not found:
            # Если контакт не найден в CSV, пробуем из TXT
            contacts = read_contacts_from_txt()
            for contact in contacts:
                if search_term.lower() in contact[0].lower():
                    print("Контакт найден:")
                    print(f"{contact[0]}, {contact[1]}, {contact[2]}\n")
                    
                    found = True
        if not found:
            print("Контакт не найден.")
    except FileNotFoundError:
        print("Телефонный справочник пуст.")


# Функция для изменения контакта
def update_contact(name):
    try:
        with open('contacts.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            contacts = list(reader)
        
        # Список для хранения найденных контактов с указанным именем
        found_contacts = []
        
        # Поиск контактов с указанным именем
        for contact in contacts:
            if name.lower() in contact[0].lower():
                found_contacts.append(contact)
        
        if not found_contacts:
            print("Контакт не найден.")
            return
        
        # Если найдено более одного контакта с таким именем
        if len(found_contacts) > 1:
            print("Найдено несколько контактов с указанным именем:")
            for index, contact in enumerate(found_contacts, start=1):
                print(f"{index}. Имя: {contact[0]}, Номер: {contact[1]}, Комментарий: {contact[2]}")
            
            choice = input("Выберите номер контакта для изменения: ")
            try:
                index = int(choice)
                if 1 <= index <= len(found_contacts):
                    chosen_contact = found_contacts[index - 1]
                else:
                    print("Некорректный выбор.")
                    return
            except ValueError:
                print("Некорректный выбор.")
                return
        else:
            chosen_contact = found_contacts[0]
        
        # Предложение пользователю выбрать действие
        while True:
            print("\nВыберите действие:")
            print("1. Изменить номер")
            print("2. Изменить имя")
            print("3. Изменить комментарий")
            print("4. Выбрать другой контакт с таким же именем")
            print("5. Выход из программы")
            
            choice = input("Введите номер действия: ")
            
            if choice == '1':
                new_number = input("Введите новый номер телефона: ")
                chosen_contact[1] = new_number
                print("Номер успешно изменен.")
            elif choice == '2':
                new_name = input("Введите новое имя: ")
                chosen_contact[0] = new_name
                print("Имя успешно изменено.")
            elif choice == '3':
                new_comment = input("Введите новый комментарий: ")
                chosen_contact[2] = new_comment
                print("Комментарий успешно изменен.")
            elif choice == '4':
                update_contact(name)  # Рекурсивный вызов для выбора другого контакта с таким же именем
                break
            elif choice == '5':
                print("Выход из программы.")
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")
        
        # Запись обновленных контактов в файл CSV
        with open('contacts.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(contacts)
        
    except FileNotFoundError:
        print("Телефонный справочник пуст.")

# Функция для удаления контакта
def delete_contact(name):
    contacts = read_contacts_from_csv()  # Пытаемся сначала прочитать из CSV
    if not contacts:
        try:
            with open('contacts.txt', 'r', encoding='utf-8') as file:
                contacts = [line.strip().split(', ') for line in file]
        except FileNotFoundError:
            pass
    
    deleted = False
    for contact in contacts:
        if name.lower() in contact[0].lower():
            contacts.remove(contact)
            deleted = True
            print("Контакт успешно удален.")
            break
    
    if deleted:
        write_contacts_to_csv(contacts)
    else:
        delete_contact_txt(name)
# Функция для копирования контактов из одного файла в другой
def copy_contact(source_file, dest_file, line_number):
    try:
        with open(source_file, 'r') as source:
            contacts = source.readlines()
            if 0 < line_number <= len(contacts):
                contact_to_copy = contacts[line_number - 1]
                with open(dest_file, 'a') as dest:
                    dest.write(contact_to_copy)
                print("Контакт успешно скопирован.")
            else:
                print("Ошибка: указанная строка не существует.")
    except FileNotFoundError:
        print("Ошибка: файл не найден.")

# Основная функция для управления контактами
def main():
    while True:
        print("""
        1. Показать все контакты
        2. Добавить контакт
        3. Найти контакт
        4. Изменить контакт
        5. Удалить контакт
        6. Копировать контакт из одного файла в другой
        7. Выход из программы""")
        choice = input("Выберите действие: ")
        if choice == '1':
            show_contacts()
        elif choice == '2':
            name = input("Введите имя: ")
            number = input("Введите номер телефона: ")
            comment = input('Ведите комментарий: ')
            add_contact(name, number, comment)
            
        elif choice == '3':
            search_term = input("Введите имя или номер телефона для поиска: ")
            find_contact(search_term)
        elif choice == '4':
            name = input("Введите имя контакта для изменения: ")
            #new_number = input("Введите новый номер телефона: ")
            update_contact(name)

        elif choice == '5':
            name = input("Введите имя контакта для удаления: ")
            delete_contact(name)
        elif choice == '6':
            source_file = input("Введите имя файла, из которого нужно скопировать контакт: ")
            dest_file = input("Введите имя файла, в который нужно скопировать контакт: ")
            try:
                line_number = int(input("Введите номер строки для копирования: "))
                copy_contact(source_file, dest_file, line_number)
            except ValueError:
                print("Ошибка: введите целое число для номера строки.")
        elif choice == '7':
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие снова.")

if __name__ == "__main__":
    main()
