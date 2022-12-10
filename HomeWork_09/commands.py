from datetime import datetime

from prompt_toolkit import prompt

from repository.contacts import get_contact_data_view, get_contacts,\
    contact_delete, contact_insert_or_update
from repository.notes import note_delete, note_insert_or_update, get_notes, get_note_data_view
from function import easy_table, sanitize_phone_num, format_phone_num
from database.db_models import DATE_FORMAT


def edit_contact_data(data_view: dict) -> dict:
    data_view["first_name"] = prompt_str_field(data_view, "first_name", True)
    data_view["last_name"] = prompt_str_field(data_view, "last_name")
    data_view["email"] = prompt_str_field(data_view, "email")
    data_view["birthday"] = prompt_date_field(data_view, "birthday")
    data_view["address"] = prompt_str_field(data_view, "address")
    data_view["phone_list"] = prompt_list_field(data_view, "phone_list", False,
                                                format_phone_num, sanitize_phone_num)
    return data_view


def add_cnt_cmd(session):
    data_view = edit_contact_data(get_contact_data_view(session, -1))
    return contact_insert_or_update(session, data_view)


def edit_cnt_cmd(session):
    input_str = prompt("Contact Id: ").strip()
    data_view = edit_contact_data(get_contact_data_view(session, int(input_str)))
    return contact_insert_or_update(session, data_view)


def del_cnt_cmd(session):
    input_str = prompt("Contact Id: ").strip()
    return contact_delete(session, int(input_str))


def find_cnt_cmd(session):
    input_str = prompt("Search string: ")
    result = get_contacts(session, filter_str=input_str)
    if result:
        return easy_table(result)
    else:
        return "No contacts was found."


def edit_note_data(data_view: dict) -> dict:
    data_view["header"] = prompt_str_field(data_view, "header", True)
    data_view["content"] = prompt_str_field(data_view, "content")
    data_view["tag_list"] = prompt_list_field(data_view, "tag_list")

    return data_view


def add_note_cmd(session):
    data_view = edit_note_data(get_note_data_view(session, -1))
    return note_insert_or_update(session, data_view)


def edit_note_cmd(session):
    input_str = prompt("Note Id: ").strip()
    data_view = edit_note_data(get_note_data_view(session, int(input_str)))
    return note_insert_or_update(session, data_view)


def del_note_cmd(session):
    input_str = prompt("Note Id: ").strip()
    return note_delete(session, int(input_str))


def find_note_cmd(session):
    input_str = prompt("Search string: ")
    result = get_notes(session, filter_str=input_str)
    if result:
        return easy_table(result)
    else:
        return "No notes was found."


def exit_cmd(session):
    if session.in_transaction():
        session.commit()
    exit(0)


def prompt_str_field(data_view: dict, field_name: str, required=False) -> str:
    prompt_text = field_name.title().replace("_", " ")
    default_str = data_view[field_name] if data_view[field_name] else ""
    input_str = prompt(f"{prompt_text}: ", default=default_str).strip()
    if required:
        while not input_str:
            input_str = prompt(f"{prompt_text}: ", default=default_str).strip()
    return input_str if input_str else None


def prompt_date_field(data_view: dict, field_name: str, required=False) -> datetime:
    prompt_text = field_name.title().replace("_", " ")
    default_str = data_view[field_name].strftime(DATE_FORMAT) if data_view[field_name] else ""
    input_str = prompt(f"{prompt_text}: ", default=default_str).strip()
    if required:
        while not input_str:
            input_str = prompt(f"{prompt_text}: ", default=default_str).strip()
    return datetime.strptime(input_str, DATE_FORMAT) if input_str else None


def prompt_list_field(data_view: dict, field_name: str, required=False,
                      format_func=None, sanitize_func=None) -> list:
    prompt_text = field_name.title().replace("_", " ")
    f_list = [format_func(item) if format_func else item for item in data_view[field_name]]
    default_str = ", ".join(f_list)
    input_str = prompt(f"{prompt_text}: ", default=default_str).strip()
    if required:
        while not input_str:
            input_str = prompt(f"{prompt_text}: ", default=default_str).strip()
    item_list = list(filter(lambda x: x != "", input_str.lower().split(",")))
    return [sanitize_func(item) if sanitize_func else item.strip() for item in item_list]


COMMANDS = {
    "add cnt": add_cnt_cmd,
    "edit cnt": edit_cnt_cmd,
    "del cnt": del_cnt_cmd,
    "find cnt": find_cnt_cmd,
    "add note": add_note_cmd,
    "edit note": edit_note_cmd,
    "del note": del_note_cmd,
    "find note": find_note_cmd,
    "exit": exit_cmd}
