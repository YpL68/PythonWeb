from collections import namedtuple

from prompt_toolkit import prompt, print_formatted_text, ANSI
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.validation import Validator
from prompt_toolkit.shortcuts import confirm

from free_assist.address_book import AddressBook
from free_assist.folder_sort import FolderSorter
from free_assist.notes import Notes
from free_assist.function import *

Param = namedtuple("Param", "name required")
param_style = Style.from_dict({'param_name': '#ffffff'})
caption_style = Style.from_dict({'field_caption': '#ffffff'})


class ExitCmd(Exception):
    pass


class CliCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor().lower().translate(TRANS_KEYS)
        if len(document.current_line_before_cursor.strip()) == len(word):
            for command in COMMANDS:
                if command.find(word) != -1:
                    yield Completion(
                        command,
                        start_position=-len(word),
                        style="fg:black",
                        selected_style="fg:black bg:white",
                    )


class CliCmdParser:
    def __init__(self):
        self.parsed_command = None

    def cmd_parse(self, inp_str: str):
        self.parsed_command = None
        clean_str = " ".join(list(filter(lambda x: x != "", inp_str.lower().split(" ")))) + " "
        for cmd_name in COMMANDS:
            cmd = cmd_name + " "
            if clean_str.startswith(cmd):
                self.parsed_command = COMMANDS[cmd_name](clean_str[len(cmd):].strip())
                break
        else:
            raise ValueError(error_msg(f"Unknown command - '{inp_str}'"))


class CliCommand:
    def __init__(self, name: str, params: str = ""):
        self.name: str = name
        self._params = params


class CloseCmd(CliCommand):
    data_name = "none"

    def __init__(self, params: str):
        super().__init__(name="exit", params=params)

    def __call__(self, params: str):
        raise ExitCmd(info_msg("Good bye!"))


class AddCntCmd(CliCommand):
    data_name = "address_book"

    def __init__(self, params: str):
        super().__init__(name="add cnt", params=params)

    def __call__(self, address_book: AddressBook) -> str:
        if self._params:
            raise ValueError(warning_msg(f"Command add cnt requires no parameters to execute."))
        return EditCntCmd("_")(address_book)


class EditCntCmd(CliCommand):
    data_name = "address_book"

    def __init__(self, params: str):
        super().__init__(name="edit cnt", params=params)

    def __call__(self, address_book: AddressBook) -> str:
        if not self._params:
            raise ValueError(warning_msg(f"Command 'edit cnt' required one parameter: 'Contact name'"))

        cnt_name = self._params
        saved_cnt_name = ""
        if cnt_name != "_":
            contact = address_book.get_contact(cnt_name)
            saved_cnt_name = contact.cnt_name.value.lower()
            print_formatted_text(ANSI(warning_msg("Editing contact...Press 'Ctrl-C' to cancel")))
        else:
            contact = address_book.get_empty_contact()
            print_formatted_text(ANSI(warning_msg("Adding contact...Press 'Ctrl-C' to cancel")))

        for fld_name, fld_info in contact.fields_info.items():
            field_caption = ('class:field_caption', fld_info["caption"] + ": ")
            try:
                def is_valid_field_value(text):
                    return is_valid_field(fld_info["class"], text,
                                          type(field_instance) == list,
                                          fld_info["is_required"])
                validator = Validator.from_callable(
                    is_valid_field_value,
                    error_message=f"Not a valid {fld_info['caption']} value.",
                    move_cursor_to_end=True,
                )
                field_instance = getattr(contact, fld_name, None)
                default_value = ""
                if field_instance:
                    if type(field_instance) == list:
                        default_value = " ".join(str(fld) for fld in field_instance)
                    else:
                        default_value = str(getattr(contact, fld_name))
                if default_value == "_":
                    default_value = ""
                result = prompt([field_caption], validator=validator, validate_while_typing=False,
                                style=caption_style, default=default_value)
                if type(field_instance) == list:
                    list_result = list(filter(lambda x: x != "", result.strip().split(" ")))
                    list_inst = [fld_info["class"](itm) for itm in list_result]
                    setattr(contact, fld_name, list_inst)
                elif result:
                    setattr(contact, fld_name, fld_info["class"](result))
                else:
                    setattr(contact, fld_name, None)
            except KeyboardInterrupt:
                raise ValueError("")

        if saved_cnt_name != contact.cnt_name.value.lower():
            if address_book.is_contact_exist(contact.cnt_name.value.lower()):
                if confirm(f"Contact by name '{contact.cnt_name.value}' exists. Overwrite?"):
                    address_book.del_contact(contact.cnt_name.value.lower())
                else:
                    return warning_msg("The operation was canceled.")
            if saved_cnt_name:
                address_book.del_contact(saved_cnt_name)

        return address_book.set_contact(contact)


class DelCntCmd(CliCommand):
    data_name = "address_book"

    def __init__(self, params: str):
        super().__init__(name="del cnt", params=params)

    def __call__(self, address_book: AddressBook) -> str:
        if not self._params:
            raise ValueError(warning_msg(f"Command 'edit cnt' required one parameter: 'Contact name'"))
        cnt_name = self._params
        return address_book.del_contact(cnt_name)


class ShowCntCmd(CliCommand):
    data_name = "address_book"

    def __init__(self, params: str):
        super().__init__(name="show cnt", params=params)

    def __call__(self, address_book: AddressBook):
        if len(self._params.split(" ")) > 1:
            raise ValueError(warning_msg(f"Command 'show cnt' has one optional parameter: 'Page size'"))
        page_output = False
        address_book.print_page_size = -1
        if self._params and self._params != "0":
            try:
                address_book.print_page_size = int(self._params)
                page_output = True
            except ValueError:
                print_formatted_text(ANSI(error_msg("The parameter 'Page size' should be an integer.")))
                return

        try:
            for contacts in address_book:
                contacts.insert(0, ["Name", "Phones", "Email", "Address", "Birthday"])
                print_formatted_text(ANSI(easy_table(data=contacts)))
                if page_output:
                    prompt("Press ENTER to continue...")
        except KeyboardInterrupt:
            return


class FindCntCmd(CliCommand):
    data_name = "address_book"

    def __init__(self, params: str):
        super().__init__(name="find cnt", params=params)

    def __call__(self, address_book: AddressBook):
        if not self._params:
            raise ValueError(warning_msg(f"Command 'find cnt' required one parameter: 'Search str'"))
        search_str = self._params
        contacts = address_book.find_contacts(search_str)
        if contacts:
            contacts.insert(0, ["Name", "Phones", "Email", "Address", "Birthday"])
            print_formatted_text(ANSI(easy_table(data=contacts, highlight_math=search_str)))
        else:
            print_formatted_text(ANSI(warning_msg("Contacts not found.")))


class BirthdayList(CliCommand):
    data_name = "address_book"

    def __init__(self, params: str):
        super().__init__(name="birth list", params=params)

    def __call__(self, address_book: AddressBook):
        if not self._params:
            raise ValueError(warning_msg(f"Command 'birth list' required one parameter: 'Days to birthday'"))
        try:
            days = int(self._params)
        except ValueError:
            raise ValueError(error_msg("The parameter 'Days to birthday' should be an integer."))
        contacts = address_book.birthday_list(days)
        if contacts:
            contacts.insert(0, ["Name", "Phones", "Email", "Address", "Birthday"])
            print_formatted_text(ANSI(easy_table(data=contacts)))
        else:
            print_formatted_text(ANSI(warning_msg("Contacts not found.")))


class AddNoteCmd(CliCommand):
    data_name = "note_book"

    def __init__(self, params):
        super().__init__(name="add note", params=params)

    def __call__(self, notes: Notes) -> str:
        if self._params:
            return notes.add_note(self._params)
        try:
            note = notes.get_note()
            default_value = ""
            field_caption = ('class:field_caption', "Note: ")
            print_formatted_text(ANSI(warning_msg("Adding a note. Press [Meta+Enter] or [Esc+Enter] to accept input.")))
            result = prompt(
                [field_caption], multiline=True, prompt_continuation=prompt_continuation,
                default=default_value, style=caption_style
            )
            note.note_text = result
            field_caption = ('class:field_caption', "Tags: ")
            result = prompt(
                [field_caption], multiline=False, default=default_value, style=caption_style
            )
            note.note_tags = list(filter(lambda x: x != "", result.lower().split(" ")))
        except KeyboardInterrupt:
            raise ValueError("")
        return notes.set_note(note)


class EditNoteCmd(CliCommand):
    data_name = "note_book"

    def __init__(self, params):
        super().__init__(name="edit note", params=params)

    def __call__(self, notes: Notes) -> str:

        if not self._params:
            raise ValueError(warning_msg(f"Command 'edit note' required one parameter: 'Note ID'"))
        try:
            if not self._params.isdecimal():
                raise ValueError(error_msg("The parameter 'Note ID' should be an integer."))
            note = notes.get_note(self._params)

            default_value = note.note_text
            field_caption = ('class:field_caption', "Note: ")
            print_formatted_text(ANSI(warning_msg("Editing a note. Press [Meta+Enter] "
                                                  "or [Esc+Enter] to accept input.")))
            result = prompt(
                [field_caption], multiline=True, prompt_continuation=prompt_continuation,
                default=default_value, style=caption_style
            )
            note.note_text = result
            default_value = note.tag_list
            field_caption = ('class:field_caption', "Tags: ")
            result = prompt(
                [field_caption], multiline=False, default=default_value, style=caption_style
            )
            note.note_tags = list(filter(lambda x: x != "", result.lower().split(" ")))
        except KeyboardInterrupt:
            raise ValueError("")
        return notes.set_note(note)


class DelNoteCmd(CliCommand):
    data_name = "note_book"

    def __init__(self, params: str):
        super().__init__(name="del note", params=params)

    def __call__(self, notes: Notes) -> str:
        if not self._params:
            raise ValueError(warning_msg(f"Command 'del note' required one parameter: 'Note ID'"))
        elif not self._params.isdecimal():
            raise ValueError(error_msg("The parameter 'Note ID' should be an integer."))
        return notes.del_note(self._params)


class FindNoteCmd(CliCommand):
    data_name = "note_book"

    def __init__(self, params: str):
        super().__init__(name="find note", params=params)

    def __call__(self, notes: Notes):
        if not self._params or len(self._params.split(" ")) > 1:
            raise ValueError(warning_msg(f"Command 'find note' required one parameter: 'Search tag'"))
        notes = notes.find_notes(self._params)
        if notes:
            notes.insert(0, ["Note id", "Note", "Tags"])
            print_formatted_text(ANSI(easy_table(data=notes, highlight_math=self._params)))
        else:
            print_formatted_text(ANSI(warning_msg("No notes have been found.")))


class ShowNotesCmd(CliCommand):
    data_name = "note_book"

    def __init__(self, params: str):
        super().__init__(name="show notes", params=params)

    def __call__(self, notes: Notes):
        if len(self._params.split(" ")) > 1:
            raise ValueError(warning_msg(f"Command 'show notes' has one optional parameter: 'Page size'"))
        page_output = False
        notes.print_page_size = -1
        if self._params and self._params != "0":
            try:
                notes.print_page_size = int(self._params)
                page_output = True
            except ValueError:
                print_formatted_text(ANSI(error_msg("The parameter 'Page size' should be an integer.")))
                return

        try:
            for items in notes:
                items.insert(0, ["Note id", "Note", "Tags"])
                print_formatted_text(ANSI(easy_table(data=items)))
                if page_output:
                    prompt("Press ENTER to continue...")
        except KeyboardInterrupt:
            return


class FolderSorting(CliCommand):
    data_name = "none"

    def __init__(self, params: str):
        super().__init__(name="folder sort", params=params)

    def __call__(self, notes: Notes):
        if not self._params or len(self._params.split(" ")) > 1:
            raise ValueError(warning_msg(f"Command 'folder sort' required one parameter: 'Folder path'"))

        sorter = FolderSorter(self._params)
        sorter.create_folders()
        sorter.folder_sorting()

        items = sorter.result_sorting()
        if items:
            items.insert(0, ["File types", "Files"])
            print_formatted_text(ANSI(easy_table(data=items)))


class HelpCmd(CliCommand):
    data_name = "none"

    def __init__(self, params: str):
        super().__init__(name="help", params=params)

    @staticmethod
    def __cmd_name_snt(cmd_name: str, str_len: int = 18) -> str:
        cmd_name = f"'{cmd_name}'"
        return f"{cmd_name.ljust(str_len, '.')}"

    def __call__(self, params: str) -> str:
        fn = self.__cmd_name_snt
        return info_msg(f" 1. {fn('clean folder')}required one parameter: 'folder path';\n"
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
