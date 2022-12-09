from datetime import datetime

from prompt_toolkit import prompt

from repository.contacts import get_contact_data_view, get_contacts,\
    contact_delete, contact_insert_or_update
from repository.notes import note_delete, note_insert_or_update, get_notes, get_note_data_view
from function import easy_table, sanitize_phone_num, format_phone_num
from database.db_models import DATE_FORMAT


def edit_contact_data(data_view: dict) -> dict:
    input_str = ""
    while not input_str:
        input_str = prompt("First name: ", default=data_view["first_name"]).strip()
    data_view["first_name"] = input_str

    default_str = data_view["last_name"] if data_view["last_name"] else ""
    input_str = prompt("Last name: ", default=default_str).strip()
    data_view["last_name"] = input_str if input_str else None

    default_str = data_view["email"] if data_view["email"] else ""
    input_str = prompt("Email: ", default=default_str).strip()
    data_view["email"] = input_str if input_str else None

    default_str = data_view["birthday"].strftime(DATE_FORMAT) if data_view["birthday"] else ""
    input_str = prompt("Birthday: ", default=default_str).strip()
    data_view["birthday"] = datetime.strptime(input_str, DATE_FORMAT) if input_str else None

    default_str = data_view["address"] if data_view["address"] else ""
    input_str = prompt("Address: ", default=default_str).strip()
    data_view["address"] = input_str if input_str else None

    default_str = ", ".join([format_phone_num(phone) for phone in data_view["phone_list"]])
    input_str = prompt("Phones: ", default=default_str)
    phone_list = list(filter(lambda x: x != "", input_str.lower().split(",")))
    data_view["phone_list"] = [sanitize_phone_num(phone_num) for phone_num in phone_list]

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
    input_str = ""
    while not input_str:
        input_str = prompt("Header: ", default=data_view["header"]).strip()
    data_view["header"] = input_str

    default_str = data_view["content"] if data_view["content"] else ""
    input_str = prompt("Content: ", default=default_str).strip()
    data_view["content"] = input_str if input_str else None
    default_str = ", ".join([tag for tag in data_view["tag_list"]])
    input_str = prompt("Tags: ", default=default_str)
    tag_list = list(filter(lambda x: x != "", input_str.lower().split(",")))
    data_view["tag_list"] = [tag.strip() for tag in tag_list]

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
