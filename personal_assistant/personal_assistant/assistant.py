import classes
from commands import commands, def_mod
import sys
from InquirerPy import inquirer
import os


def main():
    print("Welcome to your personal Python assistant!")
    print("What can I do for you today?")
    book = classes.AddressBook()
    book.read_from_file()
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
        "set birthday": names,
        "help": None,
        "show birthday": None,
        "rename": None,
    }
    return new_dict


if __name__ == "__main__":
    main()
