from collections import UserDict, UserList

class Tags():       # Класс тэгов. Хранит список тэгов
    def __init__(self, tags):
        self.data = tags
    def remove_tag(self, tag):      # Удаление существующего тэга
        try:
            self.data.remove(tag)
        except KeyError:
            print('This tag does not exists!')
    def change_tag(self, tag, new_tag):     # Смена существующего тэга на новый
        try:
            self.data.remove(tag)
            self.data.append(new_tag)
        except KeyError:
            print('This tag does not exists')
    def add_tag(self, tag):     # Добавление нового тэга
        self.append(tag)

class Note():   # Класс записки
    def __init__(self, name ,note, tags: Tags = ''):
        self.name = name
        self.note = note
        self.tags = tags
    def __repr__(self):     # Вызов класса возвращает строку с именем, тэгами и содержанием записки
        try: 
            tags = ', '.join(self.tags)
        except TypeError:
            tags = ''
        return f'''Name: {self.name}
Tags: {tags}

    {self.note}
        '''
    def change_name(self, new_name):    # Смена названия записки
        self.name = new_name
    def change_note(self, new_note):    # Смена содержания записки
        self.note = new_note
    def _tags(self):    # Функция при вызове возвращает класс тэгов
        return self.tags
    def _name(self):
        return self.name

class Notes(UserDict):      # Класс записок. Тип - словарь вида {уникальный ID записки:записка класса Note}
    def __init__(self):
        self.data = {}
        self.note_id = 0
    def add_note(self, note: Note):     # Добавляет новую записку в словарь
        self.data.update({self.note_id:note})
        self.note_id += 1
    def change_note_name(self, note_id: int, new_note_name):     # Изменяет название записки
        note = self.find_note_by_id(note_id)
        note.change_name(new_note_name)
        self.data[note_id] = note
    def change_note(self, note_id, new_note):   # Изменяет содержание записки
        note = self.find_note_by_id(self._name_id(note_id))
        note.change_note(new_note)
        self.data[note_id] = note
    def delete_note(self, note):    # Удаляет записку
        note = self._name_id(note)
        try:
            self.data.pop(note)
            self._id_order()
        except KeyError:
            print("This note does not exists!")
    def show_all(self):     # Показывает все записки
        for note_id, note in self.data.items():
            print(f'Note ID: {note_id}')
            print(note)
    def find_note_by_id(self, note_id: int):    # Поиск записки по уникальному ID
        try:
            return self.data[note_id]
        except KeyError:
            print("This note does not exists!")
    def _id_order(self):    # Скрытый метод, вызывается при удалении записи. Упорядочивает уникальные ID записей во избежание наложения
        data = self.data.copy()
        self.data.clear()
        self.note_id = 0
        for note in data.values():
            self.add_note(note)
    def find_by_tags(self, *tags):      # Поиск по тэгам
        to_return = []
        tags = list(tags)
        for note_id, each in self.data.items():
            if all(elem in each._tags()  for elem in tags):
                to_return.append(each)
            elif any(elem in each._tags()  for elem in tags):
                to_return.append(each)
        return to_return
    def find_by_name(self, name):       # Поиск записи по имени
        for note_id,note in self.data.items():
            if name.lower() in note._name().lower():
                return note_id
    def _name_id(self, string):
        try:
            return int(string)
        except:
            return self.find_by_name(string)