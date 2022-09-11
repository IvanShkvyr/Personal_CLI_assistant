import classes
from commands import commands, def_mod
import functions
import sys
from InquirerPy import inquirer
import os


def main():
    print("\nWelcome to your personal Python assistant!")
    size = os.get_terminal_size().lines
    if size < 15:
        print("\nYou can increase the size of the terminal to have a better experience working with the command line")
    print("\nWhat can I do for you today?")
    book = classes.AddressBook()
    book.read_from_file()
    congratulate = []
    if functions.find_birthdays(book, "0") != "Nobody has a birthday today":
        congratulate.append(functions.find_birthdays(book, "0"))
    if functions.find_birthdays(book, "1") != "Nobody has a birthday tomorrow":
        congratulate.append(functions.find_birthdays(book, "1"))
    if congratulate:
        print("\nLet me remind that")
        print("\n".join(congratulate))
        print("Do not forget to congratulate them\n")
    print("How can I help you today?")
    while True:
        size = os.get_terminal_size().lines
        if size > 15:
            names = {}
            for name in book.names:
                names[name] = None
            request = inquirer.text(
                message="",
                completer=create_completer(book),
                multicolumn_complete=False,
            ).execute()
            command = request
        else:
            command = input()
        mode, data = def_mod(command)
        output = commands.get(mode)(book, data)
        if output != '':
            print(output)
        if output == "Good bye!":
            book.write_to_file()
            sys.exit()


def create_completer(book: classes.AddressBook):
    names = {}
    for name in book.names:
        names[name] = None
    new_dict = {
        "hello": None,
        "exit": None,
        "good bye": None,
        "close": None,
        "save": None,
        "load": None,
        "phone": names,
        "add": {
            "contact": None,
            "number": names,
            "email": names,
        },
        "delete": {
            "contact": names,
            "number": names,
            "birthday": names,
        },
        "find": None,
        "show": {
            "all": None,
            "contact": names,
        },
        "set": {
            "birthday": names,
        },
        "help": None,
        "show birthday": None,
        "rename": None,
    }
    return new_dict


if __name__ == "__main__":
    main()
