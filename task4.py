from __future__ import annotations


def input_error(func):
    """
    Декоратор для обробки типових помилок введення:
    - ValueError: неправильна кількість аргументів (наприклад, немає телефону)
    - IndexError: відсутній обов'язковий аргумент (наприклад, немає імені)
    - KeyError: контакт не знайдено
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError:
            # наприклад: add Bob  -> не вистачає телефону
            # або: add -> взагалі немає аргументів
            return "Give me name and phone please."

        except IndexError:
            # наприклад: phone -> немає імені
            return "Enter user name."

        except KeyError:
            # наприклад: phone Bob -> Bob не існує в contacts
            return "Contact not found."

    return inner


def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]
    return command, args


@input_error
def add_contact(args, contacts):
    name, phone = args  # ValueError, якщо args не з 2 елементів
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args  # ValueError, якщо args не з 2 елементів

    # Якщо такого імені немає — спеціально викликаємо KeyError
    if name not in contacts:
        raise KeyError

    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    name = args[0]  # IndexError, якщо args порожній

    # Спроба взяти контакт напряму: якщо немає — буде KeyError
    return contacts[name]


@input_error
def show_all(contacts):
    # Тут помилок введення майже немає, але за вимогою всі handler-и під декоратором
    if not contacts:
        return "No contacts."

    lines = [f"{name}: {phone}" for name, phone in contacts.items()]
    return "\n".join(lines)


def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "all":
            print(show_all(contacts))

        elif command == "":
            continue

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()