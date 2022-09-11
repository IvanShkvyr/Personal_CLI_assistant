from collections import UserDict, UserList
import pickle

class Tags(UserList):       # Tags class. Contains tags strings in list 
    def __init__(self, tags):
        self.data = tags
    def remove_tag(self, tag):      # Deletes tag
        try:
            self.data.remove(tag)
        except KeyError:
            print('This tag does not exists!')
    def change_tag(self, tag, new_tag):     # Changes existing tag to new
        try:
            self.data.remove(tag)
            self.data.append(new_tag)
        except KeyError:
            print('This tag does not exists')
    def add_tag(self, tag):     # Adds new tag
        self.append(tag)

class Note():   # Note class
    def __init__(self, name ,note, tags: Tags = ''):
        self.name = name
        self.note = note
        self.tags = tags
    def __repr__(self):     # Class call returns a string with name, content and tags of note
        try: 
            tags = ', '.join(self.tags)
        except TypeError:
            tags = ''
        return f'''Name: {self.name}
Tags: {tags}

    {self.note}
        '''
    def change_name(self, new_name):    # Changes notes name
        self.name = new_name
    def change_note(self, new_note):    # Changes notes content
        self.note = new_note
    def _tags(self):    # Hidden function. Returns list of tags of note
        return self.tags
    def _name(self):    # Hidden function. Returns name of note
        return self.name
    def _note(self):    # Hidden function. Returns content of note
        return self.note

class Notes(UserDict):      # Notes dict {unique ID:object of class Note()}
    __file_name = "notes.pickle"
    def __init__(self):
        self.data = {}
        self.note_id = 0
    def _restore(self):
        try:
            with open(self.__file_name, "rb+") as file:
                book = pickle.load(file)
                self.data.update(book)
        except Exception:
            print("Notes not restored!")

    def _save(self):
        try:
            with open(self.__file_name, "wb+") as file:
                pickle.dump(self.data, file, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception:
            print("Some problems with saving!")
    
    def add_note(self, note: Note):     # Adds new note
        self.data.update({self.note_id:note})
        self.note_id += 1

    def change_note_name(self, note_id: int, new_note_name):     # Changes name of note
        note = self.find_note_by_id(self._name_id(note_id))
        note.change_name(new_note_name)

    def change_note(self, note_id, new_note):   # Changes notes content
        note = self.find_note_by_id(self._name_id(note_id))
        note.change_note(new_note)
        self.data[note_id] = note
    def delete_note(self, note):    # Deletes note
        note = self._name_id(note)
        try:
            self.data.pop(note)
            self._id_order()
        except KeyError:
            print("This note does not exists!")

    def show_all(self):     # Shows all notes
        for note_id, note in self.data.items():
            print(f'Note ID: {note_id}')
            print(note)

    def find_note_by_id(self, note_id: int):    # Search by ID
        try:
            return self.data[note_id]
        except KeyError:
            print("This note does not exists!")

    def _id_order(self):    # Hidden function, called by delete_note() function. Makes note ID's ordered. 
        data = self.data.copy()
        self.data.clear()
        self.note_id = 0
        for note in data.values():
            self.add_note(note)

    def find_by_tags(self, *tags):      # Search by tags
        to_return = []
        for note_id, each in self.data.items():
            if all(elem in each._tags()  for elem in tags):
                to_return.append(each)
            elif any(elem in each._tags()  for elem in tags):
                to_return.append(each)
        return to_return

    def find_by_name(self, name):       # Search by name

        for note_id,note in self.data.items():
            if name.lower() in note._name().lower():
                return note_id
    def show_note_list(self):   # Prints names of all existing notes
        for each in self.data.values():
            print(each._name())
    def search_in_notes(self, text:str):    # Search in notes content
        to_return = []
        for each in self.data.values():
            if text in each._note():
                to_return.append(each)
        return to_return
    def _name_id(self, string):     # Hidden function. Checks if [string] is notes ID. If not - calls find_by_name() function 
        try:
            return int(string)
        except:
            return self.find_by_name(string)

