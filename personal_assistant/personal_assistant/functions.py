import classes
from classes import *
import re
from notes import Note, Tags

phone_pattern = "\s\+?[-\s]?(?:\d{2,3})?[-\s]?(?:\([-\s]?\d{2,3}[-\s]?\)|\d{2,3})?[-\s]?\d{2,3}[-\s]?\d{2,3}[-\s]?\d{2,3}\s"
no_number = "Sorry, I can't identify a phone number."
no_name = "Sorry, I can't identify a contact's name."


def decorator(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(args[0], AddressBook):
            args[0].showing_records = False
            args[0].page = 0
        if isinstance(result, Exception):
            return str(Exception)
        else:
            return result
    return inner


def save_to_file(book: AddressBook, text: str = ""):
    text = text.strip()
    return book.write_to_file(text)


def read_from_file(book: AddressBook, text: str = ""):
    text = text.strip()
    return book.read_from_file(text)


@decorator
def clear(book: AddressBook, *_):
    if confirm(f"Do you want to delete all contacts from your Address book? Type 'yes'/'no'.\n"):
        book.clear()
        return f"Done!"
    else:
        return f"Glad you changed your mind."


def confirm(question):
    while True:
        string = input(question)
        if string.strip().lower() in ("y", "yes"):
            return True
        if string.strip().lower() in ("n", "no"):
            return False


def find_name_number(text: str):  # return tuple of name and number
    text += " "
    pattern = re.compile(phone_pattern)
    only_name = text
    if not pattern.findall(text):
        return find_name(text), ""
    for x in pattern.findall(text):
        only_name = only_name[:only_name.find(x)]
    return find_name(only_name), str(pattern.findall(text)[0]).strip().replace(" ", "").replace("", ""),


def find_name(text: str):  # converts text into name. Should be used only after the numer has been extracted.
    return text.strip().lower().title()


@decorator
def find(book: AddressBook, text: str):
    text = text.strip()
    contacts = book.search_in_names(text)  # list of names
    numbers = book.search_in_phones(text)  # list of tuples (name, number)
    mails = book.search_in_emails(text)
    notes = book.notes.search_in_notes(text)
    notes_tags = book.notes.find_by_tags(text)
    result = ""
    if not text:
        return "Nothing to search"
    if not (contacts or numbers or mails or notes or notes_tags):
        return "No matches found"
    else:
        if contacts:
            result += f"Matches in names:\n"
            for name in contacts:
                result += f"\t{name}\n"
        if numbers:
            result += f"Matches in phone numbers:\n"
            for pair in numbers:
                result += f"\t{pair[0]}: {pair[1]}\n"
        if mails:
            result += f"Matches in email addresses:\n"
            for pair in mails:
                result += f"\t{pair[0]}: {pair[1]}\n"
        if notes:
            result += f"Matches in notes:\n"
            for each in notes:
                result += f"\t{each._name()}: {each._note()}\n"
        if notes_tags:
            result += f"Matches in notes tags:\n"
            for each in notes_tags:
                tags = ','.join(each._tags())
                result += f"{each._name()}: {tags}\n"
        return result


@decorator
def find_birthdays(book: AddressBook, text: str):
    text = text.strip()
    try:
        days = int(text)
    except ValueError:
        return "invalid format of the numbers of days"
    if isinstance(days, int):
        print(days)
        output = []
        for contact in book.data.keys():
            if book.data.get(contact).birthday is not None:
                if book.data.get(contact).birthday.days_to_next_birthday is not None and \
                        book.data.get(contact).birthday.days_to_next_birthday == days:
                    output.append(contact)
        if not output:
            return f"Nobody has birthday in {days} days"
        elif len(output) == 1:
            return f"{output[0]} has birthday in {days} days"
        elif len(output) == 2:
            return f"{output[0]} and {output[1]} have birthday in {days} days"
        else:
            return f"{','.join(output[:-1]) + ', and ' + output[-1]} have birthday in {days} days"


def name_birthday(book: AddressBook, text: str):
    for contact in book.data.keys():
        if contact.lower() in text.lower():
            return contact, text.lower().replace(contact.lower(), "", 1).strip()
    return None, None


def name_email(book: AddressBook, text: str):
    for contact in book.data.keys():
        if contact.lower() in text.lower():
            template = re.compile(r"[a-zA-Z][a-zA-Z0-9_.]+@[a-zA-Z]+\.[a-zA-Z][a-zA-Z]+")
            mails = text.lower().replace(contact.lower(), "", 1).strip()
            mail_list = re.findall(template, mails)
            if mail_list and mail_list[0]:
                return contact, mail_list[0]
            else:
                return contact, None
    return None, None


@decorator
def add_contact(book: AddressBook, data: str):
    name, number = find_name_number(data)
    if not name:
        return no_name
    elif name in book.data.keys():
        return f"Contact '{name}' already exists"
    else:
        phone_number = Phone(number)
        if phone_number.value:
            record = Record(Name(name), [phone_number])
            book.add_record(record)
            return f"Created contact '{name}': '{number}'"
        else:
            record = Record(Name(name), [])
            book.add_record(record)
            return f"Created contact '{name}' with no phone numbers."


@decorator
def rename(book: AddressBook, data: str):
    name = find_name(data)
    if not name:
        return "Name has not been found"
    elif name not in book.data.keys():
        return f"Contact '{name}' already exists"
    else:
        while True:
            new_name = input(f"Please enter a new name for the contact {name}\n")
            new_name = find_name(new_name)
            print(name, new_name)
            if new_name not in book.data.keys():
                add_contact(book, new_name)
                book.data[new_name] = book.data.get(name)
                book.data.get(new_name).name.value = new_name
                delete_contact(book, name)
                return "Done"
            else:
                print(f"Contact '{new_name}' has already exist")


@decorator
def show_contact(book: AddressBook, data: str):
    name = find_name(data)
    if not name:
        return "Sorry, I can't identify a contact's name"
    if name not in book.data.keys():
        return f"Contact '{name}' is not in your contacts"
    else:
        return str(book.data.get(name))


def empty(book: AddressBook, *_):
    if not book.showing_records:
        return "Sorry I can't understand you. Try 'help' command to see what I can."
    else:
        return show_all(book)


@decorator
def reset(book: AddressBook, text: str = "2"):
    try:
        n = int(text.strip())
    except ValueError:
        n = 2
    book.reset_iterator(n)
    return "Done!"


def show_all(book: AddressBook, text: str = ""):
    try:
        n = int(text.strip())
        book.contacts_per_page = n
    except ValueError:
        n = book.contacts_per_page
    if not book.data:
        return "Your phone book is empty."
    else:
        output_line = ""
        first = book.page * n + 1  # first contact to show
        last = min(book.page * n + n, book.size)  # last contact to show
        if book.size == last:
            pass
        zero_line = f"Showing contacts {first}-{last} from {book.size} records:\n"
        if not book.showing_records:
            book.showing_records = True
            book.reset_iterator(n)
        try:
            output_line = zero_line + next(book.show)
            if last == book.size:
                output_line += f"End of the address book"
                book.page = 0
            else:
                output_line += f"Press 'Enter' to show next {n} contacts or 'reset' to go to the start"
                book.page += 1
            return output_line
        except StopIteration:
            book.showing_records = False
            book.reset_iterator(n)
            book.page = 0
            return ""


@decorator
def phone(book: AddressBook, data: str):
    name = find_name(data)
    if not name:
        return "Sorry, I can't identify a contact's name"
    if name not in book.data.keys():
        return f"Contact '{name}' is not in your contacts"
    else:
        return f"{name}: {', '.join([x.value for x in book.data.get(name).phones])}"


@decorator
def add_number(book: AddressBook, data: str):
    name, number = find_name_number(data)
    if not name:
        return no_name
    elif not number:
        return no_number
    elif name not in book.data.keys():
        add_contact(book, data)
        return f"Created a new contact '{name}' with number '{number}'"
    else:
        phone_number = Phone(number)
        if phone_number.value:
            book.data[name].add_number(phone_number)
            return f"Number '{number}' has been added to contact '{name}'"
        else:
            return f"Invalid phone number"


@decorator
def delete_number(book: AddressBook, data: str):
    name, number = find_name_number(data)
    if name and not number:
        if name in book.data.keys():
            if confirm(f"Do you want to delete all numbers from contact '{name}'? Type 'yes'/'no'.\n"):
                for number in book.data.get(name).phones:
                    book.data.get(name).del_number(number)
                return f"Done!"
            else:
                return f"Nothing changed"
        else:
            return f"Contact {name} does not exist."
    elif name and number:
        if name in book.data.keys():
            if number in [x.value for x in book.data.get(name).phones]:
                book.data.get(name).del_number(Phone(number))
                return f"Number '{number}' has been deleted from contact '{name}'"
            else:
                return f"Contact '{name}' has no phone number '{number}'."
    else:
        return no_name


@decorator
def delete_contact(book: AddressBook, data: str):
    name, number = find_name_number(data)
    if not name:
        return no_name
    elif name in book.data.keys():
        if confirm(f"Contact '{name}' will be deleted/renamed. "
                   f"Are you sure? Type 'yes' or 'no'.\n"):
            book.delete_record(name)
            return "Done!"
        else:
            return f"Glad you changed your mind."


@decorator
def set_birthday(book: AddressBook, data: str):
    name, birthday = name_birthday(book, data)
    if not name:
        return no_name
    elif not birthday:
        return "No date specified"
    else:
        date = classes.convert_to_date(birthday)
        if date:
            book.data.get(name).set_birthday(Birthday(birthday))
            return "Done"
        else:
            return "Invalid value of date"


@decorator
def delete_birthday(book: AddressBook, data: str):
    if not name_birthday(book, data):
        return "Contact does not exist"
    else:
        name, birthday = name_birthday(book, data)
        book.data.get(name).set_birthday(None)
        return "Done"


@decorator
def add_email(book: AddressBook, data: str):
    name, email = name_email(book, data)
    if not name:
        return "Can't find a valid contact"
    if not email:
        return "Can't find a valid email address"
    else:
        name, email = name_email(book, data)
        book.data.get(name).add_email(Email(email))
        return "Done"


@decorator
def delete_email(book: AddressBook, data: str):
    # return "function doesn't work"
    name, email = name_email(book, data)
    if not name:
        return "Can't find a valid contact"
    else:
        if not email:
            if name in book.data.keys():
                if confirm(f"Do you want to delete all emails from contact '{name}'? Type 'yes'/'no'.\n"):
                    for mail in book.data.get(name).emails:
                        book.data.get(name).del_email(mail)
                    return "Done"
                else:
                    return "Nothing has been deleted"
            else:
                return "Can't find a valid contact"
        else:
            if email in [x.value for x in book.data.get(name).emails]:
                book.data.get(name).del_email(Email(email))
                return f"Email '{email}' has been deleted from the contact '{name}'"
            else:
                return f"Contact '{name}' has no email '{email}'."

@decorator
def create_note(book: AddressBook, *_):
    note = Note(
        name=input('Enter name:'), note=input('Enter note: '), tags=Tags(input('Enter tags or press ENTER: ').split(','))
    )
    book.notes.add_note(note)
    return 'Note created.'

@decorator
def delete_note(book: AddressBook, *_):
    book.notes.delete_note(input('Enter note name or note id: '))
    return "Note deleted successfully!"

@decorator
def rename_note(book: AddressBook, *_):
    book.notes.change_note_name(input('Enter note name or note id: '), input('Enter new note name: '))
    return ''

@decorator
def change_note(book: AddressBook, *_):
    book.notes.change_note(note_id=input('Enter note name or ID:'), new_note=input("Enter new note: "))
    return "Operation successfull!"

@decorator
def show_all_notes(book:AddressBook, *_):
    book.notes.show_all()
    return ''

@decorator
def show_note_list(book:AddressBook, *_):
    book.notes.show_note_list()
    return ''

def help_me(*_):
    return "Hi! Here is the list of known commands:\n" + \
           "\tshow all: shows all your contacts by '2' on page\n" + \
           "\t\tor try:\tshow all 'n': to show all your contacts by 'n' on page\n" + \
           "\treset 'n': return to the start of the contacts, sets showed number of contacts on page to 'n'\n" + \
           "\tshow contact 'name': shows information about contact\n" + \
           "\tphone 'name': shows all phone numbers of the contact\n" + \
           "\tadd contact 'name' 'phone number': creates a new contact\n" + \
           "\tset birthday 'name' 'birthday': sets contacts birthday\n" + \
           "\t\t 'birthday' should be in forman 'mm.dd' or 'mm.dd.year'\n" + \
           "\tdelete birthday 'name': deletes birthday from the contact\n" + \
           "\tdelete contact 'name': deletes contact 'name'\n" + \
           "\tadd phone 'name' 'phone numer': adds the phone number to the existing contact or creates a new one\n" + \
           "\t\tphone number should be 7 digits long + optional 3 digits of city code\n" + \
           "\t\t+ optional 2 digits of country code + optional '+' sight\n" + \
           "\tdelete phone 'name' 'phone number': deletes the phone number from contact\n" + \
           "\tsave 'file name': saves you Address book to 'file name'\n" + \
           "\tload 'file name': loads existing Address book from 'file name'\n" + \
           "\tfind 'string': searches 'string' in names and phone numbers\n" + \
           "\tclear: clears your Address book\n" + \
           "\texit: close the assistant\n" + \
           "\tcreate note: creates new note" + \
           "\trename note: renames existing note" + \
           "\tdelete note: deletes existing note" + \
           "\tshow notes: shows all notes content" + \
           "\tshow note list: shows list of notes" + \
           "\tchange note: changes note content"
