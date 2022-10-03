from sys import exit
from time import sleep
import enum

from free_assist.abstraction.command import ACommand
from free_assist.folder_sort import FolderSorter


class MsgType(enum.Enum):
    info = 0
    warning = 1
    error = 2
    confirm = 3


class HelpCmd(ACommand):
    def __init__(self, params: str):
        super().__init__(name="help", params=params)
        self.data_name = None

    @classmethod
    def param_check(cls, params: str):
        return not params

    @staticmethod
    def __cmd_name_snt(cmd_name: str, str_len: int = 18) -> str:
        cmd_name = f"'{cmd_name}'"
        return f"{cmd_name.ljust(str_len, '.')}"

    def __call__(self):
        fn = self.__cmd_name_snt
        help_text = (f" 1. {fn('clean folder')}required one parameter: 'folder path';\n"
                     f" 2. {fn('find cnt')}required one parameter: 'search str';\n"
                     f" 3. {fn('add cnt')}requires no parameters to execute;\n"
                     f" 4. {fn('edit cnt')}required one parameter: 'contact name';\n"
                     f" 5. {fn('del cnt')}required one parameter: 'contact name';\n"
                     f" 6. {fn('show cnt')}has one optional parameter: 'page size';\n"
                     f" 7. {fn('birth list')}required one parameter: 'days to birthday';\n"
                     f" 8. {fn('add note')}has one optional parameter: 'note text';\n"
                     f" 9. {fn('edit note')}required one parameter: 'note id';\n"
                     f"10. {fn('del note')}required one parameter: 'note id';\n"
                     f"11. {fn('find note')}required one parameter: 'search tag';\n"
                     f"12. {fn('show note')}has one optional parameter: 'page size';\n"
                     f"13. {fn('close')}requires no parameters to execute;\n"
                     f"14. {fn('exit')}requires no parameters to execute;\n"
                     f"15. {fn('help')}requires no parameters to execute.")

        self.interface.show_message(MsgType.info, help_text)


class CloseCmd(ACommand):
    def __init__(self, params: str = None):
        super().__init__(name="exit", params=params)
        self.data_name = None

    @classmethod
    def param_check(cls, params: str):
        return not params

    def __call__(self, params: str = None):
        self.interface.show_message(MsgType.info, "Good bye!")
        sleep(1)
        exit(0)


class ShowCntCmd(ACommand):
    def __init__(self, params: str):
        super().__init__(name="show cnt", params=params)
        self.data_name = "address_book"
        self.data = None

    @classmethod
    def param_check(cls, params: str):
        return (not params) or (params.isdecimal() and params != "0")

    def __call__(self):
        page_output = bool(self._params)
        self.data.print_page_size = int(self._params) if page_output else -1

        try:
            for contacts in self.data:
                contacts.insert(0, ["Name", "Phones", "Email", "Address", "Birthday"])
                self.interface.show_table_view(contacts)
                if page_output:
                    if not self.interface.show_message(MsgType.confirm, "Continue?"):
                        return
        except KeyboardInterrupt:
            return


class AddCntCmd(ACommand):
    def __init__(self, params: str):
        super().__init__(name="add cnt", params=params)
        self.data_name = "address_book"
        self.data = None

    @classmethod
    def param_check(cls, params: str):
        return not params

    def __call__(self):
        command = EditCntCmd("_")
        command.data = self.data
        command.interface = self.interface
        command()


class EditCntCmd(ACommand):
    def __init__(self, params: str):
        super().__init__(name="edit cnt", params=params)
        self.data_name = "address_book"
        self.data = None

    @classmethod
    def param_check(cls, params: str):
        return len(params)

    def __call__(self):
        cnt_name = self._params
        saved_cnt_name = ""

        if cnt_name != "_":
            contact = self.data.get_contact(cnt_name)
            saved_cnt_name = contact.cnt_name.value.lower()
        else:
            contact = self.data.get_empty_contact()

        edt_record: dict = contact.fields_info
        for key, field in edt_record.items():
            field_instance = getattr(contact, key, None)
            if field_instance:
                if field["is_list"]:
                    field["value"] = " ".join(str(fld) for fld in field_instance)
                else:
                    field["value"] = str(field_instance) if str(field_instance) != "_" else ""
            else:
                field["value"] = ""

        self.interface.edit_data_record(edt_record)

        for key, field in edt_record.items():
            if field["is_list"]:
                list_result = list(filter(lambda x: x != "", field["value"].strip().split(" ")))
                list_inst = [field["class"](itm) for itm in list_result]
                setattr(contact, key, list_inst)
            elif field["value"]:
                setattr(contact, key,  field["class"](field["value"]))

        if saved_cnt_name != contact.cnt_name.value.lower():
            if self.data.is_contact_exist(contact.cnt_name.value.lower()):
                if self.interface.show_message(MsgType.confirm,
                                               f"Contact by name '{contact.cnt_name.value}' exists. Overwrite?"):
                    self.data.del_contact(contact.cnt_name.value.lower())
                else:
                    self.interface.show_message(MsgType.warning, "Editing was canceled by the user")
            if saved_cnt_name:
                self.data.del_contact(saved_cnt_name)

        self.interface.show_message(MsgType.info, self.data.set_contact(contact))


class DelCntCmd(ACommand):
    def __init__(self, params: str):
        super().__init__(name="del cnt", params=params)
        self.data_name = "address_book"
        self.data = None

    @classmethod
    def param_check(cls, params: str):
        return len(params)

    def __call__(self):
        cnt_name = self._params
        self.interface.show_message(MsgType.info, self.data.del_contact(cnt_name))


class FindCntCmd(ACommand):
    def __init__(self, params: str):
        super().__init__(name="find cnt", params=params)
        self.data_name = "address_book"
        self.data = None

    @classmethod
    def param_check(cls, params: str):
        return len(params)

    def __call__(self):
        search_str = self._params
        contacts = self.data.find_contacts(search_str)

        if contacts:
            contacts.insert(0, ["Name", "Phones", "Email", "Address", "Birthday"])
            self.interface.show_table_view(data=contacts, highlight_math=search_str)
        else:
            self.interface.show_message(MsgType.warning, "Contacts not found.")


class BirthdayList(ACommand):
    def __init__(self, params: str):
        super().__init__(name="birth list", params=params)
        self.data_name = "address_book"
        self.data = None

    @classmethod
    def param_check(cls, params: str):
        return len(params.split(" ")) == 1

    def __call__(self):
        try:
            days = int(self._params)
        except ValueError:
            self.interface.show_message(MsgType.error, "The parameter 'Days to birthday' should be an integer.")
            return
        contacts = self.data.birthday_list(days)
        if contacts:
            contacts.insert(0, ["Name", "Phones", "Email", "Address", "Birthday"])
            self.interface.show_table_view(contacts)
        else:
            self.interface.show_message(MsgType.warning, "Contacts not found.")


class AddNoteCmd(ACommand):
    def __init__(self, params):
        super().__init__(name="add note", params=params)
        self.data_name = "note_book"
        self.data = None

    @classmethod
    def param_check(cls, params: str):
        return True

    def __call__(self):
        if self._params:
            self.interface.show_message(MsgType.warning, self.data.add_note(self._params))
            return

        command = EditNoteCmd("-1")
        command.data = self.data
        command.interface = self.interface
        command()


class EditNoteCmd(ACommand):
    def __init__(self, params):
        super().__init__(name="edit note", params=params)
        self.data_name = "note_book"
        self.data = None

    @classmethod
    def param_check(cls, params: str):
        return bool(params) and (params.isdecimal() or params == "-1")

    def __call__(self):
        if self._params == "-1":
            self._params = ""
        note = self.data.get_note(self._params)

        edt_record: dict = note.fields_info
        for key, field in edt_record.items():
            field_instance = getattr(note, key, None)
            if field_instance:
                if field["is_list"]:
                    field["value"] = " ".join(str(fld) for fld in field_instance)
                else:
                    field["value"] = str(field_instance)
            else:
                field["value"] = ""

        self.interface.edit_data_record(edt_record)

        for key, field in edt_record.items():
            if field["is_list"]:
                list_result = list(filter(lambda x: x != "", field["value"].strip().split(" ")))
                list_inst = [field["class"](itm) for itm in list_result]
                setattr(note, key, list_inst)
            elif field["value"]:
                setattr(note, key,  field["class"](field["value"]))

        self.interface.show_message(MsgType.info, self.data.set_note(note))


class ShowNotesCmd(ACommand):
    def __init__(self, params: str):
        super().__init__(name="show notes", params=params)
        self.data_name = "note_book"
        self.data = None

    @classmethod
    def param_check(cls, params: str):
        return (not params) or (params.isdecimal() and params != "0")

    def __call__(self):
        page_output = bool(self._params)
        self.data.print_page_size = int(self._params) if page_output else -1

        try:
            for items in self.data:
                items.insert(0, ["Note id", "Note", "Tags"])
                self.interface.show_table_view(items)
                if page_output:
                    if not self.interface.show_message(MsgType.confirm, "Continue?"):
                        return
        except KeyboardInterrupt:
            return


class DelNoteCmd(ACommand):
    def __init__(self, params: str):
        super().__init__(name="del note", params=params)
        self.data_name = "note_book"
        self.data = None

    @classmethod
    def param_check(cls, params: str):
        return bool(params) and params.isdecimal()

    def __call__(self):
        self.interface.show_message(MsgType.info, self.data.del_note(self._params))


class FindNoteCmd(ACommand):
    def __init__(self, params: str):
        super().__init__(name="find note", params=params)
        self.data_name = "note_book"
        self.data = None

    @classmethod
    def param_check(cls, params: str):
        return len(params)

    def __call__(self):
        search_str = self._params
        notes = self.data.find_notes(search_str)

        if notes:
            notes.insert(0, ["Note id", "Note", "Tags"])
            self.interface.show_table_view(data=notes, highlight_math=search_str)
        else:
            self.interface.show_message(MsgType.warning, "Notes not found.")


class FolderSorting(ACommand):
    data_name = "none"

    def __init__(self, params: str):
        super().__init__(name="folder sort", params=params)
        self.data_name = "none"

    @classmethod
    def param_check(cls, params: str):
        return len(params.split(" ")) == 1

    def __call__(self):
        sorter = FolderSorter(self._params)
        sorter.create_folders()
        sorter.folder_sorting()

        items = sorter.result_sorting()
        if items:
            items.insert(0, ["File types", "Files"])
            self.interface.show_table_view(items)
        else:
            self.interface.show_message(MsgType.warning, "No files for sorting are found.")


COMMANDS = {
    "help":         HelpCmd,
    "clean folder": FolderSorting,
    "birth list":   BirthdayList,
    "find cnt":     FindCntCmd,
    "add cnt":      AddCntCmd,
    "edit cnt":     EditCntCmd,
    "del cnt":      DelCntCmd,
    "show cnt":     ShowCntCmd,
    "add note":     AddNoteCmd,
    "edit note":    EditNoteCmd,
    "del note":     DelNoteCmd,
    "find note":    FindNoteCmd,
    "show notes":   ShowNotesCmd,
    "close":        CloseCmd,
    "exit":         CloseCmd}
