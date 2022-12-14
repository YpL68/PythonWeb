import shelve
from pathlib import Path
from free_assist.abstraction.data import ABook, ARecord


class Note(ARecord):
    def __init__(self, note_text: str = "", note_tags: list = None):
        self.note_id = str(Notes.get_max_note_id())
        self.note_text = note_text
        self.note_tags = note_tags if note_tags else []

    @classmethod
    def data_view(cls, note):
        return {"key_value": {"value": note.note_id if note else ""},
                "note_text": {"caption": "Note", "class": str, "is_list": False, "is_required": True,
                              "value": note.note_text if note else ""},
                "note_tags": {"caption": "Tags", "class": str, "is_list": True, "is_required": False,
                              "value": note.tag_list if note and note.tag_list else ""}}

    @property
    def tag_list(self) -> str:
        return ' '.join(self.note_tags)

    @property
    def values(self) -> list:
        return [self.note_id, self.note_text, self.tag_list if self.note_tags else ""]

    def match_search_str(self, search_str: str):
        search_str = search_str.strip().lower()
        if search_str in self.note_tags:
            return True
        return False


class Notes(ABook):
    __max_note_id = 0

    def __init__(self):
        data_path = Path(Path(Path.home(), "FreeAssistData"))
        data_path.mkdir(exist_ok=True)
        self.__data = shelve.open(str(Path(data_path, "notes")), flag='c')
        if self.__data.keys():
            self.set_max_note_id(max(int(key) for key in self.__data.keys()))
        else:
            self.set_max_note_id(0)

    def __del__(self):
        self.__data.close()

    @classmethod
    def get_max_note_id(cls):
        cls.__max_note_id += 1
        return cls.__max_note_id

    @classmethod
    def set_max_note_id(cls, value):
        cls.__max_note_id = value

    def add_record(self, note_text: str) -> str:
        note = Note(note_text)
        self[note.note_id] = note
        return f"Note by id {note.note_id} has been added to note book."

    def del_record(self, note_id: str) -> str:
        del self[note_id]
        return f"Note by id {note_id} has been deleted from note book."

    def get_record(self, note_id: str = None) -> Note:
        if note_id:
            return self[note_id]
        else:
            return Note()

    def post_record(self, note: Note) -> str:
        self[note.note_id] = note
        return f"Note by id {note.note_id} has been saved to note book."

    def get_record_view(self, note_id: str = None) -> dict:
        return Note.data_view(self[note_id] if note_id else None)

    def post_from_record_view(self, record_view: dict) -> str:
        new_key_value = record_view["key_value"]["value"]

        note = self[new_key_value] if new_key_value else Note()
        record_view.pop("key_value")
        for key, field in record_view.items():
            if field["is_list"]:
                list_result = list(filter(lambda x: x != "", field["value"].strip().split(" ")))
                list_inst = [field["class"](itm) for itm in list_result]
                setattr(note, key, list_inst)
            elif field["value"]:
                setattr(note, key, field["class"](field["value"]))

        self[note.note_id] = note
        return f"Note by id {note.note_id} has been saved to note book."

    def find_records(self, search_str: str) -> list:
        if not search_str or len(search_str) < 2:
            raise ValueError("The search string cannot be shorter than 2 characters.")

        find_notes = []
        search_str = search_str.strip().lower()
        for note in self.__data.values():
            if note.match_search_str(search_str):
                find_notes.append(note.values)
        return find_notes

    def is_record_exists(self, *args, **kwargs) -> bool:
        pass

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, note_id: str) -> Note:
        result = self.__data.get(note_id)
        if not result:
            raise ValueError(f"A note by id '{note_id}' not found.")
        return result

    def __setitem__(self, note_id: str, note: Note):
        self.__data[note_id] = note

    def __delitem__(self, note_id: str):
        try:
            del self.__data[note_id]
        except KeyError:
            raise KeyError(f"A note by id '{note_id}' not found.")

    def __iter__(self):
        self.__rec_counter = 0
        self.__len = len(self.__data)
        if not self.__len:
            raise ValueError("No notes have been found.")
        self.print_page_size = getattr(self, "print_page_size", -1)
        self.add_field_headers = getattr(self, "add_field_headers", False)
        if self.print_page_size == -1:
            self.print_page_size = self.__len
        self.__sorted_keys = (key for key in sorted(self.__data, key=lambda i: int(i)))
        return self

    def __next__(self):
        if self.__rec_counter < self.__len:
            out_list = []
            while len(out_list) < self.print_page_size and self.__rec_counter < self.__len:
                self.__rec_counter += 1
                key = next(self.__sorted_keys)
                out_list.append(self.__data[key].values)
            if self.add_field_headers and out_list:
                out_list.insert(0, ["Note id", "Note", "Tags"])
            return out_list
        else:
            raise StopIteration
