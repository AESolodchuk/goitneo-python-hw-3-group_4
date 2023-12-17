from models.errors import *
from models import *


new_book = AddressBook()


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def find_contact(name):
    found_contact = new_book.find(name)
    if found_contact == False:
        raise KeyError
    else:
        return found_contact


@input_error
def add_contact(args):
    name, phone = args
    if not phone.isnumeric():
        raise PhoneContainsAlphaSymbols
    if len(phone) != 10:
        raise PhoneContainsTenSymbols

    if new_book.find(name):
        new_book.find(name).add_phone(phone)
        return f"The new phone number to contact {name} successfully added."
    else:
        new_contact = Record(name)
        new_contact.add_phone(phone)
        new_book.add_record(new_contact)
        return f"Contact {name} successfully added."


@input_error
def change_contact(args):
    try:
        name, phone, new_phone = args
    except:
        raise NewPhoneWasNotProvided

    Record.edit_phone(find_contact(name), phone, new_phone)
    return f"Contact {name} successfully updated."


@input_error
def add_birthday(args):
    try:
        name, birthday = args
    except:
        raise BirthdayFormat

    if not Record.add_birthday(find_contact(name), birthday):
        raise WrongDataFormat
    return f"Birthday for the contact {name} successfully added."


@input_error
def show_birthday(args):
    name = args[0]

    birthday = Record.show_birthday(find_contact(name))
    return f"Contact {name} birthday: {birthday}"


@input_error
def show_phone(args):
    name = args[0]
    return find_contact(name)


@input_error
def show_all():
    return new_book.data.items()


def main():
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args))
        elif command == "change":
            print(change_contact(args))
        elif command == "phone":
            print(show_phone(args))
        elif command == "add-birthday":
            print(add_birthday(args))
        elif command == "show-birthday":
            print(show_birthday(args))
        elif command == "birthdays":
            print(new_book.get_birthdays_per_week())
        elif command == "all":
            for record in new_book.data.values():
                print(record)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
